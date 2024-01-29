# -*- coding: utf-8 -*-
__author__ = "Philipe Melo"
__email__ = "philipe@dcc.ufmg.br"


import json
import gzip
import pytz
import traceback
import psycopg2
from unicodedata import normalize
from collections import OrderedDict


import imagehash
import hash_functions as HASH

import sys
import os
import  re
import time
import hashlib
import imagehash
import imghdr
from PIL import Image    
from os import listdir
from os.path import isfile, join

from importlib import import_module
from django.utils.encoding import smart_str, smart_unicode
from datetime import date as DATE
from datetime import timedelta
from datetime import datetime


def jaccard_similarity(x,y):
    try: 
        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))
        return intersection_cardinality/float(union_cardinality)
    except ZeroDivisionError:
        return 0

def compare_texts(text1, text2):
    if text1 is None or text2 is None: return 0.0
    bow_text1 = text1.split()
    bow_text2 = text2.split()
    score = jaccard_similarity(bow_text1, bow_text2)
    return score


def convert_messages_to_json(messages, media, date):

    filename = './JSONS/jsons_%ss/all_%s_%s.json' %(media, media, date)
    with open(filename, 'w') as json_file:
        msg_json = json.dumps(messages, json_file)

  

def get_time_difference(d1, d2):
    
    format = "%Y-%m-%d %H:%M:%S"
    date_1 = datetime.strptime(d1, format)
    date_2 = datetime.strptime(d2, format)
    
    time_delta = (date_2 - date_1)
    total_seconds = time_delta.total_seconds()
    minutes = total_seconds/60
    return minutes

def load_list(media, method):
    hash_list = dict
    with open('../DATA_HASHES/hashes/files_list_%ss_%s.txt'%(media, method), 'r') as fhash:
        for line in fhash:
            tks = line.strip().split('\t')
            hash_list[tks[0]] = tks[1] 
    return hash_list




def load_hashes(media, hash_methods):
    print '>>> LOADING HASHES DICT'
    hashes = dict()
    for method in hash_methods:
        hashes[method] = dict()
        print method
        if isfile('../DATA_HASHES/hashes/%ss/%s.txt'%(media, method)):
            with open('../DATA_HASHES/hashes/%ss/%s.txt'%(media, method), 'r') as fhash:
                try:
                    for line in fhash:
                        tokens = line.strip().split('\t')
                        hash     = tokens[0]
                        total    = tokens[1]
                        filename = tokens[2]
                        hashes[method][hash] = list()
                        for filename in tokens[2:]: 
                            #filename = "%s.%s" %(filename.split('_')[1], filename.split('.')[-1])
                            hashes[method][hash].append(filename)
                except: continue
    return hashes






def load_files_list(media, hash_methods):
    print '>>> LOADING %s FILES DICT CONTAINING HASHES' %(media.upper())
    images = dict()
    
    total = 0
    if isfile('../DATA_HASHES/hashes/hashes_%ss_files.txt'%(media)):
        with open('../DATA_HASHES/hashes/hashes_%ss_files.txt'%(media), 'r') as fhash:
                for line in fhash:
                    #print line
                    tokens = line.strip().split('\t')
                    filename = tokens[0]
                    #filename = "%s.%s" %(filename.split('_')[1], filename.split('.')[-1])
                    images[filename] = dict()
                    total += 1
                    for i in range (1, len(tokens)): 
                        method = hash_methods[i-1]
                        hash   = tokens[i]
                        images[filename][method] = hash
    print("Total %s files %d" %(media, total))
    return images


    
def recover_hash(message, method, hash_methods):

    hashString = ''
    try:   
        hashString = message["media"]["hashes"][method]
    except:
        raise Exception('Error getting hash')
    return hashString


def get_date_filename(date):
    return 'AllMessages_%s.txt' %(date)


def process_url_day(media, media_paths, date):
    
    urls = dict()
    
    messages = dict()
    for path in media_paths:
        json_filename=get_date_filename(date)
        if not isfile(path+json_filename): continue
        print(path, json_filename)
                
        with open(path+json_filename, 'r') as fdata:
            for line in fdata:
                print(line)
                tokens  = line.strip().split('\t')
                msgID   = tokens[0]
                gID     = tokens[1]
                gName   = smart_str(tokens[2])
                country = tokens[3]
                user    = tokens[4]
                pdate    = tokens[5]
                phour    = tokens[6]
                kind    = tokens[7]
                isMedia = tokens[8]
                filename = tokens[9]
                try: text = smart_str(tokens[10])
                except: text = ''
                ptime = pdate+' '+phour
                #print media, kind, isMedia
                if media == 'url' and kind== 'text':
                    if len(text) < 50: continue
                    isNew = True
                    hashstring = msgID
                    for ID in messages.keys():
                        text2 = messages[ID]['message']
                        score = compare_texts(text, text2)
                        if score >= 0.75:
                            isNew = False
                            hashstring = ID
                            break
                    
                    if isNew:
                        messages[hashstring] = dict()
                        messages[hashstring]['hash'] = hashstring
                        messages[hashstring]['message'] = smart_str(text)
                        messages[hashstring]['mediaID'] = hashstring
                        messages[hashstring]['date'] = pdate
                        messages[hashstring]['kind'] = kind
                        messages[hashstring]['isMedia'] = (isMedia.lower() == 'true')
                        messages[hashstring]['shares'] = list()
                        messages[hashstring]['users'] = list()
                        messages[hashstring]['groups'] = list()
                        messages[hashstring]['shareNumber'] = 0
                        messages[hashstring]['shareNumberGroups'] = 0
                        messages[hashstring]['shareNumberUsers'] = 0
                        
                   
               
                    if user not in messages[hashstring]['users']: messages[hashstring]['users'].append(user)
                    if gName not in messages[hashstring]['groups']: messages[hashstring]['groups'].append(gName)
                    messages[hashstring]['shareNumber'] += 1
                    messages[hashstring]['shareNumberGroups'] = len(messages[hashstring]['users'])
                    messages[hashstring]['shareNumberUsers']  = len(messages[hashstring]['groups'])     
                    if ptime < messages[hashstring]['date']: messages[hashstring]['date'] = ptime 
                    share = dict()
                    share['user'] = user
                    share['groupID'] = gID
                    share['title'] = gName
                    share['time'] = ptime
                    share['filename'] = '<No_file>'
                    share['text'] = text
                    messages[hashstring]['shares'].append(share)
                    

    for k in messages.keys():
        print k, messages[k]['shareNumber'] 
        
    filename = './JSONS/jsons_%ss/all_%s_%s.json' %(media, media, date)
    with open(filename, 'w') as json_file:
        #js = json.dumps(messages)
        json.dump(messages, json_file, ensure_ascii=False, indent=4)
    
    return messages
    

def get_isMedia(message):
    message_type  = message["message_type"]
    if   message_type == 1: return True
    elif message_type == 2: return True
    elif message_type == 3: return True
    elif message_type == 9: return True
    elif message_type == 20: return True
    else:
        return False


def process_data_day(media, media_paths, method, hash_methods, date):
    medias = dict()
    hashes = dict()
    
    #medias = load_files_list(media, hash_methods)
    #hashes = load_hashes(media, hash_methods)
    
    #for k in hashes.keys(): print k, hashes[k]
    #for k in medias.keys(): print k, medias[k]
      
    messages = dict()
    message_now = dict()
    message_pre = dict()
    message_pos = dict()
    
    total_msgs = 0
    for path in media_paths:
        json_filename=get_date_filename(date)
        if not isfile(path+json_filename): continue
        with open(path+json_filename, 'r') as fdata:
            message_now = dict()
            message_pre = dict()
            message_pos = dict()
            lines = 0
            for line in fdata:
                lines += 1
                try:    this_message = json.loads(line.strip())
                except: 
                       print("Error loading line %d"%(lines))
                       print(line)
                       this_message = json.loads(line.strip())
                if this_message['text']: this_message['text'] = smart_str(this_message['text'])
                if this_message['group']['group_name']: this_message['group']['group_name']  = smart_str(this_message['group']['group_name'])

                #UPDATE MESSAGES IN ORDER TO GET CONTEXT FROM NEXT AND PREVIOUS MESSAGES
                message_pre = message_now
                message_now = message_pos
                message_pos = this_message 
                
                try:
                    msgID    = message_now['message_id']
                    gID      = message_now['group']['group_id']
                    gName    = message_now['group']['group_name']
                    country  = message_now['country_code']
                    user     = message_now['sender']
                    pdate    = message_now['date'].split(' ')[0]
                    phour    = message_now['date'].split(' ')[-1]
                    kind     = message_now['media']['media_type']
                    isMedia  = get_isMedia(message_now)
                    filename = message_now["media"]["stored_filename"]
                    text     = message_now['text']
                    ptime    = message_now['date']
                except: 
                    #print(this_message)
                    continue
                
                if kind == media and isMedia:
                    index = 1
                    total_msgs += 1
                
                    try:
                        hashstring = recover_hash(message_now, method, hash_methods)
                        filename   = message_now["media"]["stored_filename"]
                    except Exception as e: 
                        hashstring = recover_hash(message_now, method, hash_methods)
                        filename   = message_now["media"]["stored_filename"]
                        print(message_now)
                        #raise Exception("ERROR HASH")
                        continue
                    hashstring = smart_str(hashstring)
                    
                    if hashstring == 'None': 
                        print(message_now)
                        #raise Exception("ERROR HASH")
                        continue
                    
                    try:
                        item = messages[hashstring]
                    except KeyError as e:
                        messages[hashstring] = dict()
                        messages[hashstring]['hash']        = hashstring
                        messages[hashstring]['mediaID']     = filename
                        messages[hashstring]['date']        = pdate
                        messages[hashstring]['kind']        = kind
                        messages[hashstring]['isMedia']     = (isMedia)
                        messages[hashstring]['shares']      = list()
                        messages[hashstring]['users']       = list()
                        messages[hashstring]['groups']      = list()
                        messages[hashstring]['context_pre'] = list()
                        messages[hashstring]['context_now'] = list()
                        messages[hashstring]['context_pos'] = list()
                        messages[hashstring]['shareNumber'] = 0
                        messages[hashstring]['shareNumberGroups'] = 0
                        messages[hashstring]['shareNumberUsers'] = 0
                        for method in hash_methods:
                            #print hashstring, method, filename
                            try:
                                _m = message_now["media"]["hashes"][method]
                                messages[hashstring][method] = _m
                            except:
                                continue
                   
               
                    if user not in messages[hashstring]['users']:   messages[hashstring]['users'].append(user)
                    if gName not in messages[hashstring]['groups']: messages[hashstring]['groups'].append(gName)
                    messages[hashstring]['shareNumber'] += 1
                    messages[hashstring]['shareNumberGroups'] = len(messages[hashstring]['users'])
                    messages[hashstring]['shareNumberUsers']  = len(messages[hashstring]['groups'])     
                    if ptime < messages[hashstring]['date']: messages[hashstring]['date'] = ptime 
                    share = dict()
                    share['user'] = user
                    share['groupID'] = gID
                    share['title'] = gName
                    share['time'] = ptime
                    share['filename'] = filename
                    share['text'] = text
                    messages[hashstring]['shares'].append(share)
                    
                    MAX_MINUTES_PRE = 1
                    MAX_MINUTES_POS = 3
                    try:
                        if message_pre['text']:
                            if len(message_pre['text']) > 2 and (message_pre['group']['group_id'] == message_now['group']['group_id']): 
                                delta_time = get_time_difference(message_pre['date'], message_now['date'])
                                if delta_time <= MAX_MINUTES_PRE:
                                    context = '%s - %dmin: %s' %(message_pre['group']['group_name'], delta_time, message_pre['text'])
                                    messages[hashstring]['context_pre'].append(context)
                    except:
                        delta_time = 999
                    
                    if message_pos['text']:
                        if len(message_pos['text']) > 2  and (message_pos['group']['group_id'] == message_now['group']['group_id'] ):
                            delta_time = get_time_difference(message_now['date'], message_pos['date'])
                            #print(delta_time, "NOW:", message_now['date'], 'POS:', message_pos['date'])
                            if delta_time <= MAX_MINUTES_POS:
                                context = '%s - %dmin: %s' %(message_pos['group']['group_name'], delta_time, message_pos['text'])
                                messages[hashstring]['context_pos'].append(context)
                    
                    if text:
                        if len(text) > 2:
                            context = '%s: %s' %(message_pos['group']['group_name'], text)
                            messages[hashstring]['context_now'].append(context)
                                        
                    
                    
                    #messages[hashstring]['context_pre'] = list()
                    #messages[hashstring]['context_pos'] = list()
                    #get_time_difference(d1, d2)
                    
                    
                    
                elif media == 'text':
                    if not text:        continue
                    if len(text) < 140: continue
                    isNew = True
                    hashstring = msgID
                    for ID in messages.keys():
                        text2 = messages[ID]['message']
                        score = compare_texts(text, text2)
                        if score >= 0.75:
                            isNew = False
                            hashstring = ID
                            break
                    
                    if isNew:
                        messages[hashstring] = dict()
                        messages[hashstring]['hash']    = hashstring
                        messages[hashstring]['message'] = smart_str(text)
                        messages[hashstring]['mediaID'] = hashstring
                        messages[hashstring]['date']    = pdate
                        messages[hashstring]['kind']    = kind
                        messages[hashstring]['isMedia'] = (isMedia)
                        messages[hashstring]['shares']  = list()
                        messages[hashstring]['users']   = list()
                        messages[hashstring]['groups']  = list()
                        messages[hashstring]['shareNumber']       = 0
                        messages[hashstring]['shareNumberGroups'] = 0
                        messages[hashstring]['shareNumberUsers']  = 0
                        
                   
               
                    if user not in messages[hashstring]['users']: messages[hashstring]['users'].append(user)
                    if gName not in messages[hashstring]['groups']: messages[hashstring]['groups'].append(gName)
                    messages[hashstring]['shareNumber'] += 1
                    messages[hashstring]['shareNumberGroups'] = len(messages[hashstring]['groups'])
                    messages[hashstring]['shareNumberUsers']  = len(messages[hashstring]['users'])     
                    if ptime < messages[hashstring]['date']: messages[hashstring]['date'] = ptime 
                    share = dict()
                    share['user'] = user
                    share['groupID'] = gID
                    share['title'] = gName
                    share['time'] = ptime
                    share['filename'] = '<No_file>'
                    share['text'] = text
                    messages[hashstring]['shares'].append(share)
                    
                    
                    
                    
                    
                    
                    
    
    #for k in messages.keys():
    #    print k, messages[k]['shareNumber'] 
    print('Total Messages %s: %d' %(media, total_msgs))
    print('Total unique keys %s: %d' %(media, len(messages.keys())))
            
    filename = './JSONS/jsons_%ss/all_%s_%s.json' %(media, media, date)
    #filename = './json_teste/teste_%s_%s.json' %(media, date)
    with open(filename, 'w') as json_file:
        #js = json.dumps(messages)
        json.dump(messages, json_file, ensure_ascii=False, indent=4)
        
    return messages
    

    
    
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

def main():
    in_media  = (sys.argv[1])
    method = (sys.argv[2])
    start_date = (sys.argv[3])
    try:    
        end_date = (sys.argv[4])
    except:
        today = DATE.today().strftime('%Y-%m-%d')
        end_date = today
        
    
    dates = get_days_list(start_date, end_date)
    print 'Getting JSONS for days:', dates
    
    mediapath = list()
    mediapath.append('/scratch1/whatsapp/whatsapp_crawler/messages_per_day/')
             
    for date in dates:
        print('Processing JSON for %s' %(date))
        if in_media == 'images':
            media = 'image'
            #hash_methods = ['phash', 'checksum', 'pdq', 'ahash',  'dhash', 'whash-haar', 'whash-db4']
            hash_methods = ['checksum', 'phash']
            messages = process_data_day(media, mediapath, method, hash_methods, date)
        elif in_media == 'stickers':
            media = 'sticker'
            #hash_methods = ['phash', 'checksum', 'pdq', 'ahash',  'dhash', 'whash-haar', 'whash-db4']
            hash_methods = ['checksum', 'phash']
            messages = process_data_day(media, mediapath, method, hash_methods, date)
        elif in_media == 'videos':
            media = 'video'
            hash_methods = ['checksum']
            messages = process_data_day(media, mediapath, method, hash_methods, date)
        elif in_media == 'audios':
            media = 'audio'
            hash_methods = ['checksum']
            messages = process_data_day(media, mediapath, method, hash_methods, date)
        elif in_media == 'texts':
            media = 'text'
            hash_methods = ['checksum']
            messages = process_data_day(media, mediapath, method, hash_methods, date)
        elif in_media == 'urls':
            media = 'url'
            hash_methods = ['checksum']
            messages = process_url_day(media, mediapath, method, hash_methods, date)
        else:
            media = 'image'
        #convert_messages_to_json(messages, media, date)
       
if __name__ == "__main__":
    main()
    exit()
