import json
import regex
import schedule
import time
import os
import datetime
from pprint import pprint
import pandas as pd
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import sys

def create_file(file_save_text,pathIsFileSave,pathIsFileJSON):
    save_text = None

    for k in range (11,12):
        name_file = ""

        if k < 10:
            name_file_month = '2016-0'+format(k)
        else:
            name_file_month = '2016-'+format(k)
        for i in range (2,31):

            name_geolocation = file_save_text
            if i < 10:
                name_file = name_file_month +'-0'+format(i)
                name_geolocation = name_geolocation + name_file
            else:
                name_file = name_file_month +'-'+format(i)
                name_geolocation = name_geolocation + name_file
            file_json = name_file + ".json"
            name_geolocation = name_geolocation+".csv"


            if (os.path.isfile( pathIsFileJSON + file_json )==True):
                if (os.path.isfile( pathIsFileSave + file_save_text )==True):
                    os.remove( pathIsFileSave + file_save_text)

                print pathIsFileSave + name_geolocation
                parse_geolocation = open(pathIsFileSave + name_geolocation, "w" )
                parse_geolocation.write("id\tlocation\ttime_zone\tgeo\n")
                parse_geolocation.close()

                count_number_tweet(name_geolocation, file_json,\
                pathIsFileSave, pathIsFileJSON)

def clear_date(text):
    text = str(regex.sub(u"(\u2018|\u2019)", "'", text.encode('ascii', 'ignore')))
    text = str(regex.sub(u"(\n)", "", text.encode('ascii', 'ignore')))
    text = str(regex.sub(',', "", text.encode('ascii', 'ignore')))
    return text

#Cuenta el numero de tweet
def count_number_tweet(name_file_geolocation,file_json,pathIsFileSave,pathIsFileJSON):
        with open(pathIsFileJSON+file_json) as data_file:
            data = json.load(data_file)
            for i in range(len(data)):
                tweets_general = { i:{
                                #'text' :(format(data[i]['text'])),
                                'location':(data[i]['user']['location']),
                                'name':  (data[i]['user']['name']),
                                'time_zone': (format(data[i]['user']['time_zone'])),
                                'created_at':(format(data[i]['created_at'])),
                                'geo': (format(data[i]['geo'])),
                                'id_tweet':(format(data[i]['id_str']))
                            }
                }
                geolocation = open(pathIsFileSave + name_file_geolocation, "a+r")

                geolocation.write(format(tweets_general[i]['id_tweet'])+"\t"+clear_date(tweets_general[i]["location"])+"\t"+
                clear_date(tweets_general[i]["time_zone"])+"\t"+clear_date(tweets_general[i]["geo"])+"\n")
