import pandas as panda
import sys
import operator



def porcentaje_valores(dictionary_stastic, numero_registros):
    suma = 0
    for key,value in dictionary_stastic.iteritems():
            porcentaje = ( dictionary_stastic[key] * 100 ) / float(numero_registros)
            dictionary_stastic[key] = round(porcentaje,2)
            suma = suma + dictionary_stastic[key]
    print suma



def function_dictionary_time(dictionary_stastic,time_zone, pos_encontrado, numero_registros):
    if pos_encontrado == True:
        if dictionary_stastic.has_key(time_zone):
            dictionary_stastic[time_zone]=\
            dictionary_stastic[time_zone] + 1
        else:
            dictionary_stastic[time_zone] = 1
        numero_registros = numero_registros + 1
    return numero_registros

def function_dictionary(dictionary_stastic,array_location, pos_encontrado, numero_registros):
    if pos_encontrado != -1:
        if dictionary_stastic.has_key(array_location[pos_encontrado]):
            dictionary_stastic[array_location[pos_encontrado]]=\
            dictionary_stastic[array_location[pos_encontrado]] + 1

        else:
            dictionary_stastic[array_location[pos_encontrado]] = 1
        numero_registros = numero_registros + 1
    return numero_registros

def search_location( array_location, full_name_state, name_state):
    pos_encontrado = -1
    for i in range ( len (array_location) ):
        if not full_name_state.has_key(array_location[i]):
            if name_state.has_key(array_location[i]):
               array_location[i] = name_state[array_location[i]]
               pos_encontrado = i
        else:
            pos_encontrado = i

    return pos_encontrado

def search_time_zone(time_zone,data_time):
    pos_encontrado = False
    if data_time.has_key(time_zone):
            pos_encontrado = True

    return pos_encontrado

def read_file_csv(name_file_geolocation,full_name_state, name_state,\
time_zone, coordinate, pathIsFileCSV, pathIsFileJSON, dictionary_stastic,\
numero_registros, estadistico):
    geolocation = panda.read_csv(pathIsFileCSV + name_file_geolocation, error_bad_lines=False,encoding="utf_8", header=0,delimiter="\t",lineterminator='\n')
    geolocalizados = 0
    geolocalizados_time = 0
    nulos = 0
    total_tweets = 0

    with open ( pathIsFileJSON + name_state ) as name:
        data_state = js.load(name)
    with open ( pathIsFileJSON + full_name_state ) as full_name:
        full_data_state = js.load(full_name)
    with open ( pathIsFileJSON + time_zone ) as time:
        data_time = js.load(time)

    total_tweets = len(geolocation)
    for i in range(len(geolocation)):
        array_location = []

        if not panda.isnull(geolocation["location"][i]):
            location = geolocation["location"][i]
        else:
            location = ""

        if  location:
            location = format(location)
            array_location = location.split(" ")
            pos_encontrado = search_location(array_location,  full_data_state, data_state)

            if pos_encontrado != -1:
                numero_registros = function_dictionary( dictionary_stastic,array_location, pos_encontrado, numero_registros)
                geolocalizados = geolocalizados + 1
                if not panda.isnull(geolocation["time_zone"][i]):
                    time_zone = geolocation["time_zone"][i]
                if time_zone != "None":
                    geolocalizados_time = geolocalizados_time + 1
            else:
                if not panda.isnull(geolocation["time_zone"][i]):
                    time_zone = geolocation["time_zone"][i]

                if time_zone != "None":
                    pos_encontrado = search_time_zone(time_zone,data_time)
                    numero_registros = function_dictionary_time( dictionary_stastic,time_zone, pos_encontrado,  numero_registros)
                    geolocalizados_time = geolocalizados_time + 1
                else:
                    nulos = nulos + 1
        else:
            if not panda.isnull(geolocation["time_zone"][i]):
                time_zone = geolocation["time_zone"][i]

            if time_zone != "None":
                pos_encontrado = search_time_zone(time_zone,data_time)
                numero_registros= function_dictionary_time( dictionary_stastic,time_zone, pos_encontrado, numero_registros)
                geolocalizados_time = geolocalizados_time + 1
            else:
                nulos = nulos + 1

    estadistico['geolocalizados'] = estadistico['geolocalizados'] + geolocalizados
    estadistico['geolocalizados_time'] = estadistico['geolocalizados_time'] + geolocalizados_time
    estadistico['nulos'] = estadistico['nulos'] + nulos
    estadistico['total_tweets'] = estadistico['total_tweets'] + total_tweets
    estadistico['total_tweets_semanales'] = estadistico['total_tweets_semanales'] + total_tweets
    return numero_registros
