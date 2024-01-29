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
from os.path import isfile, join
import sys
import os
 
whatsapp_audio_table = "whatsapp_audio"
whatsapp_image_table = "whatsapp_image"
whatsapp_link_table = "whatsapp_link"
whatsapp_message_table = "whatsapp_message"
whatsapp_video_table = "whatsapp_video"

db_host = "localhost"
db_name = "whatsapp"
db_user = "whomakestrends"
db_password = "678hjba!@1ABCUyvs8"


def get_table(media):

    if media == 'images' : return whatsapp_image_table
    elif media == 'videos' : return whatsapp_video_table
    elif media == 'audios' : return whatsapp_audio_table
    elif media == 'texts' : return whatsapp_message_table
    elif media == 'links' : return whatsapp_link_table
    return ''

    
def connect_app_database():
    conn_string = "host=%s dbname=%s user=%s password=%s"%(db_host, db_name, db_user, db_password)
    conn = psycopg2.connect(conn_string)
    return conn




def is_image_on_database(conn, image_id, obtained_at):
    cursor = conn.cursor()
    sql = "SELECT EXISTS (SELECT 1 FROM {table_name} WHERE imageid = %s AND obtained_at = TO_DATE(%s, 'YYYY-MM-DD'));".format(table_name=whatsapp_image_table)
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


def execute_command( cmd ):
    try:
        os.system(cmd)
    except Exception as error:
        print error.message

    
    
def copy_files(conn, media, mediaID, obtained_at, media_paths):
    table = get_table(media)
    
    cursor = conn.cursor()
    sql = "SELECT %s FROM %s WHERE obtained_at >= '%s' AND sharenumber >= 5  ORDER BY sharenumber DESC, sharenumberusers DESC, sharenumbergroups DESC;" %(mediaID, table, obtained_at)
    data = list()
    cursor.execute(sql, data)
    response = cursor.fetchall()
    response =  list(map(lambda x: {'imageid': x[0]}, response))
    for file in response:
        filename = file['imageid'].strip()
        for path in media_paths:
            if isfile(path+filename):
                
                cmd = 'cp -n %s /scratch1/data_whatsapp/%s/' %(path+filename, media)
                print cmd
                execute_command( cmd )

    return response


    
        
    
def update_files(conn, media, mediaID, method, media_paths, hash_reference_file):

    
    hash_reference = dict()
    with open(hash_reference_file, 'r') as fhash:
       for line in fhash:
        tokens = line.strip().split('\t')
        hash_reference[tokens[0]] = tokens[1] 
    
    table = get_table(media)
    
    cursor = conn.cursor()
    sql = "SELECT %s,%s FROM %s WHERE obtained_at >= '2020-03-01' AND sharenumber >= 2 ORDER BY sharenumber DESC, sharenumberusers DESC, sharenumbergroups DESC;" %(mediaID, method, table)
    data = list()
    cursor.execute(sql, data)
    response = cursor.fetchall()
    response =  list(map(lambda x: {'imageid': x[0], 'hash': x[1]}, response))
    for item in response:
        #print item
        filename = item['imageid']
        hash     = item['hash']
        try: new_file = hash_reference[hash] 
        except Exception as e:
            print 'ERROR', hash, e
            continue
        if filename == new_file: continue
        sql_update = "UPDATE %s SET %s = '%s', %s = '%s' WHERE %s = '%s'" %(table, mediaID, new_file, method, hash, mediaID, filename) 
        print sql_update
        cursor.execute(sql_update)
        conn.commit()

    return response


    
    
def main():
    media = (sys.argv[1])
    method = (sys.argv[2])
    mediapath = list()
    conn = connect_app_database()
    if media == 'images':
        mediaID = 'imageid'
        hash_reference_file = '/scratch1/whatsapp/DATA_HASHES/hashes/files_list_images_checksum.txt'
        mediapath.append('/scratch1/whatsapp/CRAWLER/politics_01/%s/' %(media))
        mediapath.append('/scratch1/whatsapp/CRAWLER/politics_02/%s/' %(media))
        mediapath.append('/scratch1/whatsapp/CRAWLER/politics_03/%s/' %(media))
        hash_methods = ['phash', 'checksum', 'pdq', 'ahash',  'dhash', 'whash-haar', 'whash-db4']
        hash_methods = ['checksum', 'phash']
        update_files(conn, media, mediaID, method, mediapath, hash_reference_file)
    elif media == 'videos':
        mediaID = 'videoid'
        hash_reference_file = '/scratch1/whatsapp/DATA_HASHES/hashes/files_list_videos_checksum.txt'
        mediapath.append('/scratch1/whatsapp/CRAWLER/politics_01/%s/' %(media))
        mediapath.append('/scratch1/whatsapp/CRAWLER/politics_02/%s/' %(media))
        mediapath.append('/scratch1/whatsapp/CRAWLER/politics_03/%s/' %(media))
        hash_methods = ['checksum']
        update_files(conn, media, mediaID, method, mediapath, hash_reference_file)
    elif media == 'audios':
        mediaID = 'audioid'
        hash_reference_file = '/scratch1/whatsapp/DATA_HASHES/hashes/files_list_audios_checksum.txt'
        mediapath.append('/scratch1/whatsapp/CRAWLER/politics_01/%s/' %(media))
        mediapath.append('/scratch1/whatsapp/CRAWLER/politics_02/%s/' %(media))
        mediapath.append('/scratch1/whatsapp/CRAWLER/politics_03/%s/' %(media))
        hash_methods = ['checksum']
        update_files(conn, media, mediaID, method, mediapath, hash_reference_file)
    else:
        print 'ERROR'


if __name__ == "__main__":
    main()
    exit()

    