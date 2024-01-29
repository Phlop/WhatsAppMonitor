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
from common import insert_whatsapp_audios_on_database
from common import get_days_list

conn = connect_app_database()


def load_whatsapp_data(filename):
    data = json.loads(open(filename).read()).values()
    return data


def main(filename):
    t_start = time.time()
    filename_audios = filename

    print('>>> START: Get Whatsapp Audio Data')
    audios = load_whatsapp_data(filename=filename_audios)
    print('\t>>> Total audio:', len(audios))
    print('>>> DONE: Get Whatsapp Audio Data')


    print('>>> START: Inserting Audios on database')
    insert_whatsapp_audios_on_database(conn=conn, audios=audios)
    print('>>> DONE: Inserting Audios on database')

    print("\tTime: %lf" % (time.time() - t_start))

def list_all_files():
    "../GET_JSON/jsons_images/all_image_2020-07-10.json "
    
    if len(sys.argv) >=3:
        files_path = sys.argv[1]
        start_date = sys.argv[2]
        end_date = sys.argv[3]
    
        dates = get_days_list(start_date, end_date)
        for date in dates:
            print ('Insert files from', date)
            filename = files_path+'all_audio_'+date+'.json'
            main(filename)
        
    
    else:
        print ('Missing parameter!! run command:\npython insert_whatsapp_<type>.py  <path_files> <start_date(YYYY-MM_DD)>  <end_date(YYYY-MM_DD)>'  )
    
    
if __name__ == "__main__":
    list_all_files()
    exit()
