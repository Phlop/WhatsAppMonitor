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


def main():
    t_start = time.time()
    #filename_images = sys.argv[1]
    #filename_nsfw_scores = sys.argv[2]
    #filename_links = 'links_dataUpdated.json'
    filename_links = sys.argv[1]
    #print('>>> START: Get Whatsapp Image Data')
    #images = load_whatsapp_data(filename=filename_images)
    #nsfw_scores = load_nsfw_scores(filename=filename_nsfw_scores)
    #print('\t>>> Total images: ', len(images))
    #print('>>> DONE: Get Whatsapp Image Data')

    print('>>> START: Get Whatsapp Link Data')
    links = load_whatsapp_data(filename=filename_links)
    print('\t>>> Total links: ', len(links))
    print('>>> DONE: Get Whatsapp Links Data')

    #print('>>> START: Inserting Images on database')
    #insert_whatsapp_images_on_database(conn=conn, images=images, nsfw_scores=nsfw_scores)
    #print('>>> DONE: Inserting Images on database')

    print('>>> START: Inserting Links on database')
    insert_whatsapp_links_on_database(conn=conn, links=links)
    print('>>> DONE: Inserting Links on database')

    print("\tTime: %lf" % (time.time() - t_start))


if __name__ == "__main__":
    main()
    exit()
