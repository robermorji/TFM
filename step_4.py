
from nltk.corpus import stopwords
import regex
import re
import sys
import numpy as np
import random
from sklearn import svm
from sklearn.metrics import accuracy_score
import timeit
import os
import pandas as pd

def main():

        fichero_Hillary = open("Data/Hillary/Hillary.txt","r")
        fichero_Trump = open("Data/Trump/Trump.txt","r")
        fichero_Neutral = open("Data/Neutral/neutral.txt","r")

        random_hillary = {}
        random_trump = {}
        random_neutral = {}

        num_Hillary = 0
        num_Trump   = 0
        num_Neutral = 0
        vector_word = {}
        vector_word_reverse = {}

        lista_frases_hillary = {}
        lista_frases_hillary_reverse = {}
        lista_frases_trump   = {}
        lista_frases_trump_reverse   = {}
        lista_frases_neutral = {}
        lista_frases_neutral_reverse = {}
        lista_frases_fichero = {}
        lista_frases_fichero_reverse = {}

        # Creacion Vector Word Global
        line_count = 0
        line_count     = creacionVectorWordGlobal(fichero_Hillary,vector_word,vector_word_reverse,lista_frases_hillary,lista_frases_hillary_reverse,line_count)
        line_count     = creacionVectorWordGlobal(fichero_Trump,vector_word,vector_word_reverse,lista_frases_trump,lista_frases_trump_reverse,line_count)
        line_count     = creacionVectorWordGlobal(fichero_Neutral,vector_word,vector_word_reverse,lista_frases_neutral,lista_frases_neutral_reverse,line_count)


        #Creacion matrices train y test
        num_elem = 75 * 3
        train_x = np.zeros((num_elem,line_count))
        train_y = np.zeros(num_elem)

        test_y  = np.zeros(1)


        #Inicializo las matrices de Hillary, Trump, Neutral, y las frases que es mi test
        matriz_hillary =  np.zeros((100,line_count))
        matriz_trump   =  np.zeros((100,line_count))
        matriz_neutral =  np.zeros((30,line_count))



        dar_valor_matriz(matriz_hillary,vector_word,vector_word_reverse,lista_frases_hillary)
        dar_valor_matriz(matriz_trump,vector_word,vector_word_reverse,lista_frases_trump)
        dar_valor_matriz(matriz_neutral,vector_word,vector_word_reverse,lista_frases_neutral)
        random.seed()

        #Composicion del train
        for i in range (0,num_elem):
            insert_element_train = False
            while insert_element_train == False:
                n = random.randint(1,3)
                if n==1 and num_Hillary < 75:
                    fila = random.randint(0,99)
                    while fila in random_hillary.keys():
                        fila = random.randint(0,99)
                    random_hillary[fila] = 'True'
                    rellenar_matriz_x(train_x[i], matriz_hillary[fila])
                    train_y[i] = 1

                    num_Hillary = num_Hillary + 1
                    insert_element_train = True
                elif n==2 and num_Trump < 75:
                    fila = random.randint(0,99)
                    while fila in random_trump.keys():
                        fila = random.randint(1,99)
                    random_trump[fila] = 'True'
                    #print fila
                    rellenar_matriz_x(train_x[i], matriz_trump[fila])
                    train_y[i]= -1
                    num_Trump = num_Trump + 1
                    insert_element_train = True
                elif n==3 and num_Neutral < 75:
                    fila = random.randint(0,29)
                    #while fila in random_neutral.keys():
                    #    fila = random.randint(0,29)
                    #random_neutral[fila] = 'True'
                    rellenar_matriz_x(train_x[i], matriz_neutral[fila])
                    train_y[i] = 0
                    num_Neutral = num_Neutral + 1
                    insert_element_train = True

        #f = open("prueba_texto.txt","r")
        #limpiarPalabrasVacias(f,lista_frases_fichero)
        #dar_valor_matriz(matriz_frases,vector_word,lista_frases_fichero)
        #rellenar_matriz_x(test_x[0],matriz_frases[0])
        #print test_x[0]


        clf = svm.SVC(kernel='linear', tol=1e-4)
        entrenado = clf.fit(train_x, train_y)

        pathIsFileBag          = "Bag_of_Word/"
        numero_lineas_predicciones = 0
        contador_dias = 0
        week = 1
        array_predicciones = []
        count_Hillary = 0
        count_Trump = 0
        count_Neutral = 0

        for k in range (8,12):
            name_file_bag_of_words = "bag_of_words_"
            if k < 10:
                name_file_month = '2016-0'+format(k)
            else:
                name_file_month = '2016-'+format(k)
            for i in range (1,31):
                lista_frases_fichero = {}
                name_file = ""
                if i < 10:
                    name_file = name_file_bag_of_words + name_file_month +'-0'+format(i)+".csv"
                else:
                    name_file = name_file_bag_of_words + name_file_month +'-'+format(i) +".csv"
                print pathIsFileBag + name_file_bag_of_words

                if (os.path.isfile( pathIsFileBag + name_file)==True):
                    test = pd.read_csv( pathIsFileBag + name_file, encoding="utf_8", header=0,delimiter="\t",lineterminator='\n')

                    limpiarPalabrasVacias(test,lista_frases_fichero)
                    print len(lista_frases_fichero)

                    test_x  = np.zeros((len(test['text']),line_count))
                    matriz_frases  =  np.zeros((len(test['text']),line_count))

                    print "Fichero: "+ pathIsFileBag + name_file
                    print "Dando valor a la  Matriz: " + format(i)
                    #print vector_word
                    #sys.exit()
                    print "Dando valor a la matriz de test"
                    dar_valor_matriz(matriz_frases,vector_word,vector_word_reverse,lista_frases_fichero)

                    for i in range (len(test['text'])):
                        print "Rellenando la frase clasificador: "+format(i)
                        rellenar_matriz_x(test_x[i],matriz_frases[i])
                        prediccion = entrenado.predict(test_x[i])
                        array_predicciones.append(prediccion)

                else:
                    print "No existe el fichero"
                contador_dias += 1
                if contador_dias % 7==0:
                    path = "Votos/votos_semana_"+format(week)+".csv"
                    fichero_semanal = open(path,"w")
                    fichero_semanal.write("candidato,count\n")
                    for contador in range(len(array_predicciones)):
                        if array_predicciones[contador] == 1:
                            count_Hillary += 1
                        elif array_predicciones[contador] == -1:
                            count_Trump += 1
                        else:
                            count_Neutral += 1
                    week+=1
                    fichero_semanal.write("hillary,"+format(count_Hillary)+"\n")
                    fichero_semanal.write("trump,"+format(count_Trump)+"\n")
                    fichero_semanal.write("neutral,"+format(count_Neutral)+"\n")
                    count_Hillary = 0
                    count_Trump = 0
                    count_Neutral = 0
                    array_predicciones = []
                    fichero_semanal.close()
                print "Contador dias: " + format(contador_dias) + "\n"

def rellenar_matriz_x(conjunto_x, array):
    for i in range(len(array)):
        conjunto_x[i] = array[i]


def dar_valor_matriz(matriz,vector_word,vector_word_reverse,lista_frases):
     for key_fila, lista in lista_frases.items():
        for elemento_lista in lista:
            if elemento_lista in vector_word.values():
                posicion_columna_matriz = vector_word_reverse[elemento_lista]
                matriz[key_fila][posicion_columna_matriz] = 1
                #print format(key_fila) + " - " + format(posicion_columna_matriz)

def limpiarPalabrasVacias(fichero, lista_frases):
    line_count = 0

    for line in range(len(fichero['id'])):
         letters_only = re.sub("[^@a-zA-Z]"," ",format(fichero['text'][line]))
         letters_only = re.sub("@\w*","",letters_only )
         lower_case = letters_only.lower()
         words = lower_case.split()
         lista_frases[line_count] = []
         lista_aux = []
         element_count = 0
         for w in words:
             if not w in stopwords.words("english"):
                lista_aux.append(w)
                element_count+=1

         lista_frases[line_count] = lista_aux
         line_count = line_count + 1



def creacionVectorWordGlobal(fichero, vector_word, vector_word_reverse, lista_frases,lista_frases_reverse,word_count):
     line_count = 0

     #insert_element = True

     for line in fichero:
         #print " " + line[i]
         letters_only = re.sub("[^@a-zA-Z]"," ",line)
         letters_only = re.sub("@\w*","",letters_only )
         lower_case = letters_only.lower()
         words = lower_case.split()
         lista_frases[line_count] = []
         lista_aux = []
         element_count = 0
         for w in words:
             if not w in stopwords.words("english"):
                 lista_aux.append(w)
                 element_count+=1
                 if not w in vector_word.values():
                    vector_word[word_count] = w
                    vector_word_reverse[w] = word_count
                    word_count += 1
         lista_frases[line_count] = lista_aux
         line_count = line_count + 1

     return word_count


if __name__ == "__main__":
    main()
