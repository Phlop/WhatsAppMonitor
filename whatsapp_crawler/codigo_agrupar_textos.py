import os, re, sys
import random
import string
import json
import time

import hashlib
import random
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

from statsmodels.distributions.empirical_distribution import ECDF

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import PercentFormatter
import matplotlib.ticker as ticker

from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)
 

from urlextract import URLExtract
import tldextract
import requests

import unidecode
from os import listdir
from os.path import isfile, join

import phonenumbers
from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
    region_code_for_number,
)


def SetPlotRC():
    plt.rc('font',family='sans-serif')
    plt.rc('pdf',fonttype = 42)
    plt.rc('ps',fonttype = 42)

    
def plot_days_counts(list_days, list_values, path, leg, Ylabel, colors, lines, period):

    LEGEND_SIZE = 17
    LABEL_SIZE = 22
    TICK_SIZE = 16
    SMALL_SIZE = 24
    MEDIUM_SIZE = 24    
    BIGGER_SIZE = 30
    plt.rc('axes', titlesize=LABEL_SIZE)  
    plt.rc('axes',  labelsize=LABEL_SIZE)   
    plt.rc('xtick', labelsize=TICK_SIZE) 
    plt.rc('ytick', labelsize=TICK_SIZE)   
    plt.rc('legend', fontsize=LEGEND_SIZE)   
    plt.rc('figure', titlesize=MEDIUM_SIZE) 
    fig, ax = plt.subplots(figsize=(12,4.5))

    k=0
    for values in list_values:
        period_days = list()
        counts    = list()
        time_window = 1
        sum = 0
        for d in range(len(list_days)):
            sum += values[d]
            time_window += 1
            
            if time_window%period == 0:
                period_days.append(list_days[d])
                counts.append(sum)
                sum = 0
                time_window = 1
        
        days = [datetime.strptime(x, '%Y-%m-%d') for x in period_days]
        days2 = mdates.date2num(days)
        ax.plot_date(days2, counts, marker = '', color=colors[k], linestyle=lines[k], linewidth=1.5, alpha=0.8 )
        k+=1
     
    months = mdates.MonthLocator(range(1,13), bymonthday=2, interval=1)
    monthsFmt = mdates.DateFormatter("%d/%m/%y") 
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.autoscale_view()
    #ax.set_yscale('log')
    fig.autofmt_xdate()
    plt.ylabel(Ylabel)
    plt.grid()
    plt.xticks(rotation=40)
    if len(leg) > 1:
        plt.legend(leg,  ncol=3, loc='upper center')
    plt.margins(x=0)
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_horizontalalignment('center')
        
    plt.savefig(path+'.jpg', bbox_inches='tight')
    plt.savefig(path+'.pdf', bbox_inches='tight')
    plt.clf()
    plt.cla()
    


def plot_hist(list_curve, colors, styles, label_curve, x_label, y_label, chart_path, Density=True, isLog=True):

    LEGEND_SIZE = 20
    LABEL_SIZE = 24
    TICK_SIZE = 17
    SMALL_SIZE = 18
    MEDIUM_SIZE = 24    
    BIGGER_SIZE = 30
    plt.rc('axes', titlesize=SMALL_SIZE)  
    plt.rc('axes',  labelsize=LABEL_SIZE)   
    plt.rc('xtick', labelsize=TICK_SIZE) 
    plt.rc('ytick', labelsize=TICK_SIZE)   
    plt.rc('legend', fontsize=LEGEND_SIZE)   
    plt.rc('figure', titlesize=MEDIUM_SIZE) 
    SetPlotRC()
    fig, ax = plt.subplots(figsize=(7,5))
    
    n = len(list_curve)
    for k in range(n):
        if Density:
            weights = np.ones_like(list_curve[k])*100.00 / len(list_curve[k])
            plt.hist(list_curve[k], weights=weights, color = colors[k], edgecolor='black', alpha=0.75, bins=20, linewidth=1)  # density=False would make counts
            ax.yaxis.set_major_formatter(PercentFormatter())
    
        else:
            plt.hist(list_curve[k], color = colors[k], edgecolor='black', alpha=0.75, bins=20, linewidth=1)  # density=False would make counts
    
    #ax.xaxis.set_major_locator(ticker.MultipleLocator(10)) # set x sticks interal
    #ax.xaxis.set_major_formatter(PercentFormatter())
    if len(label_curve) > 1:
        plt.legend(loc='lower right')
    if isLog:
        ax.set_yscale('log')
    ax.set_adjustable("box")
    plt.grid()
    plt.xticks(rotation=40)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.tight_layout()
    fig.savefig(chart_path+'.pdf', bbox_inches = 'tight',    pad_inches = 0)
    fig.savefig(chart_path+'.png', bbox_inches = 'tight',    pad_inches = 0)
    plt.clf()
    plt.cla()

 
 

def plot_cdf_n_curves(list_curve, colors, styles, label_curve, x_label, chart_path, isLog=True):
    LEGEND_SIZE = 20
    LABEL_SIZE = 24
    TICK_SIZE = 17
    SMALL_SIZE = 18
    MEDIUM_SIZE = 24    
    BIGGER_SIZE = 30
    plt.rc('axes', titlesize=SMALL_SIZE)  
    plt.rc('axes',  labelsize=LABEL_SIZE)   
    plt.rc('xtick', labelsize=TICK_SIZE) 
    plt.rc('ytick', labelsize=TICK_SIZE)   
    plt.rc('legend', fontsize=LEGEND_SIZE)   
    plt.rc('figure', titlesize=MEDIUM_SIZE) 
    SetPlotRC()
    
    fig, ax = plt.subplots(figsize=(7,5))
    
    n = len(list_curve)
    ecdf_list = list()
    for k in range(n):
        list_curve[k].sort()
        cdf = ECDF(list_curve[k])
        ecdf_list.append(cdf)
    
    for k in range(n):
        plt.plot(ecdf_list[k].x, ecdf_list[k].y, linestyle=styles[k] , color=colors[k], label=label_curve[k], linewidth=3)
 
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(30)) # set x sticks interal
    if len(label_curve) > 1:
        plt.legend(loc='lower right')
    #ax.set_title(title_name)
    if isLog:
        ax.set_xscale('log')
    ax.set_xlabel(x_label)
    ax.set_adjustable("box")
    ax.set_ylabel('CDF')
    plt.grid()
    plt.tight_layout()
    fig.savefig(chart_path+'.pdf', bbox_inches = 'tight',    pad_inches = 0)
    fig.savefig(chart_path+'.png', bbox_inches = 'tight',    pad_inches = 0)
    plt.clf()
    plt.cla()
    
    
def _process_string(string):
    string = string.strip()
    string = string.replace('\r', '')
    string = string.replace('\n', ' ')
    string = string.replace('\t', ' ')
    #string = smart_str(string)
    return string

        
def process_text_for_latex(text):
    text.replace('_',' ')
    text.replace('$','S')
    text.replace('#','-')
    text.replace('\\','/')
    text.replace('\t',' ')
    text.replace('\n',' ')
    text.replace('\r','')
    return text
        
def anonymize_message(message):
    string = message
    string = string.strip()
    string = string.replace('\r', '')
    string = string.replace('\n', ' ')
    string = string.replace('\t', ' ')
    string = smart_str(string)
    return string
 
def create_messages_data(all_messages, path, out_file):
    #false_558399689520-1507037580@g.us_23FC82251D187451C8F3F4463ED4B269	558399689520-1507037580	Anti-esquerda	55	+554396102010	2020-03-29	08:23:38	text	False	<NoFile>	Liberacao da Cloroquina pela Anvisa, ja com posologia para tratamento do Covid-19!!
    data_file = join(path,'all_messages_%s.csv' %(out_file))
    print('>>>>Storing all messages in %s file' %(out_file))
    with open(data_file, 'w') as fout:
        message_string = '{ID}\t{GID}\t{UID}\t{NAME}\t{DATE}\t{TIME}\t{CC}\t{DDD}\t{TYPE}\t{TEXT}'.format(ID='ID', GID='GroupID', UID='UserID', NAME='GroupName', DATE='Date', TIME='Time', CC='Country', DDD='Location', TYPE='Type', TEXT='Text')
        print(message_string, file=fout)
        for message in all_messages:

            id       =  message['messageID'] 
            gid      =  message['groupID'] 
            uid      =  message['user']   
            name     =  message['gName'] 
            date     =  message['date'] 
            time     =  message['time'] 
            type     =  message['msg_type'] 
            is_media =  message['is_media'] 
            filename =  message['filename'] 
            text     =  message['text']
            country = message['country_code']
            ddd = message['ddd_code']
            
            _ID = id
            GID = gid
            UID = uid
            message_string = '{ID}\t{GID}\t{UID}\t{NAME}\t{DATE}\t{TIME}\t{CC}\t{DDD}\t{TYPE}\t{TEXT}'.format(ID=_ID, GID=GID, UID=UID, NAME=name, DATE=date, TIME=time, CC=country, DDD=ddd, TYPE=type, TEXT=text)
            print(message_string, file=fout)
            
    
def get_messages_day(all_messages, start_date, end_date, path, out_file):
    print('>>>>Getting Messages per day for messages')
    
    formatter = '%Y-%m-%d'
    date1 = datetime.strptime(start_date, formatter)
    date2 = datetime.strptime(end_date, formatter)
    delta = date2 - date1       # as timedelta

    total_day = dict()
    dates_list = list()
    for i in range(delta.days + 1):
        day = date1 + timedelta(days=i)
        date_string = day.strftime(formatter)
        dates_list.append(date_string)
        total_day[date_string] = 0
    
    for message in all_messages:
        date = message['date']
        try:    total_day[date] += 1
        except: total_day[date] = 1
        
    
    list_days   = list()
    list_values = list()
    Ylabel = '#Mensagens'
    legend = ['WhatsApp']
    colors = ['green']
    lines =  ['-']
    period = 1
    data_file = join(path,'data_%s.txt' %(out_file))
    with open(data_file, 'w') as fout:
    
        print('%s\t%s'%('DATE', '#MESSAGES'), file=fout)
        values = list()
        for day in sorted(total_day.keys()):
            list_days.append(day)
            values.append(total_day[day])
            print('%s\t%d'%(day, total_day[day]), file=fout)
    list_values = [values]    
    p_name = '%s/%s'%(path, out_file)
    plot_days_counts(list_days, list_values, p_name, legend, Ylabel, colors, lines, period)                


def get_messages_group(all_messages, path, out_file):
    print('>>>>Getting total Messages sent per GROUP')
    
    groups = dict()
    for message in all_messages:
        gid = message['groupID']
        try:    groups[gid] += 1
        except: groups[gid] = 1
        
    
    values = list()
    x_label = '#Mensagens Enviadas'
    x_label = '#Mensagens'
    y_label = 'Grupos'
    legend = [ ]
    label_curve = ['']
    colors = ['green']
    styles =  ['-']
    
    data_file = join(path,'data_%s.txt' %(out_file))
    with open(data_file, 'w') as fout:
        print('GROUP_ID\t#MESSAGES', file=fout)
        for gid in groups.keys():
            values.append(groups[gid])
            print('%s\t%d'%(gid, groups[gid]), file=fout)
            
    p_name = '%s/cdf_%s'%(path, out_file)
    plot_cdf_n_curves([values], colors, styles, label_curve, x_label, p_name, isLog=True)
    p_name = '%s/hist_%s'%(path, out_file)
    plot_hist([values], colors, styles, label_curve, x_label, y_label, p_name, Density=False, isLog=False)
    
    
def get_messages_user(all_messages, path, out_file):
    print('>>>>Getting total Messages sent per USER')
    
    users = dict()
    for message in all_messages:
        uid = message['user']
        uid = hashlib.md5(uid.encode('utf-8')).hexdigest()
        
        try:    users[uid] += 1
        except: users[uid] = 1
        
    
    values = list()
    x_label = '#Mensagens Enviadas' 
    y_label = 'Usuarios'
    legend = [ ]
    label_curve = ['']
    colors = ['green']
    styles =  ['-']
    
    data_file = join(path,'data_%s.txt' %(out_file))
    with open(data_file, 'w') as fout:
        
        print('USER_ID\t#MESSAGES', file=fout)
        for uid in users.keys():
            values.append(users[uid])
            print('%s\t%d'%(uid, users[uid]), file=fout)
    
    p_name = '%s/cdf_%s'%(path, out_file)
    plot_cdf_n_curves([values], colors, styles, label_curve, x_label, p_name, isLog=True)
    p_name = '%s/hist_%s'%(path, out_file)
    plot_hist([values], colors, styles, label_curve, x_label, y_label, p_name, Density=False, isLog=False)


def get_messages_types(all_messages, path, out_file):
    print('>>>>Getting total Messages sent per MEDIA TYPE')
    
    medias = dict()
    for message in all_messages:
        tipo = message['msg_type']
        try:    medias[tipo] += 1
        except: medias[tipo] = 1
        
    data_file = join(path,'data_%s.txt' %(out_file))
    with open(data_file, 'w') as fout:
        print('%s\t%s'%('TYPE', '#TOTAL'), file=fout)
        for tipo in medias.keys():
            print('%s\t%d'%(tipo, medias[tipo]), file=fout)
    


def count_groups_political(all_messages, path, out_file):
    print('>>>>Getting total groups for each political alignement')
    
    groups_label_filename = 'labels_groups.txt'
    labels = dict()
    with open(groups_label_filename, 'r') as flabel:
        for line in flabel:
            tokens = line.strip().split('\t')
            labels[tokens[0]] = tokens[1]
    
    groups = dict()
    for message in all_messages:
        gid = message['groupID']
        try:    groups[gid] += 1
        except: groups[gid] = 1
        
    TOTAL = dict()
    sum = 0
    for gid in groups.keys():
        try: l = labels[gid]
        except:
            print('Groups %s not labeled' %(gid)) 
            continue
        try:    
            TOTAL[l] += 1
            sum += 1
        except: TOTAL[l]  = 1
        
    data_file = join(path,'data_%s.txt' %(out_file))
    with open(data_file, 'w') as fout:
        print('POLITICAL\t#GROUPS', file=fout)
        print('%s\t%d'%('Esquerda', TOTAL['E']), file=fout)
        print('%s\t%d'%('Direita', TOTAL['D']), file=fout)
        print('%s\t%d'%('Indefinido', TOTAL['I']), file=fout)
    

def count_messages_political(all_messages, path, out_file):
    print('>>>>Getting total messages for each political alignement')
    
    groups_label_filename = 'labels_groups.txt'
    labels = dict()
    with open(groups_label_filename, 'r') as flabel:
        for line in flabel:
            tokens = line.strip().split('\t')
            labels[tokens[0]] = tokens[1]
    
    groups = dict()
    for message in all_messages:
        gid = message['groupID']
        try:    groups[gid] += 1
        except: groups[gid] = 1
        
    TOTAL = dict()
    sum = 0
    for gid in groups.keys():
        try: l = labels[gid]
        except:
            print('Groups %s not labeled' %(gid))
            continue
        try:    
            TOTAL[l] += groups[gid]
            sum += groups[gid]
        except: TOTAL[l]  = groups[gid]
        
    data_file = join(path,'data_%s.txt' %(out_file))
    with open(data_file, 'w') as fout:
        print('POLITICAL\t#MESSAGES', file=fout)
        print('%s\t%d'%('Esquerda', TOTAL['E']), file=fout)
        print('%s\t%d'%('Direita', TOTAL['D']), file=fout)
        print('%s\t%d'%('Indefinido', TOTAL['I']), file=fout)
    


def get_ddd_from_number(message):
    state_codes = {11:'SP', 12:'SP', 13:'SP', 14:'SP',
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
    ddd =  message['ddd_code']
    state = state_codes[ddd]

    return state
    
    
        
def get_messages_location(all_messages, path, out_file):
    print('>>>>Counting DDDs per message')
    
    country_codes = dict()
    country_users = dict()
    country_groups = dict()
    ddd_codes     = dict()
    ddd_users     = dict()
    ddd_groups     = dict()
    
    
    for message in all_messages:
        text = message['text']
        uid = message['user']
        gid = message['groupID']
        cc = message['country_code']
        #print(uid, pn, cc)
        try:     country_codes[cc] +=1
        except:  
            country_codes[cc]  =1
            country_groups[cc] = set()
            country_users[cc] = set()
        country_groups[cc].add(uid)
        country_users[cc].add(uid)
        if cc == 'BR':
            ddd = get_ddd_from_number(message)
            try:     ddd_codes[ddd] +=1
            except:  
                ddd_codes[ddd]  = 1
                ddd_users[ddd]  = set()
                ddd_groups[ddd] = set()
            ddd_users[ddd].add(uid)
            ddd_groups[ddd].add(uid)
        
    data_file = join(path, 'data_country_%s.txt' %(out_file))
    with open(data_file, 'w') as fout:
        print('%s\t%s\t%s'%('COUNTRY', '#MESSAGES', '#USERS'), file=fout)
        for key in sorted(country_codes, key=country_codes.get, reverse=True):
            print('%s\t%d\t%d'%(key, country_codes[key], len(country_users[key])), file=fout)

    data_file = join(path, 'data_ddd_%s.txt' %(out_file))
    with open(data_file, 'w') as fout:
        print('%s\t%s\t%s'%('DDD', '#MESSAGES', '#USERS'), file=fout)
        for key in sorted(ddd_codes, key=ddd_codes.get, reverse=True):
            print('%s\t%d\t%d'%(key, ddd_codes[key], len(ddd_users[key])), file=fout)



def has_keyword(message, key):
    if not message:      return False
    if len(message) < 3: return False
    tokens = message.split(' ')
    if len(tokens) <= 1:
        return False
    
    key = key.lower().strip()
    key_tokens = key.split(' ')
    n_gram = len(key_tokens)
    
    if n_gram > 1:
        if key.lower() in message.lower():
            #print ('PALAVRA N_GRAM > 1', key, '--', message)        
            return True
        else:
            return False
        
    else:
        for word in tokens:
            if key == word:
                #print ('PALAVRA EXATA', key, '--', message)
                return True
    
    return False
    
    


def has_keyword_simplified(message, key):
    if not message:      return False
    if len(message) < 3: return False
    tokens = message.split(' ')
    if len(tokens) <= 1:
        return False
    
    key = key.lower().strip()
    message = message.lower()
    if key in message:
        return True
    
    return False
    
    
        
def count_popularity_keywords(all_messages, keywords, path, out_file):
    print('>>>>Counting popularity of KEYWORDS')
    
    n_keywords = set()
    for k in keywords:
        n_keywords.add(unidecode.unidecode(k))
    
    count_keywords = dict()
    keywords_groups = dict()
    keywords_users = dict()
    for key in n_keywords:
        count_keywords[key] = 0
        keywords_groups[key] = set()
        keywords_users[key] = set()
    
    for message in all_messages:
        text = message['text']
        uid = message['user']
        gid = message['groupID']
        text = unidecode.unidecode(text).lower()
        for key in n_keywords:
            if has_keyword(text, key):
                count_keywords[key] +=1
                keywords_groups[key].add(gid)
                keywords_users[key].add(uid)
        
    data_file = join(path,'data_%s.txt' %(out_file))
    with open(data_file, 'w') as fout:
        print('%s\t%s\t%s\t%s'%('KEYWORD', '#TOTAL', '#GROUPS', '#USERS'), file=fout)
        for key in sorted(count_keywords, key=count_keywords.get, reverse=True):
            print('%s\t%d\t%d\t%d'%(key, count_keywords[key], len(keywords_groups[key]), len(keywords_users[key])), file=fout)

   

    
def count_popularity_hashtags(all_messages, path, out_file):
    print('>>>>Counting popularity of HASHTAGS')
    count_hashtags = dict()
    hashtags_groups = dict()
    hashtags_users = dict()
    
    for message in all_messages:
        text = message['text']
        uid = message['user']
        gid = message['groupID']
        for token in text.split(' '):
            term = token.strip()
            term = token.strip('.,\'")({}/\\\t')
            term = process_word(term)
            try:
                if term[0] == '#': 
                    try:   count_hashtags[term] += 1
                    except KeyError as e: 
                        count_hashtags[term]  = 1
                        hashtags_groups[term]  = set()
                        hashtags_users[term]  = set()
                    hashtags_groups[term].add(gid)
                    hashtags_users[term].add(uid)
    
            except: continue
        
    data_file = join(path,'data_%s.txt' %(out_file))
    with open(data_file, 'w') as fout:
        print('%s\t%s\t%s\t%s'%('HASHTAGS', '#TOTAL', '#GROUPS', '#USERS'), file=fout)
        for key in sorted(count_hashtags, key=count_hashtags.get, reverse=True):
            print('%s\t%d\t%d\t%d'%(key, count_hashtags[key], len(hashtags_groups[key]), len(hashtags_users[key])), file=fout)

def process_word(term):
    term = term.lower()
    term = term.strip('*')
    term = term.strip('.')
    term = term.strip(',')
    term = term.strip('?')
    term = term.strip('!')
    term = term.strip('_')
    term = term.strip('\"')
    term = term.strip('\'')
    term = term.replace('/', '')
    term = term.replace('(', '')
    term = term.replace(')', '')
    term = term.replace('{', '')
    term = term.replace('}', '')
    term = term.replace('[', '')
    term = term.replace(']', '')
    return term
    
def count_popularity_terms(all_messages, path, out_file):
    print('>>>>Counting popularity of ALL TERMS')
    top_terms = dict()
    terms_users = dict()
    terms_groups = dict()
    
    for message in all_messages:
        text = message['text']
        uid = message['user']
        gid = message['groupID']
        for token in text.split(' '):
            term = token.strip()
            term = process_word(term)
            term = term.strip('#')
            try:   top_terms[term] += 1
            except KeyError as e: 
                top_terms[term]  = 1
                terms_groups[term]  = set()
                terms_users[term]  = set()
            terms_groups[term].add(gid)
            terms_users[term].add(uid)
        
    data_file = join(path,'data_%s.txt' %(out_file))
    with open(data_file, 'w') as fout:
        print('%s\t%s\t%s\t%s'%('TERM', '#TOTAL', '#GROUPS', '#USERS'), file=fout)
        for key in sorted(top_terms, key=top_terms.get, reverse=True):
            print('%s\t%d\t%d\t%d'%(key, top_terms[key], len(terms_groups[key]), len(terms_users[key])), file=fout)


def media_dict():

    M = {'youtube.com':{
            'name' : 'Youtube',
            'color': 'red',
            'dash' : '-',
            'short' : 'YT',
            }, 
        'facebook.com':{
            'name' : 'Facebook',
            'color': 'blue',
            'dash' : '--',
            'short' : 'FB',
            },  
        'instagram.com':{
            'name' : 'Instagram',
            'color': 'purple',
            'dash' : ':',
            'short' : 'IG',
            }, 
        'twitter.com':{
            'name' : 'Twitter',
            'color': 'cyan',
            'dash' : '-.',
            'short' : 'TW',
            },  
        'whatsapp.com':{
            'name' : 'WhatsApp',
            'color': 'green',
            'dash' : ':',
            'short' : 'WP',
            },  
        't.me':{
            'name' : 'Telegram',
            'color': 'blue',
            'dash' : '--',
            'short' : 'TL',
            },  
        'pinterest.com':{
            'name' : 'Pinterest',
            'color': 'pink',
            'dash' : ':',
            'short' : 'PT',
            },  
        'reddit.com':{
            'name' : 'Reddit',
            'color': 'orange',
            'dash' : '-.',
            'short' : 'RE',
            },  
        'google.com':{
            'name' : 'Google',
            'color': 'yellow',
            'dash' : '-',
            'short' : 'GO',
            }
    }
    
    return M
            
def extract_urls(extractor, text):
    urls = extractor.find_urls(text)
    return urls


    
def is_special_domains(URL):
    urls_expanded = ['www.instagram.com', 'chat.whatsapp.com', 'https://t.me/', 'gazetabrasil.com.br', 'jornaldacidadeonline.com.br', 'conexaopolitica.com.br']
    for url in urls_expanded:
        if url in URL:
            return True
    
    return False


def count_URLs(all_messages, path, out_file):
    mainstream_medias = ['youtube.com', 'facebook.com', 'instagram.com', 'twitter.com', 'whatsapp.com', 't.me', 'pinterest.com', 'reddit.com', 'google.com']
    mainstream_date = dict()
    M = media_dict()
    
    
    extractor = URLExtract()
    print('>>>>Counting popularity of URLS and DOMAINS')
    URLs = dict()
    URLs_date = dict()
    URLs_users = dict()
    URls_groups = dict()
    full_URLs = dict()
    full_URLs_users = dict()
    full_URls_groups = dict()
    domains = dict()
    domains_users = dict()
    domains_groups = dict()
    domains_unique = dict()
    
    total_urls = 0
    total_msgs = 0
    for message in all_messages:
        text = message['text']
        uid  = message['user']
        gid  = message['groupID']
        date = message['date']
        extracted = extract_urls(extractor, text) 
        total_msgs += 1
        
        try: A = mainstream_date[date]
        except: 
            mainstream_date[date] = dict()
            for m in mainstream_medias: mainstream_date[date][m] = 0
        
        for url in extracted:
            #print(total_msgs, url)
            try:
                URLs[url] += 1
            except Exception as error:
                URLs[url]        = 1
                URLs_users[url]  = set()
                URls_groups[url] = set()
                URLs_date[url] = set()
            total_urls += 1
            URLs_users[url].add(uid)
            URls_groups[url].add(gid)
            URLs_date[url].add(date)
    print('TOTAL %d messages. TOTAL %d URLS found and %d  distinct' %(total_msgs, total_urls, len(URLs.keys() )))
    
    for url in URLs.keys():
        
        
        expand_urls = True
        
        if is_special_domains(url):
            full_url = url
        
        elif expand_urls:
            try:
                reveal = requests.get(url, timeout=2.5)
                full_url = reveal.url
            except Exception as error:
                #print(error, url)
                full_url = url
        else:
            full_url = url
            
        try:
            full_URLs[full_url] +=  URLs[url]
        except:
            full_URLs[full_url] =   URLs[url]
            full_URLs_users[full_url]  = set()
            full_URls_groups[full_url] = set()
        full_URLs_users[full_url].update(URLs_users[url])
        full_URls_groups[full_url].update(URls_groups[url])
        
    
        #ExtractResult(subdomain='forums.news', domain='cnn', suffix='com')
        result = tldextract.extract(full_url)
        dom = '%s.%s'%(result.domain, result.suffix)
        try:
            domains[dom] +=  URLs[url]
            domains_unique[dom] += 1
        except:
            domains[dom] =   URLs[url]
            domains_users[dom]  = set()
            domains_groups[dom] = set()
            domains_unique[dom] = 1
        domains_users[dom].update(URLs_users[url])
        domains_groups[dom].update(URls_groups[url])
        
        if dom in mainstream_medias:
            for date in URLs_date[url]:
                mainstream_date[date][dom] += 1
        
    print('TOTAL %d messages. %d Total and Unique %d URLS and %d DOMAINS' %(total_msgs, total_urls, len(full_URLs.keys()), len(domains.keys()) ))
    data_file = join(path, 'data_urls_%s.txt' %(out_file))
    with open(data_file, 'w') as fout:
        print('%s\t%s\t%s\t%s'%('URL', '#TOTAL', '#GROUPS', '#USERS'), file=fout)
        for key in sorted(full_URLs, key=full_URLs.get, reverse=True):
            print('%s\t%d\t%d\t%d'%(key, full_URLs[key], len(full_URls_groups[key]), len(full_URLs_users[key])), file=fout)
                    
    data_file = join(path, 'data_domains_%s.txt' %(out_file))
    with open(data_file, 'w') as fout:
        print('%s\t%s\t%s\t%s'%('DOMAIN', '#TOTAL', '#UNIQUE_URLS', '#USERS'), file=fout)
        for key in sorted(domains, key=domains.get, reverse=True):
            print('%s\t%d\t%d\t%d'%(key, domains[key], domains_unique[key], len(domains_users[key])), file=fout)

    
    data_file = join(path, 'data_mainstrem_%s.txt' %(out_file))
    with open(data_file, 'w') as fout:
        header = 'Date'
        for m in mainstream_medias:
            header =  header +'\t%s' %(M[m]['name'])
        print(header, file=fout)
    
        for day in sorted(mainstream_date.keys()):
                final_string = '%s' %(day)
                values = list()
                for m in mainstream_medias:
                    v = mainstream_date[day][m]
                    final_string =  final_string +'\t%d' %(v)
                print(final_string, file=fout)
                
    list_days = list()
    for d in sorted(mainstream_date.keys()):
        list_days.append(d)
    
    Ylabel = '# Total de URLs'
    period = 7
    plot_name = join(path, 'data_mainstream_%s.txt' %(out_file))
    list_values = list()
    list_colors = list()
    list_lines = list()
    list_label = list()
    
    for m in mainstream_medias:
        values = list()
        for day in list_days:
            v = mainstream_date[day][m]
            values.append(v)
        list_values.append(values)
        list_colors.append(M[m]['color'])
        list_lines.append(M[m]['dash'])
        list_label.append(M[m]['name'])
    
    plot_days_counts(list_days, list_values, plot_name, list_label, Ylabel, list_colors, list_lines, period)
    
    
    

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

 
def compare_images(filename1, filename2):
    if filename1 is None or filename2 is None: return 0.0
    score = 0
    if filename1 == filename2:
        score=1
    return score
   
    
    
def group_messages(all_messages, path, out_file, max=1000):

    print('>>>>Groups messages by popularity')
    total_urls = 0  
    total_msgs = 0
    messages = dict()
    ms_total = dict()
    n=0
    
    total_all_messages = len(all_messages)*1.0
    
    for message in all_messages:
        n+=1
        if n%5000==0: 
            print('%.2f%%  -- Processing message %d: ' %( (n*100.0/total_all_messages), n ))
        text = message['text']
        mid  = message['messageID']
        uid  = message['user']
        gid  = message['groupID']
        date = message['date']
        tipo = message['msg_type']
        total_msgs += 1
        
        text = _process_string(text)
        
        if tipo == 'document': continue
        if len(text) < 150:
            continue

        isNew = True
        hashstring = mid
        for ID in messages.keys():
            text2 = messages[ID]['message']
            min_size = min(len(text), len(text2))
            max_difference = min(25, min_size/10)
            if abs(len(text) - len(text2)) < max_difference:
                score = compare_texts(text.lower(), text2.lower())
                if score >= 0.80:
                    isNew = False
                    hashstring = ID
                    break

        if isNew:
            messages[hashstring] = dict()
            messages[hashstring]['message'] = text
            messages[hashstring]['date']    = date
            messages[hashstring]['total']  = 0
            ms_total[hashstring]  = 0
            messages[hashstring]['users']   = set()
            messages[hashstring]['groups']  = set()
        
        if date < messages[hashstring]['date']:  messages[hashstring]['date'] = date
        messages[hashstring]['total']  += 1
        ms_total[hashstring] += 1
        messages[hashstring]['users'].add(uid) 
        messages[hashstring]['groups'].add(gid)
        
        if n%1000000==0: 
            print('Saving data after %d messages', n)
            data_file = join(path, 'data_most_shared_messages.txt')
            with open(data_file, 'w') as fout:
                print('MESSAGE_ID	DATE	#SHARES	#GROUPS	#USERS	#CONTENT', file=fout)
                n = 0
                for key in sorted(ms_total, key=ms_total.get, reverse=True):
                    n += 1
                    if n > max: break
                    
                    print('%s\t%s\t%d\t%d\t%d\t%s'%(key, messages[key]['date'], messages[key]['total'], len(messages[key]['users']), len(messages[key]['groups']), messages[key]['message']), file=fout)
                
        
        
        
    data_file = join(path, 'data_most_shared_messages.txt')
    with open(data_file, 'w') as fout:
        print('MESSAGE_ID	DATE	#SHARES	#GROUPS	#USERS	#CONTENT', file=fout)
        n = 0
        for key in sorted(ms_total, key=ms_total.get, reverse=True):
            n += 1
            if n > max: break
            
            print('%s\t%s\t%d\t%d\t%d\t%s'%(key, messages[key]['date'], messages[key]['total'], len(messages[key]['users']), len(messages[key]['groups']), messages[key]['message']), file=fout)
        
        
        
        
        
        

    
def get_top_images_from_text(all_messages, path, out_file, max=100):

    print('>>>>Get most shared images with messages containing keywords')
    total_urls = 0  
    total_msgs = 0
    media_dict = dict()
    ms_total = dict()
    n=0
    for message in all_messages:
        n+=1
        if n%5000==0: print('Message', n)
        text = message['text']
        text = process_text_for_latex(text)
        mid  = message['messageID']
        uid  = message['user']
        gid  = message['groupID']
        date = message['date']
        tipo = message['msg_type']
        file = message['is_media']
        filename = message['filename']
        try: hash = message['hashes']['phash']
        except: hash = filename
        
        if not hash : continue
        if len(hash) <= 2: continue
        
        total_msgs += 1
        

        if tipo.lower() == 'image': 
            if not hash: continue
            if hash.lower().strip() == 'none': continue
            if len(hash) < 5: continue
            
            isNew = True
            hashstring = hash
            for ID in media_dict.keys():
                score = compare_images(filename, ID)
                if score >= 0.80:
                    isNew = False
                    hashstring = ID
                    break

            if isNew:
                media_dict[hashstring] = dict()
                media_dict[hashstring]['hashstring'] = hashstring
                media_dict[hashstring]['filename'] = filename
                media_dict[hashstring]['messages'] = list()
                media_dict[hashstring]['date']    = date
                media_dict[hashstring]['end_date']    = date
                media_dict[hashstring]['total']  = 0
                ms_total[hashstring]  = 0
                media_dict[hashstring]['users']   = list()
                media_dict[hashstring]['groups']  = list()
            
            if date < media_dict[hashstring]['date']:  media_dict[hashstring]['date'] = date
            if date > media_dict[hashstring]['end_date']:  media_dict[hashstring]['end_date'] = date
            media_dict[hashstring]['total']  += 1
            ms_total[hashstring] += 1
            if uid not in  media_dict[hashstring]['users']:    media_dict[hashstring]['users'].append(uid) 
            if gid not in  media_dict[hashstring]['groups']:   media_dict[hashstring]['groups'].append(gid)
            if text not in media_dict[hashstring]['messages']: media_dict[hashstring]['messages'].append(text)
            
    out_file = out_file+'.txt'
    data_file = join(path, out_file)
    with open(data_file, 'w') as fout:
        #print('FILENAME	DATE	#SHARES	#GROUPS	#USERS	#CONTENT', file=fout)
        n = 0
        for key in sorted(ms_total, key=ms_total.get, reverse=True):
            n += 1
            if n > max: break
            item =  media_dict[key]
            json_string = json.dumps(item)
            print('%s'%(json_string), file=fout)
            #print('%s\t%s\t%d\t%d\t%d\t%s'%(key, media_dict[key]['date'], media_dict[key]['total'], len(media_dict[key]['users']), len(media_dict[key]['groups']), media_dict[key]['messages']), file=fout)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
 import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Carregar as mensagens do WhatsApp e textos de checagem de fatos
with open('mensagens.json', 'r', encoding='utf-8') as file:
    mensagens = json.load(file)

with open('textos_de_checagem.json', 'r', encoding='utf-8') as file:
    textos_de_checagem = json.load(file)

# Tokenização e remoção de stopwords
stop_words = set(stopwords.words('portuguese'))

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    return set(tokens)

# Função para calcular o índice de Jaccard entre dois conjuntos
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

# Iterar sobre as mensagens do WhatsApp
for mensagem in mensagens:
    mensagem_texto = preprocess_text(mensagem['texto'])
    max_similarity = 0.0
    most_similar_text = ''

    # Iterar sobre os textos de checagem de fatos
    for texto in textos_de_checagem:
        texto_preprocessado = preprocess_text(texto)
        similarity = jaccard_similarity(mensagem_texto, texto_preprocessado)

        # Atualizar se encontrarmos uma similaridade maior
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_text = texto

    # Adicionar campos ao dicionário da mensagem do WhatsApp
    mensagem['checagem_similar'] = most_similar_text
    mensagem['similaridade'] = max_similarity

# Salvar o resultado de volta no arquivo JSON
with open('mensagens_atualizadas.json', 'w', encoding='utf-8') as file:
    json.dump(mensagens, file, ensure_ascii=False, indent=2)
