# -*- coding: utf-8 -*-
# Make the retweets random
__author__ = "Johnnatan Messias"
__copyright__ = "Max Planck Institute for Software and Systems - MPI-SWS"
__email__ = "johnme@mpi-sws.org"
__status__ = "In production"

# ----- Kernel Imports ----- #
import sys
import json
import psycopg2
import time
import random
import math
import traceback
import requests
import datetime
import unicodedata
from collections import Counter

# ----- Kernel Imports ----- #



max_images = 2500
max_audios = 500
max_videos = 500
max_msgs   = 500
max_links  = 500
max_stickers  = 2500

offset_images = 30
offset_videos = 30
offset_audios = 30
offset_message= 50
offset_links  = 50
offset_stickers  = 50

whatsapp_audio_table   = "whatsapp_audio"
whatsapp_image_table   = "whatsapp_image"
whatsapp_sticker_table = "whatsapp_sticker"
whatsapp_link_table    = "whatsapp_link"
whatsapp_message_table = "whatsapp_message"
whatsapp_video_table   = "whatsapp_video"
whatsapp_tag_table     = "whatsapp_tag"

# Function to connect to the database

def set_offset(type, offset):
    if type == 'images':   
        offset_images = int(offset);
    elif type == 'audios':   
        offset_audios = int(offset);
    elif type == 'links':    
        offset_links = int(offset);
    elif type == 'videos':   
        offset_videos = int(offset);
    elif type == 'messages': 
        offset_message = int(offset);
    elif type == 'stickers': 
        offset_stickers = int(offset);
    else:
        offset_images = int(offset);
     


def check_end_date_condition(start_date, end_date):
    f = "(obtained_at = TO_DATE('%s', 'YYYY-MM-DD'))" %start_date
    t = "(obtained_at BETWEEN TO_DATE('%s', 'YYYY-MM-DD') AND  TO_DATE('%s', 'YYYY-MM-DD'))" % (start_date, end_date) 
    if len(end_date) < 5:
        return f
    
    if end_date <= start_date:
        return f
    
    return  t


def merge_data_by_key(data, key, nameid):
    merged = dict()
    final_data = list()
    count = 0
    for item in data:
        if not item[key] or len(item[key]) <= 1:
            merged["id"+str(count)] = list()
            merged["id"+str(count)].append(item)
            count +=1
        else:
            if item[key] not in merged.keys():
                merged[item[key]] = list()
            merged[item[key]].append(item)
    
    for k in merged.keys():
        item = merged[k]
        new_item = dict()
        groups = list()
        users = list()
        context_now = list()
        context_pre = list()
        context_pos = list()
        for i in item:
            if  i['shared_groups']:
                for g in i['shared_groups']:
                    if g not in groups:
                        groups.append(g)
            if  i['shared_users']:       
                for u in i['shared_users']:
                    if u not in users:
                        users.append(u)
            if  'context_now' in i.keys():       
                for cnow in i['context_now']:
                    if cnow not in context_now:
                        context_now.append(cnow)
            if  'context_pre' in i.keys():  
                for cpre in i['context_pre']:
                    if cpre not in context_pre:
                        context_pre.append(cpre)
            if  'context_pos' in i.keys():  
                for cpos in i['context_pos']:
                    if cpos not in context_pos:
                        context_pos.append(cpos)
        new_item['shared_groups']      = groups
        new_item['shareNumberGroups']  = len(groups)
        new_item['shared_users']       = users
        new_item['shareNumberUsers']   = len(users)
        new_item['checksum']           = item[0]['checksum']
        new_item['context_now']        = context_now
        new_item['context_pre']        = context_pre
        new_item['context_pos']        = context_pos
        new_item[nameid]               = item[0][nameid]
        if nameid == 'audioid':            new_item['url']  = item[0]['url']
        if 'nsfw_score' in item[0].keys(): new_item['nsfw_score']  = item[0]['nsfw_score']
        if 'phash'      in item[0].keys(): new_item['phash']       = item[0]['phash']
        new_item['shareNumber'] = sum([i['shareNumber'] for  i in item])
        new_item['obtained_at'] = min([i['obtained_at'] for  i in item])
        new_item['end_date']    = max([i['obtained_at'] for  i in item])
        new_item[key]  = k
        new_item['filename']  = item[0]['filename']
        final_data.append(new_item)
        
    new_list =  sorted(final_data, key=lambda k: k['shareNumber'], reverse=True) 
    #for k in new_list:
    #    if  k['shareNumber'] <=3: break
    #    print k[key], k['shareNumber']
    
    return new_list


    
    
def connect_app_database():
    conn_string = "host=localhost dbname=whatsapp user=whomakestrends password=678hjba!@1ABCUyvs8"
    conn = psycopg2.connect(conn_string)
    return conn


def get_images_by_date(conn, obtained_at, offset,  end_date):
    cursor = conn.cursor()
    date_condition = check_end_date_condition( obtained_at, end_date)
    sql = "SELECT imageID, rankingday, sharenumber, sharenumberusers, sharenumbergroups, obtained_at, shared_groups, shared_users, checksum, phash, nsfw_score, context_now, context_pre, context_pos, filename FROM {table_name} WHERE ".format(table_name=whatsapp_image_table) +      date_condition + " ORDER BY sharenumber DESC, sharenumberusers DESC, sharenumbergroups DESC LIMIT {max_images};".format(max_images=max_images)
    data = list()
    cursor.execute(sql, data)
    response = cursor.fetchall()
    response =  list(map(lambda x: {'imageid': x[0], 'rankingDay': x[1],  'shareNumber': x[2], 'shareNumberUsers': x[3], 'shareNumberGroups': x[4], 'obtained_at': x[5].strftime('%m/%d/%Y'), 'shared_groups': x[6], 'shared_users': x[7], 'checksum': x[8],'phash': x[9] ,'nsfw_score': x[10],'context_now': x[11],'context_pre': x[12],'context_pos': x[13], 'filename': x[14]}, response))
    response = merge_data_by_key(response, 'phash', 'imageid')
    return response



def get_stickers_by_date(conn, obtained_at, offset,  end_date):
    cursor = conn.cursor()
    date_condition = check_end_date_condition( obtained_at, end_date)
    sql = "SELECT imageID, rankingday, sharenumber, sharenumberusers, sharenumbergroups, obtained_at, shared_groups, shared_users, checksum, phash, nsfw_score, context_now, context_pre, context_pos, filename FROM {table_name} WHERE ".format(table_name=whatsapp_sticker_table) +      date_condition + " ORDER BY sharenumber DESC, sharenumberusers DESC, sharenumbergroups DESC LIMIT {max_stickers};".format(max_stickers=max_stickers)
    data = list()
    cursor.execute(sql, data)
    response = cursor.fetchall()
    response =  list(map(lambda x: {'imageid': x[0], 'rankingDay': x[1],  'shareNumber': x[2], 'shareNumberUsers': x[3], 'shareNumberGroups': x[4], 'obtained_at': x[5].strftime('%m/%d/%Y'), 'shared_groups': x[6], 'shared_users': x[7], 'checksum': x[8],'phash': x[9] ,'nsfw_score': x[10],'context_now': x[11],'context_pre': x[12],'context_pos': x[13], 'filename': x[14]}, response))
    response = merge_data_by_key(response, 'checksum', 'imageid')
    return response


def get_audios_by_date(conn, obtained_at, offset,  end_date):
    # sql = "SELECT audioID FROM {table_name} WHERE obtained_at = TO_DATE(%s, 'YYYY-MM-DD') ORDER BY rankingday ASC, sharenumber DESC, sharenumberusers DESC, sharenumbergroups DESC LIMIT {max_audios} OFFSET %s;".format(table_name=whatsapp_audio_table, max_audios=max_audios)   
    cursor = conn.cursor()
    date_condition = check_end_date_condition(obtained_at, end_date)
    sql = "SELECT audioID, rankingday, sharenumber, sharenumberusers, sharenumbergroups, obtained_at, shared_groups, shared_users, duration, checksum, context_now, context_pre, context_pos, filename FROM {table_name} WHERE ".format(table_name=whatsapp_audio_table) +           date_condition + " ORDER BY sharenumber DESC, sharenumberusers DESC, sharenumbergroups DESC LIMIT {max_audios};".format(max_audios=max_audios)
    data = (obtained_at, )
    cursor.execute(sql, data)
    response = cursor.fetchall()
    response =  list(map(lambda x: {'name': "Áudio", 'url': 'http://150.164.214.48/monitor-de-whatsapp/data/audios/' + str(x[0]), 'audioid': x[0], 'rankingDay': x[1],  'shareNumber': x[2], 'shareNumberUsers': x[3], 'shareNumberGroups': x[4], 'obtained_at': x[5].strftime('%m/%d/%Y'), 'shared_groups': x[6], 'shared_users': x[7], 'duration': x[8], 'checksum': x[9], 'context_now': x[10],'context_pre': x[11],'context_pos': x[12], 'filename': x[13] }, response))
    response = merge_data_by_key(response, 'checksum', 'audioid')
    return response

def get_videos_by_date(conn, obtained_at, offset, end_date):
    cursor = conn.cursor()
    date_condition = check_end_date_condition( obtained_at, end_date)
    sql = "SELECT videoid, rankingday, sharenumber, sharenumberusers, sharenumbergroups, obtained_at, shared_groups, shared_users, checksum, nsfw_score, context_now, context_pre, context_pos, filename  FROM {table_name} WHERE ".format(table_name=whatsapp_video_table) +    date_condition + "ORDER BY sharenumber DESC, sharenumberusers DESC LIMIT {max_videos};".format(max_videos=max_videos)
    data = list()
    cursor.execute(sql, data)
    response = cursor.fetchall()
    response = list(map(lambda x: {'videoid': x[0], 'rankingDay': x[1],  'shareNumber': x[2], 'shareNumberUsers': x[3], 'shareNumberGroups': x[4], 'obtained_at': x[5].strftime('%m/%d/%Y'), 'shared_groups': x[6], 'shared_users': x[7], 'checksum': x[8], 'nsfw_score': x[9], 'context_now': x[10],'context_pre': x[11],'context_pos': x[12], 'filename': x[13]}, response))
    response = merge_data_by_key(response, 'checksum', 'videoid')
    return response
	    
    
    
def get_links_by_date(conn, obtained_at, offset,  end_date):
    cursor = conn.cursor()
    date_condition = check_end_date_condition( obtained_at, end_date)
    sql = "SELECT link, rankingday, sharenumber, sharenumberusers, sharenumbergroups, obtained_at, link_title, link_description, link_image, link_author, link_date, link_keywords, shared_groups, shared_users  FROM  {table_name}    WHERE ".format(table_name=whatsapp_link_table) + date_condition + " ORDER BY sharenumber DESC, sharenumberusers DESC LIMIT {max_links};".format(max_links=max_links)
    data = list( )
    cursor.execute(sql, data)
    response = cursor.fetchall()
    response = list(map(lambda x: {'LinkID': x[0], 'rankingDay': x[1],  'shareNumber': x[2], 'shareNumberUsers': x[3], 'shareNumberGroups': x[4], 'obtained_at': x[5].strftime('%m/%d/%Y'),  'link_title': x[6], 'link_description': x[7], 'link_image': x[8], 'link_author': x[9], 'link_date': x[10], 'link_keywords': x[11], 'shared_groups': x[12], 'shared_users': x[13]}, response))
    return response

	
def get_messages_by_date(conn, obtained_at, offset,  end_date):
    cursor = conn.cursor()
    date_condition = check_end_date_condition( obtained_at, end_date)
    sql = "SELECT message, rankingday, sharenumber, sharenumberusers, sharenumbergroups, obtained_at, shared_groups, shared_users, id  FROM {table_name} WHERE".format(table_name=whatsapp_message_table) + date_condition +  " ORDER BY sharenumber DESC, sharenumberusers DESC LIMIT {max_messages};".format(max_messages=max_msgs)
    data = list( )
    cursor.execute(sql, data)
    response = cursor.fetchall()
    response = list(map(lambda x: {'message': x[0], 'rankingDay': x[1],  'shareNumber': x[2], 'shareNumberUsers': x[3], 'shareNumberGroups': x[4], 'obtained_at': x[5].strftime('%m/%d/%Y'), 'shared_groups': x[6], 'shared_users': x[7], 'messageid':x[8]}, response))
    return response
	
	
	

	
def get_today():
    return datetime.datetime.today().strftime('%Y-%m-%d')

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')


def tags_rename(tags):
    for tag in list(tags.keys()):
        tag_new = 'tag_' + tag
        tags[tag_new] = tags.pop(tag)
    return tags


def is_tag_on_database(conn, email, imageid):
    cursor = conn.cursor()
    sql = "SELECT EXISTS (SELECT 1 FROM whatsapp_tag WHERE email = %s AND imageid = %s);"
    data = (email, imageid)
    cursor.execute(sql, data)
    return cursor.fetchone()[0]


def persist_tags_on_database(conn, email, imageid, comments, tags, type):
    if not is_tag_on_database(conn=conn, email=email, imageid=imageid):
        tags = tags_rename(tags=tags)
        cursor = conn.cursor()
        registered_at = get_today()
        comments =  comments.encode('utf-8', 'surrogateescape').decode('utf-8', 'replace')
        
        sql = """INSERT INTO whatsapp_tag (email, imageid, tag_verdadeira, tag_suspeita_a_ser_verdadeira, tag_suspeita_a_ser_falsa, 
			tag_falsa, tag_noticia, tag_satira, tag_conteudo_politico, tag_disseminacao_de_odio, tag_conteudo_improprio, tag_violencia, 
			tag_selfie, tag_merece_investigacao, tag_promocao_de_produtos_ilicitos, tag_propaganda, tag_ativismo, tag_opiniao, tag_foto, tag_diversos, tag_outros, registered_at, type) VALUES
			(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::TEXT, TO_DATE(%s, 'YYYY-MM-DD'), %s);"""
        
        data = 	(	 email, imageid, tags['tag_verdadeira'] ,  tags['tag_suspeita_a_ser_verdadeira'] ,  tags['tag_suspeita_a_ser_falsa'] , 
            tags['tag_falsa'] ,  tags['tag_noticia'] ,  tags['tag_satira'] ,  tags['tag_conteudo_politico'] ,  tags['tag_disseminacao_de_odio'] , 
			tags['tag_conteudo_improprio'] ,  tags['tag_violencia'] ,  tags['tag_selfie'] ,  tags['tag_merece_investigacao'] , 
			tags['tag_promocao_de_produtos_ilicitos'] ,  tags['tag_propaganda'] ,  tags['tag_ativismo'] ,  tags['tag_opiniao'] ,  tags['tag_foto'] ,   tags['tag_diversos'] , comments, registered_at, type)
        
        cursor.execute(sql, data)
        conn.commit()
    return 'successful'

   

def main():
    arg = sys.argv[1]
    
    #p = '{"op": 1010, "obtained_at": "2019-01-25", "end_date": "2019-01-30", "offset": 0, "type": "image"}'
    #p1 = '{"op": 1010, "obtained_at": "2022-06-12", "end_date": "2022-06-12", "offset": 30, "type":"images"}'
    
    
    #arg = p1
    params = json.loads(arg)

    op = params['op']
    results = {}
    conn = connect_app_database()

    if op == 1010:
        obtained_at = params['obtained_at']
        end_date    = params['end_date']
        offset      = params['offset']
        type        = params['type']
        set_offset(type, offset)
        
        images   = []
        audios   = []
        links    = []
        messages = []
        videos   = []
        images   = get_images_by_date  (conn=conn, obtained_at=obtained_at, offset=offset, end_date=end_date)
        audios   = get_audios_by_date  (conn=conn, obtained_at=obtained_at, offset=offset, end_date=end_date)
        links    = get_links_by_date   (conn=conn, obtained_at=obtained_at, offset=offset, end_date=end_date)
        messages = get_messages_by_date(conn=conn, obtained_at=obtained_at, offset=offset, end_date=end_date)
        videos   = get_videos_by_date  (conn=conn, obtained_at=obtained_at, offset=offset, end_date=end_date)
        stickers = get_stickers_by_date  (conn=conn, obtained_at=obtained_at, offset=offset, end_date=end_date)
        	
        #results = {'images': images, 'audios': audios, 'links':links}
        results = {'images': images, 'audios': audios, 'links':links, 'messages':messages, 'videos':videos, 'stickers':stickers}
        
    elif op == 102312:
        email = params['email']
        imageid = params['imageid']
        comments = params['comments']
        tags = params['tags']
        type = params['type']
        results = persist_tags_on_database(conn=conn, email=email, imageid=imageid, comments=comments, tags=tags, type=type)
        
    print(json.dumps({'status': 'ok', "param":arg, 'response': results}))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({'status': 'error', 'response': str(traceback.print_exc())}))

