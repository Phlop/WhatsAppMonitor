# -*- coding: utf-8 -*-

__author__ = "Johnnatan Messias"
__copyright__ = "Departamento de Ciência da Computacao - UFMG - Brazil"
__email__ = "johnnatan@dcc.ufmg.br"
__website__ = "http://johnnatan.me"
__status__ = "Done"

import json
import gzip
import time
import traceback
import psycopg2
from unicodedata import normalize

import datetime
from datetime import date as DATE
from datetime import timedelta
from datetime import datetime


whatsapp_audio_table   = "whatsapp_audio"
whatsapp_image_table   = "whatsapp_image"
whatsapp_sticker_table = "whatsapp_sticker"
whatsapp_link_table    = "whatsapp_link"
whatsapp_message_table = "whatsapp_message"
whatsapp_video_table   = "whatsapp_video"

db_host = "localhost"
db_name = "whatsapp"
db_user = "whomakestrends"
db_password = "678hjba!@1ABCUyvs8"



def connect_app_database():
    conn_string = "host=%s dbname=%s user=%s password=%s"%(db_host, db_name, db_user, db_password)
    conn = psycopg2.connect(conn_string)
    return conn


def getCurrentTime():
   return '%s' % (time.strftime("%Y-%m-%d--%H-%M-%S"))


def remove_special_caracter(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


def is_image_on_database(conn, image_id, obtained_at):
    cursor = conn.cursor()
    sql = "SELECT EXISTS (SELECT 1 FROM {table_name} WHERE imageid = %s AND obtained_at = TO_DATE(%s, 'YYYY-MM-DD'));".format(table_name=whatsapp_image_table)
    data = (image_id, obtained_at)
    cursor.execute(sql, data)
    return cursor.fetchone()[0]



def is_sticker_on_database(conn, image_id, obtained_at):
    cursor = conn.cursor()
    sql = "SELECT EXISTS (SELECT 1 FROM {table_name} WHERE imageid = %s AND obtained_at = TO_DATE(%s, 'YYYY-MM-DD'));".format(table_name=whatsapp_sticker_table)
    data = (image_id, obtained_at)
    cursor.execute(sql, data)
    return cursor.fetchone()[0]


def is_video_on_database(conn, video_id, obtained_at):
    cursor = conn.cursor()
    sql = "SELECT EXISTS (SELECT 1 FROM {table_name} WHERE videoid = %s AND obtained_at = TO_DATE(%s, 'YYYY-MM-DD'));".format(table_name=whatsapp_video_table)
    data = (video_id, obtained_at)
    cursor.execute(sql, data)
    return cursor.fetchone()[0]


    
def is_audio_on_database(conn, audio_id, obtained_at):
    cursor = conn.cursor()
    sql = "SELECT EXISTS (SELECT 1 FROM {table_name} WHERE audioid = %s AND obtained_at = TO_DATE(%s, 'YYYY-MM-DD'));".format(table_name=whatsapp_audio_table)
    data = (audio_id, obtained_at)
    cursor.execute(sql, data)
    return cursor.fetchone()[0]


def update_nsfw_scores_on_database(conn, nsfw_scores):
    cursor = conn.cursor()
    sql = "UPDATE {table_name} SET nsfw_score=%s WHERE imageid=%s;".format(table_name=whatsapp_image_table)
    for imageID in nsfw_scores:
        try:
            data = (nsfw_scores[imageID], imageID)
            print (data)
            cursor.execute(sql, data)
        except Exception as e:
            print("update_nsfw_scores_on_database", str(e))
    conn.commit()


def insert_whatsapp_images_on_database(conn, images, nsfw_scores):
    print("\t\tWhatsapp: Inserting images on database: %d images" % len(images))
    cursor = conn.cursor()
    sql = "INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s, TO_DATE(%s, 'YYYY-MM-DD'), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(table_name=whatsapp_image_table)
    count = 0
    for image in images:
        if not is_image_on_database(conn=conn, image_id=image['mediaID'], obtained_at=image['date']):
            try:
                imageID 		  = image['mediaID']
                rankingDay 		  = count
                shareNumber 	  = image['shareNumber']
                shareNumberUsers  = image['shareNumberUsers']
                shareNumberGroups = image['shareNumberGroups']
                obtained_at 	  = image['date']
                nsfw_score 		  = 0
                shared_groups     = image['groups'] 
                shared_users      = image['users'] 
                checksum          = image["checksum"]
                phash             = image["phash"]
                fakeness          = 0.0    
                
                try:    context_pre = image["context_pre"]
                except: context_pre = []
                try:    context_now = image["context_now"]
                except: context_now = []
                try:    context_pos = image["context_pos"]
                except: context_pos = []
                
                data = (imageID, rankingDay, shareNumber, shareNumberUsers, shareNumberGroups, obtained_at, nsfw_score, shared_groups, shared_users, checksum, phash, fakeness, imageID, context_pre, context_pos, context_now)
                #print 'Inserting Image %s, checksum= %s, phash= %s. Shared %d times' %(imageID, checksum, phash, int(shareNumber) )
                cursor.execute(sql, data)
                count += 1
            except Exception as e:
                print("insert_whatsapp_images_on_database", str(e))
                # print(traceback.format_exc())
    conn.commit()
    print('\t\t>>> Total persisted images:', count)


def insert_whatsapp_stickers_on_database(conn, stickers, nsfw_scores):
    print("\t\tWhatsapp: Inserting stickers on database: %d images" % len(stickers))
    cursor = conn.cursor()
    sql = "INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s, TO_DATE(%s, 'YYYY-MM-DD'), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(table_name=whatsapp_sticker_table)
    count = 0
    for sticker in stickers:
        if not is_sticker_on_database(conn=conn, image_id=sticker['mediaID'], obtained_at=sticker['date']):
            try:
                imageID 		  = sticker['mediaID']
                rankingDay 		  = count
                shareNumber 	  = sticker['shareNumber']
                shareNumberUsers  = sticker['shareNumberUsers']
                shareNumberGroups = sticker['shareNumberGroups']
                obtained_at 	  = sticker['date']
                nsfw_score 		  = 0
                shared_groups     = sticker['groups'] 
                shared_users      = sticker['users'] 
                checksum          = sticker["checksum"]
                phash             = sticker["phash"]
                fakeness          = 0.0    
                
                try:    context_pre = []
                except: context_pre = []
                try:    context_now = sticker["context_now"]
                except: context_now = []
                try:    context_pos = []
                except: context_pos = []
                
                data = (imageID, rankingDay, shareNumber, shareNumberUsers, shareNumberGroups, obtained_at, nsfw_score, shared_groups, shared_users, checksum, phash, fakeness, imageID, context_pre, context_pos, context_now)
                #print 'Inserting sticker %s, checksum= %s, phash= %s. Shared %d times' %(imageID, checksum, phash, int(shareNumber) )
                cursor.execute(sql, data)
                count += 1
            except Exception as e:
                print("insert_whatsapp_stickers_on_database", str(e))
                # print(traceback.format_exc())
    conn.commit()
    print('\t\t>>> Total persisted Stickers:', count)


def insert_whatsapp_audios_on_database(conn, audios):
    print("\t\tWhatsapp: Inserting audios on database: %d audios" % len(audios))
    cursor = conn.cursor()
    sql = "INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s, TO_DATE(%s, 'YYYY-MM-DD'), %s::json, %s, %s, %s, %s, %s, %s, %s);".format(table_name=whatsapp_audio_table)
    count = 0
    dur ={
      "horas": 0, 
      "minutos": 0, 
      "segundos": 0
    }
    for audio in audios:
        if not is_audio_on_database(conn=conn, audio_id=audio['mediaID'], obtained_at=audio['date']):
            try:
                audioID 			= audio['mediaID']
                rankingDay 			= count
                shareNumber 		= audio['shareNumber']
                shareNumberUsers 	= audio['shareNumberUsers']
                shareNumberGroups   = audio['shareNumberGroups']
                obtained_at 		= audio['date']
                duration 			= json.dumps(dur)
                shared_groups     	= audio['groups'] 
                shared_users      	= audio['users'] 
                checksum            = audio['checksum']
                
                
                try:    context_pre = audio["context_pre"]
                except: context_pre = []
                try:    context_now = audio["context_now"]
                except: context_now = []
                try:    context_pos = audio["context_pos"]
                except: context_pos = []
                
                data = (audioID, rankingDay, shareNumber, shareNumberUsers, shareNumberGroups, obtained_at, duration, shared_groups, shared_users, checksum, audioID,  context_pre, context_pos, context_now)
                #print 'Inserting Audios %s, checksum %s. Shared %d times' %(audioID, checksum, int(shareNumber) )
                cursor.execute(sql, data)
                count += 1
            except Exception as e:
                print("insert_whatsapp_audios_on_database", str(e))
                print(traceback.format_exc())
    conn.commit()
    print('\t\t>>> Total persisted audios:', count)

def insert_whatsapp_links_on_database(conn, links):
    print("\t\tWhatsapp: Inserting links on database: %d links" % len(links))
    cursor = conn.cursor()
    sql = "INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s, TO_DATE(%s, 'YYYY-MM-DD'), %s, %s, %s, %s, %s, %s, %s, %s);".format(table_name=whatsapp_link_table)
    count = 0
    for link in links:
        try:
            link_             = link['mediaID']
            rankingDay        = count
            shareNumber       = link['shareNumber']
            shareNumberUsers  = link['shareNumberUsers']
            shareNumberGroups = link['shareNumberGroups']
            obtained_at       = link['date']              
            link_title        = link['title']
            link_description  = link['description']
            link_image        = link['image']
            link_author       = link['author']
            link_date         = link['linkDate']
            link_keywords     = link['keywords']
            shared_groups     = link['groups'] 
            shared_users      = link['users']
            
            data = (link_, rankingDay, shareNumber, shareNumberUsers, shareNumberGroups, obtained_at, link_title, link_description, link_image, link_author, link_date, link_keywords, shared_groups, shared_users)
            cursor.execute(sql, data)
            count += 1
        except Exception as e:
            print("insert_whatsapp_links_on_database", str(e))
            print(traceback.format_exc())
            break
    conn.commit()
    print('\t\t>>> Total persisted links:', count)
    

def insert_whatsapp_messages_on_database(conn, messages):
    print("\t\tWhatsapp: Inserting links on database: %d messages" % len(messages))
    cursor = conn.cursor()
    sql = "INSERT INTO {table_name} VALUES (%s, %s,  TO_DATE(%s, 'YYYY-MM-DD'), %s, %s, %s, %s, %s, %s);".format(table_name=whatsapp_message_table)
    count = 0

    for msg in messages:
        try:
            id                = msg['mediaID'] #OLD FORMAT: 'MessageID_'+str(count+1)+"_"+msg['date']+"_"+remove_special_caracter(msg['message'][:25])
            message_          = msg['message']
            rankingDay        = count
            shareNumber       = msg['shareNumber']
            shareNumberUsers  = msg['shareNumberUsers']
            shareNumberGroups = msg['shareNumberGroups']
            obtained_at       = msg['date']
            shared_groups     = msg['groups'] 
            shared_users      = msg['users']
            
            data = (id, message_, obtained_at, rankingDay, shareNumber, shareNumberUsers, shareNumberGroups, shared_groups, shared_users)
            #print ( "INSERT INTO whatsapp_message VALUES (%s,  TO_DATE(%s, 'YYYY-MM-DD'), %s, %s, %s, %s, %s, %s);\n\n" %(message_, obtained_at, rankingDay, shareNumber, shareNumberUsers, shareNumberGroups, shared_groups, shared_users))
            cursor.execute(sql, data)
            count += 1
        except ValueError as e:
            print("insert_whatsapp_messages_on_database", count,sql,  str(e))
            print(traceback.format_exc())
            continue  
        except Exception as e:
            print("insert_whatsapp_messages_on_database", count,  str(e))
            print(traceback.format_exc())
            break
    conn.commit()
    print('\t\t>>> Total persisted links:', count)
    

def insert_whatsapp_videos_on_database(conn, videos, nsfw_scores=[]):
    print("\t\tWhatsapp: Inserting videos on database: %d videos" % len(videos))
    cursor = conn.cursor()
    sql = "INSERT INTO {table_name} VALUES (%s, TO_DATE(%s, 'YYYY-MM-DD'), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(table_name=whatsapp_video_table)
    count = 0
    for video in videos:
        if not is_video_on_database(conn=conn, video_id=video['mediaID'], obtained_at=video['date']):
            try:
                videoID               = video['mediaID']
                rankingDay            = count
                shareNumber           = video['shareNumber']
                shareNumberUsers      = video['shareNumberUsers']
                shareNumberGroups     = video['shareNumberGroups']
                obtained_at           = video['date']
                shared_groups         = video['groups'] 
                shared_users          = video['users']
                checksum              = video['checksum']
                nsfw_score            = 0
                if len(nsfw_scores) > 0:
                    nsfw_score            = nsfw_scores[video['mediaID']]
                    
                try:    context_pre = video["context_pre"]
                except: context_pre = []
                try:    context_now = video["context_now"]
                except: context_now = []
                try:    context_pos = video["context_pos"]
                except: context_pos = []
                
                data = (videoID, obtained_at, rankingDay, shareNumber, shareNumberUsers, shareNumberGroups, shared_groups, shared_users, nsfw_score, checksum, videoID, context_pos, context_pre , context_now)
                #print 'Inserting Video %s, checksum %s. Shared %d times' %(videoID, checksum, int(shareNumber) )
                cursor.execute(sql, data)
                count += 1
            except Exception as e:
                print("insert_whatsapp_videos_on_database ", count,  str(e))
                # print(traceback.format_exc())
                break
    conn.commit()
    print('\t\t>>> Total persisted videos:', count)


def get_days_list(start_date, end_date):

    formatter = '%Y-%m-%d'
    
    date1 = datetime.strptime(start_date, formatter)
    date2 = datetime.strptime(end_date, formatter)
    delta = date2 - date1       # as timedelta

    dates_list = list()
    for i in range(delta.days + 1):
        day = date1 + timedelta(days=i)
        date_string = day.strftime(formatter)
        dates_list.append(date_string)

    return dates_list
   
    
    
    
'''
def export_data_from_database(conn):
    cursor = conn.cursor()
    sql = "SELECT user_id, user_json::json, bot_or_not::json, obtained_at FROM " + bot_or_not_users_table + ";"
    cursor.execute(sql)
    response = cursor.fetchall()
    response = map(lambda x: dict(zip(['user_id', 'user', 'bot_or_not', 'obtained_at'], x)), response)
    return response


def get_all_data_from_database(conn):
    cursor = conn.cursor()
    response = {}
    sql = "SELECT bot_or_not::json FROM " + bot_or_not_users_table + ";"
    cursor.execute(sql)
    response = cursor.fetchall()
    if response:
        response = map(lambda x: x[0], response)
    return response

'''
