# -*- coding: utf-8 -*-
__author__ = "Johnnatan Messias"
__copyright__ = "Departamento de Ciência da Computação - UFMG - Brazil"
__email__ = "johnnatan@dcc.ufmg.br"
__website__ = "http://johnnatan.me"
__status__ = "Done"

import json
import gzip
import time
import sys
import pytz
import sys
from datetime import datetime
from common import connect_app_database
from common import insert_whatsapp_images_on_database
from common import insert_whatsapp_links_on_database
from common import insert_whatsapp_messages_on_database
from common import insert_whatsapp_videos_on_database
from common import get_days_list

path = 'data/'
conn = connect_app_database()


def load_whatsapp_data(filename):
    data = json.loads(open(filename).read()).values()
    return data


def load_nsfw_scores(filename):
    nsfw_scores = dict()
    inFile = open(filename, 'rt')
    for line in inFile:
        data = json.loads(line)
        nsfw_scores[data['input_file']] = data['NSFW score']
    inFile.close()
    return nsfw_scores


def main(filename):
    t_start = time.time()
    filename_videos = filename
    nsfw_scores = list()
    
    videos = load_whatsapp_data(filename=filename_videos)
        
    print('>>> START: Get Whatsapp Link Data')
    
    print('\t>>> Total Text Messages: ', len(videos))
    print('>>> DONE: Get Whatsapp Text Message Data')
    
    print('>>> START: Inserting Messages on database')
    insert_whatsapp_videos_on_database(conn=conn, videos=videos, nsfw_scores=nsfw_scores)
    print('>>> DONE: Inserting Messages on database')

    print("\tTime: %lf" % (time.time() - t_start))


def list_all_files():
    #"../GET_JSON/jsons_videos/all_videos_2020-07-10.json "
    
    if len(sys.argv) >=3:
        files_path = sys.argv[1]
        start_date = sys.argv[2]
        end_date = sys.argv[3]
    
        dates = get_days_list(start_date, end_date)
        for date in dates:
            print ('Insert files from', date)
            filename = files_path+'all_video_'+date+'.json'
            main(filename)
        
    
    else:
        print ('Missing parameter!! run command:\npython insert_whatsapp_<type>.py  <path_files> <start_date(YYYY-MM_DD)>  <end_date(YYYY-MM_DD)>'  )
    
    
if __name__ == "__main__":
    list_all_files()
    exit()