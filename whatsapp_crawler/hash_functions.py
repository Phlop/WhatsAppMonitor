# -*- coding: utf-8 -*-
__author__ = "Philipe Melo"
__email__ = "philipe@dcc.ufmg.br"

import os
import sys
import time
from datetime import datetime
import hashlib

from os.path import isfile, join
from sys import argv, stdout

import sys
from PIL import ImageFile    
from PIL import Image    

import six
import imagehash
import imghdr


#from pdqhashing.hasher.pdq_hasher import PDQHasher
#from pdqhashing.types.hash256 import Hash256



data_path_image = ''
data_path_audio = ''
data_path_video = ''

ImageFile.LOAD_TRUNCATED_IMAGES = True

def compare_texts(text1, text2):
    if text1 is None or text2 is None: return 0.0
    bow_text1 = text1.split()
    bow_text2 = text2.split()
    score = jaccard_similarity(text1, text2)
    return score

def hamming_distance(hash1, hash2, treshold=16):   
    hamming = hash1.hammingDistance(hash2)
    if hamming <= treshold: 
        return True, hamming
    else:
        return False, hamming
    

def compare_hashes(hash1, hash2, treshold=16):   
    if hamming <= treshold: 
        return True, hamming
    else:
        return False, hamming
    


def equal_hashes(hash1, hash2):   
    return hash1 == hash2


def load_pHash_from_string(string_hash):
   image_hash = imagehash.hex_to_hash(string_hash)
   return image_hash

def load_PDQhash_from_string(string_hash):
   image_hash = Hash256.fromHexString(string_hash)
   return image_hash


def get_facebookPDQ_hash(filename):
    pdq_hash = ''
    pdq = PDQHasher()
    try:
        computed_hash = pdq.fromFile(filename)
        pdq_hash = computed_hash.getHash()
        
    except Exception as e:
        sys.stderr.write( "Error processing PDQ hash for file %s!!" %(filename) )
        print (e)
        #pdq_hash = Hash256.fromHexString('')
    return pdq_hash



def getCheckSum(filename):
    check = ''
    if os.path.isfile(data_path_image+filename) :
        image_file = open(data_path_image+filename).read()
        check = hashlib.md5(image_file).hexdigest()
    return  check



 
def get_pHash(filename):
    pHahs = ''
    if os.path.isfile(data_path_image+filename) :
        try:
            pHash = imagehash.phash(Image.open(data_path_image+filename))
        except Exception as e:
            print ('Error pHash for %s!' %(filename), e)
            pHash = ''
    return  pHash



def is_image(filename):
    f = filename.lower()
    return f.endswith(".png") or f.endswith(".jpg") or \
        f.endswith(".jpeg") or f.endswith(".bmp") or f.endswith(".gif") or '.jpg' in f


def get_hash_from_method(filename, method):
    hash = ''
    hash_function = get_hash_func(method)
    try:
        hash = hash_function(filename)
    except:
        try:
            hash = hash_function(Image.open(filename))
        except Exception as e:
            print('Problem:', e, 'with', filename)
    return hash
    
def get_comparison_method(media):
    if media == 'image':
        return equal_hashes
    elif media == 'video':
        return equal_hashes
    elif media == 'audio':
        return equal_hashes
    elif media == 'text':
        return equal_hashes
    elif media == 'text':
        return compare_texts
    elif media == 'pdq':
        return hamming_distance
    elif media == 'hashes':
        return compare_hashes
    else:
        return equal_hashes
   

def get_hash_func(hashmethod):
    if hashmethod == 'ahash':
        hashfunc = imagehash.average_hash
    elif hashmethod == 'phash':
        hashfunc = imagehash.phash
    elif hashmethod == 'dhash':
        hashfunc = imagehash.dhash
    elif hashmethod == 'whash-haar':
        hashfunc = imagehash.whash
    elif hashmethod == 'whash-db4':
        hashfunc = lambda img: imagehash.whash(img, mode='db4')
    elif hashmethod == 'pdq':
        hashfunc = get_facebookPDQ_hash
    elif hashmethod == 'checksum':
        hashfunc = getCheckSum
    else:
        hashfunc = imagehash.phash
    return hashfunc

 
