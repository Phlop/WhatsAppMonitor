# -*- coding: utf-8 -*-
import os
import sys
import re
import random
import pathlib
import argparse
import json
import traceback
import hashlib
import imagehash
import pytz

import sqlite3
from importlib import import_module
from os import listdir
from os.path import isfile, join 
from pathlib import Path

from django.utils.encoding import smart_str
from django.utils.encoding import smart_unicode
from datetime import datetime
from datetime import date as DATE
from datetime import timedelta

import time

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen# import magic
from urllib import urlretrieve


import glob
import binascii
import base64
from axolotl.kdf.hkdfv3    import HKDFv3
from axolotl.util.byteutil import ByteUtil
from Crypto.Cipher import AES
import hashlib
import hmac
from PIL import Image
    
    

import phonenumbers
from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
    region_code_for_number,
)


#EXTERNAL SCRIPTS
import hash_functions as HASH


def string_to_bool(value):
    value = str(value)
    if (value.upper() == 'TRUE') or (value.upper() == 'T') or (value == '1'): 
        return True
    elif (value.upper() == 'FALSE') or (value.upper() == 'F') or (value == '0'): 
        return False
    elif (value.upper() == 'NONE'): 
        return False
    else:
        return True
    
    
class WhatsAppCrawler():
  
    def __init__(self, database_name, crawler_name='', phone=None, argsjson=None):
 
        self.crawler_name          = crawler_name
        self.phonenumber           = phone
        self.joined_groups         = set()
        self.database              = database_name
        self.data_path             = 'data/'
        self.user_blacklist        = set()
        self.group_blacklist       = set()
        self.start_date            = '2000-01-01'   
        self.end_date              = '2999-12-31'   
        self.ENCODING              = 'utf-8-sig'
        
        self.save_media            = True
        self.collect_audios        = True
        self.collect_videos        = False
        self.collect_images        = True
        self.collect_documents     = True
        self.collect_stickers      = True
        self.process_image_hashes  = True
        self.process_audio_hashes  = True
        self.process_video_hashes  = True
        self.process_document_hashes  = True
        self.process_sticker_hashes   = True
        self.all_media_types = ['image', 'audio', 'video', 'sticker', 'document']
            
        if argsjson:
            args_dict = vars(argsjson)
            print(args_dict)
            self.database          = args_dict['database']   
            self.save_media        = args_dict['save_media']   
            self.phonenumber       = args_dict['phone_number']   
            self.data_path         = args_dict['datalake']            
            self.files_path        = args_dict['file_path']            
            self.start_date        = args_dict['start_date']   
            self.end_date          = args_dict['end_date']   
            self.blacklist         = args_dict['group_blacklist']   
            self.whitelist         = args_dict['group_whitelist']   
            self.save_media        = args_dict['save_media'] 
            self.collect_audios    = args_dict['save_audios'] 
            self.collect_videos    = args_dict['save_videos'] 
            self.collect_images    = args_dict['save_images'] 
            self.collect_stickers  = args_dict['save_stickers'] 
            self.collect_documents = args_dict['save_documents']     
            
            self.process_hashes    = args_dict['process_hashes'] 
            self.hash_methods      = ['checksum', 'phash'] 
            if not string_to_bool(self.process_hashes): 
                self.process_image_hashes  = False
                self.process_audio_hashes  = False
                self.process_video_hashes  = False
                self.process_document_hashes  = False
                self.process_sticker_hashes   = False
            
            else:
                if self.collect_audios    : self.process_audio_hashes  = True
                if self.collect_videos    : self.process_video_hashes  = True
                if self.collect_images    : self.process_image_hashes  = True
                if self.collect_stickers  : self.process_sticker_hashes   = True
                if self.collect_documents : self.process_document_hashes  = True
                       
           
            if len(args_dict['filename_blacklist'])>3:
                self.load_blacklist(self, args_dict['filename_blacklist'])
            
            if len(args_dict['filename_whitelist'])>3:
                self.load_whitelist(self, args_dict['filename_blacklist'])
            
            if len(self.files_path) < 4:
                self.files_path = join(self.data_path, 'stored_files/')   
            
    def load_whitelist(self, filename):
        with open(filename, 'r') as fw:
            for line in fw:
                gid = line.strip().split()[0]
                gid = int(gid)
                self.whitelist.append(gid)
        
        if len(self.whitelist) > 0:
            print('Loading groups to whitelist (IDs to collect)')
            return True
        else:
            return False
    
    
    def load_blacklist(self, filename):
        with open(filename, 'r') as fb:
            for line in fb:
                gid = line.strip().split()[0]
                gid = int(gid)
                self.blacklist.append(gid)
        
        if len(self.blacklist) > 0:
            print('Loading groups to black list (not collected)')
            return True
        else:
            return False
    
    
    def setting_path(self):
        print('>>>SETTING UP DIRECTORIES TO DATA CRAWLER')
        # Create data directories
        if not self.data_path:
            self.data_path = 'data/'
        self.path_day   = self.data_path+"messages_per_day"
        self.path_api   = self.data_path+"messages_api_response"
        self.path_group = self.data_path+"messages_per_groups"
        
        if not self.files_path:
            self.files_path = self.data_path+"stored_files/"
        self.path_encrypted = self.files_path+"encrypted"
        self.path_images    = self.files_path+"images"
        self.path_audios    = self.files_path+"audios"
        self.path_videos    = self.files_path+"videos"
        self.path_stickers  = self.files_path+"stickers"
        self.path_documents = self.files_path+"documents"
        self.path_hashes = self.files_path+"hashes"
        self.path_notifications = self.files_path+"notifications"
        
        try:    pathlib.Path(self.data_path).mkdir(parents=True) 
        except: print('Path %s already created' %(self.data_path))
        try:    pathlib.Path(self.path_day).mkdir(parents=True)
        except: print('Path %s already created' %(self.path_day))
        try:    pathlib.Path(self.path_api).mkdir(parents=True)
        except: print('Path %s already created' %(self.path_api))
        try:    pathlib.Path(self.path_group).mkdir(parents=True)
        except: print('Path %s already created' %(self.path_group))
        try:    pathlib.Path(self.files_path).mkdir(parents=True)
        except: print('Path %s already created' %(self.files_path))
        try:    pathlib.Path(self.path_encrypted).mkdir(parents=True)
        except: print('Path %s already created' %(self.path_encrypted))
        try:    pathlib.Path(self.path_images).mkdir(parents=True)
        except: print('Path %s already created' %(self.path_images))
        try:    pathlib.Path(self.path_audios).mkdir(parents=True)
        except: print('Path %s already created' %(self.path_audios))
        try:    pathlib.Path(self.path_videos).mkdir(parents=True)
        except: print('Path %s already created' %(self.path_videos))
        try:    pathlib.Path(self.path_stickers).mkdir(parents=True)
        except: print('Path %s already created' %(self.path_stickers))
        try:    pathlib.Path(self.path_documents).mkdir(parents=True)
        except: print('Path %s already created' %(self.path_documents))
        try:    pathlib.Path(self.path_notifications).mkdir(parents=True)
        except: print('Path %s already created' %(self.path_notifications))
        try:    pathlib.Path(self.path_hashes).mkdir(parents=True)
        except: print('Path %s already created' %(self.path_hashes))
        
        return True
                
     

    
    def get_days_list(self, start_date, end_date):

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
 
    def list_filenames_by_date(self, start_date):        
        today = DATE.today().strftime('%Y-%m-%d')
        end_date = today
        dates = self.get_days_list(start_date, end_date)
        
        all_filenames = list()
        for date in dates:
            filename = 'AllMessages_%s.txt' %(date)
            if isfile(join(self.path_day, filename)):
                all_filenames.append(join(self.path_day, filename))
        return all_filenames
       
       
    def get_ids_from_files(self, all_hashes):
        
        print('>>> Reading all messages already collected before start new collection (AVOID DUPLICATES)'.upper())
        initial_date_ids = '2023-01-01'
        
        #Listing all files by group:
        #allfiles = [join(self.path_group, f) for f in listdir(self.path_group) if isfile(join(self.path_group, f))]
        
        #Listing all files by date:
        allfiles = self.list_filenames_by_date(initial_date_ids)
        
        total_messages = 0
        repeated_messages = 0
        all_messages = set()
        all_groups   = set()
        all_messages_dict   = dict()
        error = 0
        
        print('>>> LOADING  PREVIOUS IDS FROM %d GROUPS SINCE %s' %(len(allfiles), initial_date_ids) )
        for filename in allfiles:
            with open( filename, 'r') as fin:
                for line in fin:
                    try:   message = json.loads(line.strip())
                    except:
                        print(line)
                        continue
                        message = json.loads(line.strip())
                    message_id = message['message_id']
                    group_id   = message['group']['group_id']
                    msg_date   = message['date']
                    if msg_date < initial_date_ids: continue
                    
                    try: A = all_messages_dict[group_id]
                    except:  all_messages_dict[group_id] = set()
                    
                    #all_messages.append(message_id)
                    all_messages_dict[group_id].add(message_id)
                    all_groups.add(group_id)
                    total_messages += 1
                    try:
                        media_type = message['media']['media_type']
                        filename   = message['media']['stored_filename']
                        for method in message['media']['hashes']:
                            hash = message['media']['hashes'][method]
                            all_hashes[media_type][method][hash] = filename
                    except:
                        error += 1
                        
        print('Total of messages previously loaded:\t%d' %(total_messages) )
        print('Total of groups   previously loaded:\t%d' %(len(all_groups)) )
        return all_messages, all_groups, all_hashes, all_messages_dict     ##ALTERED ALL_MESAGES TO A DICT FOR EACH GROUP TO BE FASTER     

    def data_anonymization(self, data):
        if not data: return None
        anon_data = hashlib.md5(data.encode('utf-8')).hexdigest()
        return anon_data

    def  get_country_code(self, sender):
        try:    phone = phonenumbers.parse(sender)
        except: 
            try:
                phone = phonenumbers.parse('+'+sender)
            except:
                return None
        cc =  phone.country_code
        country = region_code_for_country_code(cc)
        return country
    
    def get_ddd_from_number(self, phone):
        if self.get_country_code(phone) == 'BR':
            state_codes = { 11:'SP', 12:'SP', 13:'SP', 14:'SP',
                            15:'SP', 16:'SP', 17:'SP', 18:'SP',
                            19:'SP', 21:'RJ', 22:'RJ', 24:'RJ',
                            27:'ES', 28:'ES', 31:'MG', 32:'MG',
                            33:'MG', 34:'MG', 35:'MG', 37:'MG',
                            38:'MG', 41:'PR', 42:'PR', 43:'PR',
                            44:'PR', 45:'PR', 46:'PR', 47:'SC',
                            48:'SC', 49:'SC', 51:'RS', 53:'RS',
                            54:'RS', 55:'RS', 61:'DF', 62:'GO',
                            63:'TO', 64:'GO', 65:'MT', 66:'MT',
                            67:'MS', 68:'AC', 69:'RO', 71:'BA',
                            73:'BA', 74:'BA', 75:'BA', 77:'BA',
                            79:'SE', 81:'PE', 82:'AL', 83:'PB',
                            84:'RN', 85:'CE', 86:'PI', 87:'PE',
                            88:'CE', 89:'PI', 91:'PA', 92:'AM',
                            93:'PA', 94:'PA', 95:'RR', 96:'AP',
                            97:'AM', 98:'MA', 99:'MA'}
            phone = phone.strip().replace(' ', '')
            phone = phone.replace('+','')
            phone = phone.replace('-','')
            ddd = int(phone[2:4])
            try:    state = state_codes[ddd]
            except: state = str(ddd)
            return ddd
        else: 
            return None
        
    def old_format_message(self, message):
        text_message =   message['text']  
        if  text_message:
            text_message = text_message.strip( )
            text_message = text_message.replace('\r','')
            text_message = text_message.replace('\n',' ')
            text_message = text_message.replace('\t',' ')
            #try : text_message = smart_str(text_message)
            try : text_message = smart_unicode(text_message)
            except : text_message = 'NoName'
        messageLine = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%r\t%s\t%s\t%s' %(message['message_id'], 
                                                                    message['group']['group_id'],
                                                                    message['group']['group_name'],
                                                                    message['country_code'], 
                                                                    message['sender'], 
                                                                    message['date'], 
                                                                    message['message_type'], 
                                                                    message['media']['mime_type'], 
                                                                    message['media']['stored_filename'], 
                                                                    str(message['forwarded']), 
                                                                    text_message
                                                                    )
        return messageLine
    
    def remove_file(self, filename):
        try:
            os.remove(filename)
            return True
        except:
            return False
    
    def md5(fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
     
    
    def is_media(self, message):
        if (message):
            return True
        else:
            return False
            
            
    def get_main_method(self, media_type):
        if media_type == 'image'   :   return 'phash'
        if media_type == 'video'   :   return 'checksum'
        if media_type == 'audio'   :   return 'checksum'
        if media_type == 'sticker' :   return 'phash'
        if media_type == 'document':   return 'checksum'
        return False
        
    def check_media_hashes(self, method, media_type):
        # CHECK IF HASH METHOD IS VALID FOR MEDIA TYPE
        audio_hashes     = ['checksum']
        video_hashes     = ['checksum']
        documents_hashes = ['checksum']
        image_hashes     = ['checksum', 'phash', 'ahash', 'dhash', 'whash-haar', 'whash-db4', 'pdq']   
        sticker_hashes   = ['checksum', 'phash', 'ahash', 'dhash', 'whash-haar', 'whash-db4', 'pdq']
        if media_type == 'image'   and method in image_hashes:    return True
        if media_type == 'video'   and method in video_hashes:    return True
        if media_type == 'audio'   and method in audio_hashes:    return True
        if media_type == 'sticker' and method in sticker_hashes:  return True
        if media_type == 'document'and method in documents_hashes:return True
        return False
            
    def is_collect_media(self, media_type):
        if media_type == 'image'   and self.collect_images:    return True
        if media_type == 'video'   and self.collect_videos:    return True
        if media_type == 'audio'   and self.collect_audios:    return True
        if media_type == 'sticker' and self.collect_stickers:  return True
        if media_type == 'document'and self.collect_documents: return True
        return False
    
    def is_hash(self, media_type):
        if media_type == 'image'   and self.process_image_hashes:    return True
        if media_type == 'video'   and self.process_video_hashes:    return True
        if media_type == 'audio'   and self.process_audio_hashes:    return True
        if media_type == 'sticker' and self.process_sticker_hashes:  return True
        if media_type == 'document'and self.process_document_hashes: return True
        return False

    def save_media_url_hash(self, media_url, media_type, hash, filename):
        hashes_filename = "mediaURL_%s.njson" %(media_type)
        fullname =  join(self.path_hashes, hashes_filename)
        
        if not os.path.isdir(self.path_hashes):
            os.makedirs(self.path_hashes)

        with open(fullname, 'a') as fout:
            new_line = "{}\t{}\t{}\n".format(media_url, hash, filename)
            fout.write(new_line)
    
    def load_media_url_hash(self):
        
        print('>>> Reading all media_URL already collected (AVOID DOWNLOAD DUPLICATED FILES)'.upper())
        media_url_dict = dict()
        for media_type in ['image', 'audio', 'sticker', 'video', 'document']:
            hashes_filename = "mediaURL_%s.njson" %(media_type)
            media_url_dict[media_type] = dict()
            fullname =  join(self.path_hashes, hashes_filename)
            if isfile(fullname): 
                with open(fullname, 'r') as fin:
                    for line in fin:
                        data = line.strip().split('\t')
                        media_url_dict[media_type][data[0]] = (data[1], data[2])
                
        return media_url_dict
        
    def replace_filename(self, original_filename, hash, method, media_type, all_hashes):
        final_file  = original_filename
        path        = self.get_path_location(media_type)
        
        if hash in  all_hashes[media_type][method]:
            replaced_file = all_hashes[media_type][method][hash]
            if original_filename != replaced_file:
                if isfile(join(path,replaced_file)):
                    print('HASH FOUND!!! FILE %s REPLACED TO %s' %(original_filename, replaced_file))
                    final_file = replaced_file
                    self.remove_file(join(path,original_filename))
        
        return final_file
    
    
    def get_hash_from_file(self, filename, media_type):
        path        = self.get_path_location(media_type)
        
        hash_dict   = dict()
        execute_hashes = list()
        for method in self.hash_methods:
            if self.check_media_hashes(method, media_type): 
                execute_hashes.append(method)
                hash_dict[method] = ''
                
        if isfile(join(path,filename)):
            for method in execute_hashes:
                hash = HASH.get_hash_from_method(join(path,filename), method)
                hash = str(hash)
                hash_dict[method] = hash
        
        return hash_dict



    def getCryptKeys(self, mediaType):
        if mediaType == "image":
            return '576861747341707020496d616765204b657973'
        if mediaType == "sticker":
            return '576861747341707020496d616765204b657973'
        if mediaType == "audio" or mediaType == "ptt":
            return '576861747341707020417564696f204b657973'
        if mediaType == "video":
            return '576861747341707020566964656f204b657973'
        if mediaType == "document" or mediaType == "application":
            return '576861747341707020446f63756d656e74204b657973'
        else:
            return '576861747341707020446f63756d656e74204b657973'
        return None

    def decrypt_media(self, encypted_filename, media_URL, MediaKey, output_filename, mediaType):
        try:
            CipherData = urlopen(media_URL).read()

            CipherImage = CipherData[:-10]
            cryptKeys   = self.getCryptKeys(mediaType)
            MediaKey64  =  base64.b64decode (MediaKey)
            MediaKey    = binascii.unhexlify(MediaKey)
            SecretsRaw  = HKDFv3().deriveSecrets(MediaKey, binascii.unhexlify(cryptKeys), 112)
            Secrets     = ByteUtil.split(SecretsRaw, 16, 32)
            iv          = Secrets[0]
            CipherKey   = Secrets[1]
            AES.key_size=128
            AESInstance = AES.new(key=CipherKey, mode=AES.MODE_CBC, IV=iv)
            Plain_MediaFile  = AESInstance.decrypt(CipherImage)

            with open(output_filename, 'wb') as f:
                f.write(Plain_MediaFile)
                f.close()
                
            return True    
        except:
            return False
    
    #deprecated
    def decrypt_alternative(self, encypted_file, url, refkey, filename, tipo = "image"): 
        encimg = urlopen(url).read( )
        cryptKeys = self.getCryptKeys(tipo) 
        refkey = base64.b64decode(refkey)
        print (cryptKeys, refkey)
        derivative = HKDFv3().deriveSecrets(refkey, binascii.unhexlify(cryptKeys), 112) 
        parts = ByteUtil.split(derivative, 16, 32) 
        iv = parts[0] 
        cipherKey = parts[1] 
        e_img = encimg[:-10]
        AES.key_size = 128
        cr_obj = AES.new(key=cipherKey, mode=AES.MODE_CBC, IV=iv) 
        PlainImage = cr_obj.decrypt(e_img)
        with open(filename, 'wb') as f:
            f.write(PlainImage)
            f.close()
        return cr_obj.decrypt(e_img)

        
    def get_media_extension(self, mime_type):
        if not mime_type:
            return 'text', 'txt'
        elif mime_type ==  u'image/jpeg':
            return 'image', 'jpeg'
        elif mime_type ==  u'image/webp':
            return 'sticker', 'webp'
        elif mime_type ==  u'audio/mpeg':
            return 'audio', 'mp3'
        elif mime_type ==  u'audio/ogg; codecs=opus':
            return 'audio', 'mp3'
        elif 'ptt' in mime_type:
            return 'audio', 'ogg'
        elif mime_type ==  u'audio/mp4':
            return 'video', 'mp4'
        elif mime_type ==  u'video/mp4':
            return 'video', 'mp4'
        elif mime_type ==  u'application/pdf':
            return 'document', 'pdf'
        else:
            return 'other', 'unk'

    def get_path_location(self, media_type):
        if media_type == 'image':   return self.path_images
        if media_type == 'audio':   return self.path_audios
        if media_type == 'video':   return self.path_videos
        if media_type == 'sticker': return self.path_stickers
        else:
            return self.path_documents
    
    
    def create_media_filename(self, media_url, mime_type):
        media_type, extension = self.get_media_extension(mime_type)
        filename = media_url.split("?")[0]
        filename = filename.split("/")[-1]
        filename = filename.strip()
        filename = filename.replace(' ','_')
        filename = filename.split(".")[0]
        
        # Normalize o nome do arquivo para remover caracteres inválidos
        filename = Path(filename).with_suffix("."+extension)
        filename = filename.name
        
        return filename
        
        
    def get_encrypted_filename(self, media_url):
        filename = media_url.split("?")[0]
        filename = filename.split("/")[-1]
        filename = filename.strip()
        filename = filename.replace(' ','_')
        filename = filename.split(".")[0]
        
        # Normalize o nome do arquivo para remover caracteres inválidos
        filename = Path(filename).with_suffix(".enc")
        filename = filename.name
        
        return filename
        
    
    def download_media_file(self, media_url, mime_type, media_key ):
        media_type, extension = self.get_media_extension(mime_type)
        encrypted_path        = self.path_encrypted
        download_path         = self.get_path_location(media_type)
        encrypted_filename    = self.get_encrypted_filename(media_url)
        media_final_filename  = self.create_media_filename(media_url, mime_type)
        output_filename       = join(download_path,media_final_filename)
        
        if isfile(output_filename) : 
            #MEDIA FILE ALREADY DOWNLOAD
            print('MEDIA FILE ALREADY DOWNLOADED')
            return media_final_filename
        else:
            #print(">>> DOWNLOAD ENCRYPTED FILE")
            fullpath_encypted_filename = join(encrypted_path,encrypted_filename)
            #urlretrieve(media_url, fullpath_encypted_filename)
            print("DECRYPTING FILE")
            downloaded = self.decrypt_media(fullpath_encypted_filename, media_url, media_key, output_filename, media_type)
            if not downloaded:
                print('File %s couldnt be downloaded and decrypted' %(output_filename))
            
            #print("REMOVE ENC FILE")
            if isfile(fullpath_encypted_filename): 
                self.remove_file(fullpath_encypted_filename)
            return media_final_filename
        

    def get_group_creator(self, jid, group_ids):

            if jid:
                groupID = group_ids[jid]
                tokens = groupID.split('-')
                if len(tokens) == 1: return None
                creator   = tokens[0]
                timestamp = tokens[1]
                return creator
            else:    
                return None
            
    def convert_timestamp_to_date(self, timestamp):
        try:
            if not timestamp: return None
            ts = int(timestamp/1000)
            datetime_t   = datetime.utcfromtimestamp(ts)
            datetime_str = datetime_t.strftime('%Y-%m-%d %H:%M:%S')
            return datetime_str
        except:
            return None
        
    def convert_date_to_timestamp(self, date):
        date_format = '%Y-%m-%d %H:%M:%S'
        if not date: return None
        try:    date_ts = datetime.strptime(date, date_format)
        except: date_ts = datetime.strptime(date+' 00:00:00', date_format)
        
        timestamp = time.mktime(date_ts.timetuple())
        timestamp = int(timestamp)*1000
        return timestamp
    
    def get_all_jids(self, cursor):
        sql_groups_query = 'SELECT _id,user FROM jid'
        cursor.execute(sql_groups_query);
        response  = cursor.fetchall()
        jids = list(   map( lambda x:{ 'id':x[0],  'jid':x[1]},  response)  )
        groups_ids = dict()
        for j in jids:
            groups_ids[j['id']] = j['jid']
        return groups_ids
        
    def sql_query_messages(self):
        #CREATE TABLE message (_id INTEGER PRIMARY KEY AUTOINCREMENT, chat_row_id INTEGER NOT NULL, from_me INTEGER NOT NULL, key_id TEXT NOT NULL, sender_jid_row_id INTEGER, status INTEGER, broadcast INTEGER, recipient_count INTEGER, participant_hash TEXT, origination_flags INTEGER, origin INTEGER, timestamp INTEGER, received_timestamp INTEGER, receipt_server_timestamp INTEGER, message_type INTEGER, text_data TEXT, starred INTEGER, lookup_tables INTEGER, message_add_on_flags INTEGER, sort_id INTEGER NOT NULL DEFAULT 0 )
        
        #CREATE TABLE chat (_id INTEGER PRIMARY KEY AUTOINCREMENT,jid_row_id INTEGER UNIQUE,hidden INTEGER,subject TEXT,created_timestamp INTEGER,display_message_row_id INTEGER,last_message_row_id INTEGER,last_read_message_row_id INTEGER,last_read_receipt_sent_message_row_id INTEGER,last_important_message_row_id INTEGER,archived INTEGER,sort_timestamp INTEGER,mod_tag INTEGER,gen REAL,spam_detection INTEGER,unseen_earliest_message_received_time INTEGER,unseen_message_count INTEGER,unseen_missed_calls_count INTEGER,unseen_row_count INTEGER,plaintext_disabled INTEGER,vcard_ui_dismissed INTEGER,change_number_notified_message_row_id INTEGER,show_group_description INTEGER,ephemeral_expiration INTEGER,last_read_ephemeral_message_row_id INTEGER,ephemeral_setting_timestamp INTEGER,ephemeral_disappearing_messages_initiator INTEGER,unseen_important_message_count INTEGER NOT NULL DEFAULT 0,group_type INTEGER NOT NULL DEFAULT 0, last_message_reaction_row_id INTEGER, last_seen_message_reaction_row_id INTEGER, unseen_message_reaction_count INTEGER, growth_lock_level INTEGER, growth_lock_expiration_ts INTEGER, last_read_message_sort_id INTEGER, display_message_sort_id INTEGER, last_message_sort_id INTEGER, last_read_receipt_sent_message_sort_id INTEGER )
        
        #CREATE TABLE jid (_id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT NOT NULL, server TEXT NOT NULL, agent INTEGER, device INTEGER, type INTEGER, raw_string TEXT)
        
        #CREATE TABLE message_forwarded(message_row_id INTEGER PRIMARY KEY, forward_score INTEGER)
        
        #CREATE TABLE message_media (message_row_id INTEGER PRIMARY KEY, chat_row_id INTEGER, autotransfer_retry_enabled INTEGER, multicast_id TEXT, media_job_uuid TEXT, transferred INTEGER, transcoded INTEGER, file_path TEXT, file_size INTEGER, suspicious_content INTEGER, trim_from INTEGER, trim_to INTEGER, face_x INTEGER, face_y INTEGER, media_key BLOB, media_key_timestamp INTEGER, width INTEGER, height INTEGER, has_streaming_sidecar INTEGER, gif_attribution INTEGER, thumbnail_height_width_ratio REAL, direct_path TEXT, first_scan_sidecar BLOB, first_scan_length INTEGER, message_url TEXT, mime_type TEXT, file_length INTEGER, media_name TEXT, file_hash TEXT, media_duration INTEGER, page_count INTEGER, enc_file_hash TEXT, partial_media_hash TEXT, partial_media_enc_hash TEXT, is_animated_sticker INTEGER, original_file_hash TEXT, mute_video INTEGER DEFAULT 0)
        
        #CREATE TABLE message_ephemeral(message_row_id INTEGER PRIMARY KEY, duration INTEGER NOT NULL, expire_timestamp INTEGER NOT NULL, keep_in_chat INTEGER NOT NULL DEFAULT 0)
        
        start_timestamp = self.convert_date_to_timestamp(self.start_date)
        end_timestamp   = self.convert_date_to_timestamp(self.end_date)
        
        print('Start Date', self.start_date, start_timestamp)
        print('End Date',   self.end_date,   end_timestamp)
        
        query = ''' SELECT
            m.chat_row_id,
            m.key_id,
            m.sender_jid_row_id,
            m.timestamp,
            m.text_data,
            m.message_type,
            c.subject,
            c.created_timestamp,
            c.jid_row_id,
            u.user,
            f.forward_score,
            hex(media.media_key),
            media.media_key_timestamp,
            media.width,
            media.height,
            media.direct_path,
            media.message_url,
            media.mime_type,
            media.media_name,
            media.file_path,
            media.file_length,
            media.file_hash,
            media.enc_file_hash,
            media.partial_media_hash,
            media.suspicious_content,
            expire.duration,
            expire.expire_timestamp,
            q.key_id,
            c.ephemeral_expiration
            
        FROM 
            message AS m
        LEFT JOIN chat  AS c
            ON m.chat_row_id = c._id
        LEFT JOIN jid AS  u
            ON u._id = m.sender_jid_row_id
        LEFT JOIN message_quoted AS  q
            ON q.message_row_id = m._id
        LEFT JOIN message_forwarded AS  f
            ON f.message_row_id = m._id
        LEFT JOIN message_ephemeral AS  expire
            ON expire.message_row_id = m._id
        LEFT JOIN message_media AS  media
            ON media.message_row_id = m._id
            
        WHERE
            m.timestamp >= %d AND m.timestamp <= %d
        ''' %(start_timestamp, end_timestamp)

        #query = 'SELECT chat_row_id,text_data FROM message'
        return query

    def  map_messages_results(self, response, group_ids):
        result = list(
                    map(
                        lambda x: {
                                'row_id':       x[0], 
                                'message_id':   x[1],
                                'sender_id':    x[2],
                                'timestamp':    x[3],
                                'date':         self.convert_timestamp_to_date(x[3]),
                                'text':         x[4],
                                'message_type': x[5],
                                'group':{
                                    'group_name':      x[6],
                                    'group_timestamp': x[7],
                                    'group_date':      self.convert_timestamp_to_date(x[7]),
                                    'group_jid':       x[8],
                                    'group_id':        self.data_anonymization( group_ids[x[8]]) if(x[8]) else None,
                                    'ephemeral':       x[28],
                                    'group_country':   self.get_country_code(   self.get_group_creator(x[8], group_ids)),
                                    'group_ddd':       self.get_ddd_from_number(self.get_group_creator(x[8], group_ids)),
                                    'group_creator':   self.data_anonymization( self.get_group_creator(x[8], group_ids))
                                },
                                'sender': self.data_anonymization(x[9]),
                                'forwarded': x[10],
                                'media':{
                                    'media_key':     x[11],
                                    'media_key_timestamp': x[12],
                                    'media_key_date': self.convert_timestamp_to_date(x[12]),
                                    'width':         x[13],
                                    'height':        x[14],
                                    'direct_path':   x[15],
                                    'message_url':   x[16],
                                    'mime_type':     x[17],
                                    'media_type':    self.get_media_extension(x[17])[0],
                                    'media_name':    x[18],
                                    'file_path':     x[19],
                                    'file_length':   x[20],
                                    'file_hash':     x[21],
                                    'enc_file_hash': x[22],
                                    'partial_media_hash': x[23],
                                    'suspicious_content': x[24],
                                    'stored_filename': None,
                                    'hashes':{
                                        'checksum':    None,
                                        'phash':       None
                                    }
                                },
                                'message_duration': x[25],
                                'expire_timestamp': x[26],
                                'expire_date':     self.convert_timestamp_to_date(x[26]),
                                'ddd_code':        self.get_ddd_from_number(x[9]),
                                'country_code':    self.get_country_code(x[9]),
                                'is_quote': True if(x[27]) else False,
                                'quote': x[27]
                                }, 
                        response
                        )
                    )
                    
        return result


    def save_message(self, message):
        group_filename = message['group']['group_id'] + '.njson'
        group_filename = join(self.path_group, group_filename)
        
        day_filename =  "AllMessages_" + message['date'].split()[0] + ".txt"  
        day_filename = join(self.path_day, day_filename)    
        
        
        with open(group_filename, "a") as json_file_group:
            json.dump(message, json_file_group)
            print >> json_file_group, ""
            
        with open(day_filename, "a") as json_file_day:
            json.dump(message, json_file_day)
            print >> json_file_day, ""
         
        return True
        
    def collect_messages(self):
        
        print('>>>GETTING DATA FROM DATABASE %s' %(self.database.upper()))
        db_filename = self.database
        conn = sqlite3.connect(db_filename);
        c = conn.cursor();
        sql_query = self.sql_query_messages()
        print(sql_query)
        c.execute(sql_query);
        response  = c.fetchall()
        group_ids = self.get_all_jids(c)
        all_rows = self.map_messages_results(response, group_ids)
        
        print('Total messages rows = %d' %(len(all_rows)))
        
        all_hashes = dict()
        for media_type in self.all_media_types:
            all_hashes[media_type] = dict()
            for method in self.hash_methods:
                all_hashes[media_type][method] = dict()
        
        
        previous_ids, previous_groups, all_hashes, previous_ids_dict = self.get_ids_from_files(all_hashes)
        all_mediaURLs = self.load_media_url_hash( )
        check_group_w = False
        check_group_b = False
        rev = False
        if len(self.whitelist) > 0: check_group_w = True
        if len(self.blacklist) > 0: check_group_b = True
        
        print('>>>PROCESSING ALL MESSAGES')
        MAX = 99900000
        i = 0
        total_media = 0
        total_messages = 0
        
        for message in all_rows:
            total_messages += 1
            if (not message['group']['group_id']): 
                # NOT A GROUP MESSAGE
                continue
            
            if (not message['message_id']) or (not message['sender']) or (not message['date']) : continue
            message_id = message['message_id']
            sender     = message['sender']
            group_id   = message['group']['group_id']
            group_name = message['group']['group_name']
            date       = message['date'].split()[0]
            

            # Checking requisites of messages
            if date <  self.start_date: continue
            if date >  self.end_date:   continue
            #if str(message_id) in previous_ids:   Altered to a dict to be faster
            if group_id in previous_ids_dict.keys():
                if str(message_id) in previous_ids_dict[group_id]: 
                    print('%d -> Message %s in group %s already collected' %(total_messages, message_id, group_name))
                    continue
            
            if check_group_w and (group_id not in self.whitelist):
                if check_group_w and (group_name not in self.whitelist):
                    print('Group',group_id, str(group_name), 'not in whitelist!!!')
                    continue
            if check_group_b and (group_id in self.blacklist or group_name in self.blacklist):
                print('Group',group_id, str(group_name), 'in blacklist!!! Next group')
                continue
            
            
            i += 1
            if i > MAX: break
            
            if message['media']['message_url']:
                total_media += 1
                    
                media_url =  message['media']['message_url']
                mime_type =  message['media']['mime_type']
                media_key =  message['media']['media_key']
                media_type = message['media']['media_type']
                try:
                    if media_url not in all_mediaURLs[media_type]: 
                    
                        if self.is_collect_media(media_type):
                            stored_filename = self.download_media_file(media_url, mime_type, media_key )
                            if self.is_hash(media_type):
                                hashes_dict =  self.get_hash_from_file(stored_filename, media_type)
                                main_method = self.get_main_method(media_type)
                                
                                for method in hashes_dict.keys():
                                    hash  = hashes_dict[method]
                                    message['media']['hashes'][method]   = hash
                                    new_filename = self.replace_filename(stored_filename, hash, method, media_type, all_hashes)
                                    all_hashes[media_type][method][hash] = new_filename
                                    if method == main_method:  
                                        main_file = new_filename
                                message['media']['stored_filename'] = main_file
                                self.save_media_url_hash(media_url, media_type, hash, main_file)
                                all_mediaURLs[media_type][media_url] = (hash, main_file)
                    else: #means that media_URL was previously colected in another message
                    
                        method = self.get_main_method(media_type)
                        message['media']['hashes'][method]   = all_mediaURLs[media_type][media_url][0]
                        message['media']['stored_filename']  = all_mediaURLs[media_type][media_url][1]
                except:
                    print "UNKOWN MEDIA TYPE FOUND: ", media_type
    
            
            message_string = self.old_format_message(message)
            print(message_string)
            self.save_message(message)
            
            #if message['expire_date']:
            #     print('Message Date:', message['date'], '/t/Expire Date:', message['expire_date'])
            #    print(message)
           

        
        print("FINISHED DATA COLLECTION FOR MESSAGES")   
        print('Total Stickers:', total_media)
        #keydict = get_media_keys_from_db(name)
        #groups  = get_groups_name(name, c)
        #process_database(name, c, keydict, groups)


    
        
        
        


def main():
        #USEFUL LINKS
        #https://blog.group-ib.com/whatsapp_forensic_artifacts
        #https://towardsdatascience.com/analyzing-my-whatsapp-database-using-sql-and-redash-5ef9bd6a0b0
        #https://medium.com/@Med1um1/extracting-whatsapp-messages-from-backups-with-code-examples-49186de94ab4
        #https://blog.erratasec.com/2020/01/how-to-decrypt-whatsapp-end-to-end.html#.YpUBcMPMKUl
        #https://mazzo.li/posts/whatsapp-backup.html
        
        #GITHUBS
        #https://github.com/tgalal/yowsup/issues/2235
        #Whatsapp Api Python 3 -- https://github.com/wictorChaves/WhatsappApiPython3/blob/master/Decrypter.py
        #WEBWHATSAPI --           https://github.com/mukulhase/WebWhatsapp-Wrapper/blob/master/webwhatsapi/js/wapi.js
        # Kiran  --               https://github.com/gvrkiran/whatsapp-public-groups
        # https://github.com/ddz/whatsapp-media-decrypt
        crawler = 'whatsapp_crawler'
        phone   = '+55319000000'
        database_name = 'msgstore.db'
        

        parser = argparse.ArgumentParser()

        parser.add_argument("--phone_number", type=str,
                            help="Phone number of Telegram account", 
                            default=phone)

        parser.add_argument("--crawler_name", type=str,
                            help="Give a name for the crawler being set", 
                            default= 'whatsapp_crawler')
                            
        parser.add_argument("--database", type=str, required=True,
                            help="File of database of WhatsApp data", 
                            default='msgstore.db')

        parser.add_argument("--datalake", type=str,
                            help="Location (path) to save all data collected",
                            default='data/')
                                
        parser.add_argument("--file_path", type=str,
                            help="Location (path) to save all data collected",
                            default='')
                                
        parser.add_argument("-s", "--start_date", type=str,
                            help="start period of collection YYYY-MM-DD",
                            default='1990-01-01')
        
        parser.add_argument("-e", "--end_date", type=str,
                            help="End period of collection YYYY-MM-DD",
                            default='2999-12-31')

        parser.add_argument("-m", "--save_media", default=True, action="store_true",
                        help="Save media files from messages")
                        
        parser.add_argument("--save_images", default=True, action="store_true",
                        help="Download and store images files from messages")
        parser.add_argument("--skip_images", dest='save_images', action="store_false",
                        help="Skip and DONT STORE images files from messages")
                        
        parser.add_argument("--save_videos", default=True, action="store_true",
                        help="Download and store videos files from messages")
        parser.add_argument("--skip_videos", dest='save_videos', action="store_false",
                        help="Skip and DONT STORE videos files from messages")
                        
        parser.add_argument("--save_audios", default=True, action="store_true",
                        help="Download and store audios files from messages")
        parser.add_argument("--skip_audios", dest='save_audios', action="store_false",
                        help="Skip and DONT STORE audios files from messages")

        parser.add_argument("--save_stickers", default=True, action="store_true",
                        help="Download and store stickers files from messages")
        parser.add_argument("--skip_stickers", dest='save_stickers', action="store_false",
                        help="Skip and DONT STORE stickers files from messages")
                        
        parser.add_argument("--save_documents", default=True, action="store_true",
                        help="Download and store documents files from messages")
        parser.add_argument("--skip_documents", dest='save_documents', action="store_false",
                        help="Skip and DONT STORE documents files from messages")
        
        parser.add_argument("-p", "--process_hashes", type=str,
                        help="Process hash for downloaded files",
                        default='phash')
         
        parser.add_argument("--group_blacklist", nargs="+",
                        help="List of groups that should not be collected",
                        default=[])

        parser.add_argument("--group_whitelist", nargs="+",
                        help="List of groups that should be collected ",
                        default=[])
                        
        parser.add_argument("--filename_blacklist", type=str,
                        help="File with a list of groups that should not be collected",
                        default='')

        parser.add_argument("--filename_whitelist", type=str,
                        help="File with a list of groups that should be collected ",
                        default='')
                        
        
        
        args = parser.parse_args()
        
        
        collector = WhatsAppCrawler(database_name, crawler_name=crawler, phone=phone, argsjson=args)
        collector.setting_path( )
        collector.collect_messages( )
        

if __name__ == '__main__':
    
    #python whatsapp_crawler.py --database /home/user/Documents/ic/data/msgstore-2024-01-09.db --datalake /home/user/Documents/ic/data/msgstore-2024-01-09.db
    #python whatsapp_crawler.py --database /scratch4/whatsapp/root/Politics02/msgstore_2022_06_06.db --datalake /scratch4/whatsapp/DATABASE_CRAWLER/ -s 2022-05-01 -e 2023-12-31
    #python whatsapp_crawler.py --database /scratch4/whatsapp/root/Politics03/msgstore_2022_06_06.db --datalake /scratch4/whatsapp/DATABASE_CRAWLER/ -s 2022-05-01 -e 2023-12-31
    #python whatsapp_crawler.py --database /scratch4/whatsapp/root/Politics02/msgstore.db --datalake /scratch4/whatsapp/root/Politics02/data/ -s 2022-05-01 -e 2023-12-31
    main()
