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
import operator

def create_file(file_save_text,file_bag_of_words, pathIsFileSave,\
 pathIsFileBag, pathIsFileJSON):
    save_text = None
    diccionario = {}
    asigna_primer_nombre = True
    contador_dias = 3
    for k in range (11,12):
        name_file = ""
        if k < 10:
            name_file_month = '2016-0'+format(k)
        else:
            name_file_month = '2016-'+format(k)
        for i in range (2,31):
            if i < 10:
                name_file = name_file_month +'-0'+format(i)
                if asigna_primer_nombre == True:
                    week = name_file
                    asigna_primer_nombre = False
            else:
                name_file = name_file_month +'-'+format(i)
                if asigna_primer_nombre == True:
                    week = name_file
                    asigna_primer_nombre = False
            if contador_dias%7==0:
                name_file_save_text = ""
                name_file_save_text = file_save_text + week +"_"+name_file + ".csv"
                if (os.path.isfile( pathIsFileSave + name_file_save_text )==True):
                    os.remove( pathIsFileSave + name_file_save_text)
                save_text = open( pathIsFileSave + name_file_save_text,"w" )
                elementos = sorted(diccionario.items(), key=operator.itemgetter(1),\
                reverse=True)
                save_text.write("word,count\n")
                for tag, count in elementos:
                    save_text.write(format(tag)+","+format(count)+"\n")
                print("\n")
                save_text.close()
                diccionario = {}
                asigna_primer_nombre = True
                print ("Semana: " + week)
                week = ""
            file_json = name_file + ".json"
            name_file_bag_of_words = file_bag_of_words+name_file+".csv"
            contador_dias = contador_dias + 1
            if (os.path.isfile( pathIsFileJSON + file_json )==True):
                if (os.path.isfile( pathIsFileBag + name_file_bag_of_words )==True):
                    os.remove( pathIsFileBag + name_file_bag_of_words)
                bag_of_words = open( pathIsFileBag + name_file_bag_of_words, "w" )
                bag_of_words.write("id\ttext\n")
                bag_of_words.close()
                count_number_tweet(name_file_bag_of_words, file_json,\
                pathIsFileBag, pathIsFileJSON)
                read_file_csv( pathIsFileBag, name_file_bag_of_words, diccionario)
                print diccionario


#Funcion encargada de  leer fichero csv
#@param pathIsFileBag: Ruta donde se guardaran las bag_of_words
#@param name_file_bag_of_words: Nombre del fichero
#@diccionario de datos que modifico
#return: void
def read_file_csv(pathIsFileBag, name_file_bag_of_words,diccionario):
    train = pd.read_csv( pathIsFileBag + name_file_bag_of_words, encoding="utf_8", header=0,delimiter="\t",lineterminator='\n')
    vectorizer = CountVectorizer(analyzer = "word", tokenizer = None,preprocessor = None,
    stop_words = None,max_features = 100,ngram_range=(2, 2))
    array_words = []
    array_words_double = []

    print "Creando fichero "+name_file_bag_of_words
    for i in range(len(train['id'])):
        print("read_file: " + format(i) + " - " + format(len(train['id'])))

        letters_only = re.sub("[^@a-zA-Z]",           # The pattern to search for
                          " ",                   # The pattern to replace it with
                          format(train['text'][i]))  # The text to search
        letters_only = re.sub("@\w*","",           # The pattern to search for
                          letters_only )  # The text to search
        lower_case = letters_only.lower()        # Convert to lower case
        words = lower_case.split()
        words = [w for w in words if not w in stopwords.words("english")]
        cont = 0
        double=""

        #Create unigram and bigrams
        for w in words:
            array_words.append(w)
            if cont == 0:
                ant = w
                double = ant
                cont = cont + 1
            else:
                act = w
                double = ant + " " + act
                array_words_double.append(double)
                ant = act
                double = ""
                cont = cont + 1
    train_data = vectorizer.fit_transform(array_words_double)
    train_data = train_data.toarray()
    vocab = vectorizer.get_feature_names()
    dist = np.sum(train_data, axis=0)
    for tag, count in zip(vocab, dist):
        if tag in diccionario.keys():
            diccionario[tag] = diccionario[tag] + count
        else:
            diccionario[tag] = count
#Limpieza de datos
def clear_date(text):
    text = str(regex.sub(u"(\u2018|\u2019|\u0022|\u0027|\u0060|\u00B4|\u201C|\u201D)", "", text.encode('ascii', 'ignore')))
    text = str(regex.sub(u"(\n)", "", text.encode('ascii', 'ignore')))
    text = str(regex.sub(',', "", text.encode('ascii', 'ignore')))
    return text

# Recorre el archivo json lo limpia y me quedo con lo que me interesa en un
# diccionari ode datos
def count_number_tweet (name_file_bag_of_words,file_json,\
pathIsFileBag,pathIsFileJSON ):
        tweets_general = {}
        with open(pathIsFileJSON + file_json) as data_file:
            data = json.load(data_file)
            for i in range(len(data)):
                tweets_general = { i:{
                            'text' :(format(data[i]['text'])),
                            'location':(data[i]['user']['location']),
                            'name':  (data[i]['user']['name']),
                            'time_zone': (format(data[i]['user']['time_zone'])),
                            'created_at':(format(data[i]['created_at'])),
                            'geo': (format(data[i]['geo'])),
                            'id_tweet':(format(data[i]['id_str']))
                        }
                }
                bag_of_words = open( pathIsFileBag + name_file_bag_of_words, "a+r")
                bag_of_words.write(format(tweets_general[i]['id_tweet'])+"\t"+
                clear_date(tweets_general[i]["text"])+"\n")
