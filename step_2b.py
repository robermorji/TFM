from lib import normalizacion_geo as geo
import json as js
import os

def main():

    #Inicializacion de todos los parametros
    numero_registros = 0
    dictionary_stastic = {}
    full_name_state = "full_name_state.json"
    name_state = "name_state.json"
    time_zone = "time_zone.json"
    coordinate = "coordinate.json"
    file_save_text = "State_Save_Week_"
    file_global_event_text = "Global_Event_Week"
    pathIsFileCSV = "Geolocation/"
    pathIsFileSave = "Stastic/"
    pathIsFileJSON = "json/"
    pathIsFileGlobalEvent = "GlobalEvent/"
    pathIsFileStastic = "File_Stastic/"
    block_stastic = "file_static.csv"
    estadistico = {}
    estadistico['total_tweets'] = 0
    estadistico['geolocalizados'] = 0
    estadistico['geolocalizados_time'] = 0
    estadistico['nulos'] = 0
    estadistico['total_tweets'] = 0
    estadistico['total_tweets_semanales'] = 0

    week = ""
    asigna_primer_nombre = True
    contador_dias = 3

    # Preparacion de los ficheros para guardarlos y tenerlos preparados
    # para lanzar la aplicacion de pintar los diagramas
    with open( pathIsFileJSON + coordinate ) as coord:
        data_coord = js.load( coord )

    for  k in range (8,12):
        name_file_month = ""
        if k < 10:
            name_file_month = '2016-0'+format(k)
        else:
            name_file_month = '2016-'+format(k)
        for i in range (1,31):
            if k==11 and i == 14:
                break;
            name_file_geolocation = "geolocation_"
            name_file_stastic = "stastic_"
            name_file_global_events = "global_event_"
            if i < 10:
                name_file_geolocation = name_file_geolocation +\
                                        name_file_month +\
                                        '-0'+format(i)
                name_file_stastic = name_file_stastic +\
                                    name_file_month +\
                                    '-0'+format(i)
                if asigna_primer_nombre == True:
                    week = name_file_stastic
                    asigna_primer_nombre = False
            else:
                name_file_geolocation = name_file_geolocation +\
                                        name_file_month +'-'+\
                                        format(i)
                name_file_stastic = name_file_stastic +\
                                    name_file_month +'-'+\
                                    format(i)
                if asigna_primer_nombre == True:
                    week = name_file_stastic
                    asigna_primer_nombre = False


            print pathIsFileCSV + name_file_geolocation
            name_file_geolocation = name_file_geolocation + ".csv"
            if (os.path.isfile( pathIsFileCSV + name_file_geolocation )==True):
                numero_registros = geo.read_file_csv(name_file_geolocation,full_name_state,
                                                name_state,time_zone, coordinate,
                                                pathIsFileCSV,pathIsFileJSON,dictionary_stastic,
                                                numero_registros, estadistico)
            print numero_registros

            if contador_dias%7==0:
                geo.porcentaje_valores(dictionary_stastic,numero_registros)
                sorted_dictionary = sorted(dictionary_stastic.items(),
                                key=operator.itemgetter(1),
                                reverse=True)
                name_file_save_text = ""
                name_file_save_text = file_save_text + week+"_"+name_file_stastic+".csv"
                if (os.path.isfile( pathIsFileSave + name_file_save_text )==True):
                    os.remove( pathIsFileSave + name_file_save_text)
                save_text = open( pathIsFileSave + name_file_save_text,"w" )

                elementos = sorted_dictionary
                save_text.write("zone,perc,lat,lon\n")
                for tag, count in elementos:
                    save_text.write(format(tag)+","+format(count)+ "," +
                    data_coord[tag]+"\n")
                numero_registros = 0
                asigna_primer_nombre = True
                print ("Semana: " + week)

                name_file_global_event_text = "Tweets_Semanales_Totales.csv"

                if (os.path.isfile( pathIsFileGlobalEvent + name_file_global_event_text )==False):
                    GlobalEvent_text = open( pathIsFileGlobalEvent + name_file_global_event_text,"w" )
                else:
                    GlobalEvent_text = open( pathIsFileGlobalEvent + name_file_global_event_text,"a" )

                if os.stat(pathIsFileGlobalEvent + name_file_global_event_text).st_size == 0:
                   GlobalEvent_text.write("semana, numero_totales_tweets\n")

                GlobalEvent_text.write(week + "," +format(estadistico['total_tweets_semanales'])+'\n')
                GlobalEvent_text.close()
                week = ""
                print "Total tweets semanales: " + format(estadistico['total_tweets_semanales'])
                estadistico['total_tweets_semanales'] = 0
            contador_dias = contador_dias + 1
            print "Total tweets: " + format(estadistico['total_tweets'])
            print "Geolocalizados: " + format(estadistico['geolocalizados'])
            print "Geolocalizados por tiempo: " + format(estadistico['geolocalizados_time'])
            print "Nulos: " + format(estadistico['nulos'])



    File_Stastic = open(pathIsFileStastic + block_stastic, "w")

    File_Stastic.write("Total_tweets" + "\t" + "Geolocalizados" +
    "\t" + "Geolocalizados por time_zone" + "\t" + "Nulos " )

    File_Stastic.write(format(estadistico['total_tweets']) +"\t"\
    + format(estadistico['geolocalizados']) + "\t"\
    + format(estadistico['geolocalizados_time']) + "\t"\
    + format(estadistico['nulos']))

    File_Stastic.close()

if __name__ == "__main__":
    main()
