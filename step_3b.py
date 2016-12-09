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
from sklearn.naive_bayes import GaussianNB
from imblearn.over_sampling import SMOTE
from collections import Counter
def main(n_time):

        sm = SMOTE(random_state=42)
        fichero_Hillary = open("Data/Hillary/Hillary.txt","r")
        fichero_Trump = open("Data/Trump/Trump.txt","r")
        fichero_Neutral = open("Data/Neutral/neutral.txt","r")

        random_hillary = {}
        random_trump = {}
        random_neutral = {}

        num_Hillary = 0
        num_Trump   = 0
        num_Neutral = 0
        vector_word = []

        lista_frases_hillary = {}
        lista_frases_trump   = {}
        lista_frases_neutral = {}

        line_count = 0
        line_count     += matriz_candidatos(fichero_Hillary,vector_word,lista_frases_hillary)
        line_count     += matriz_candidatos(fichero_Trump,vector_word,lista_frases_trump)
        line_count     += matriz_candidatos(fichero_Neutral,vector_word,lista_frases_neutral)

        num_elem = 165
        train_x = np.zeros((num_elem,line_count))
        train_y = np.zeros(num_elem)
        test_x  = np.zeros((65,line_count))
        test_y  = np.zeros(65)

        matriz_hillary =  np.zeros((100,line_count))
        matriz_trump   =  np.zeros((100,line_count))
        matriz_neutral =  np.zeros((30,line_count))

        dar_valor_matriz(matriz_hillary,vector_word,lista_frases_hillary)
        dar_valor_matriz(matriz_trump,vector_word,lista_frases_trump)
        dar_valor_matriz(matriz_neutral,vector_word,lista_frases_neutral)

        random.seed()
        lista_aleatoria_candidato = [1,2,3]
        #Composicion del train
        for i in range (0,num_elem):
            insert_element_train = False
            while insert_element_train == False:
                n = random.choice(lista_aleatoria_candidato)
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
                    rellenar_matriz_x(train_x[i], matriz_trump[fila])
                    train_y[i]= -1
                    num_Trump = num_Trump + 1
                    insert_element_train = True
                elif n==3 and num_Neutral < 15:
                    fila = random.randint(0,29)
                    while fila in random_neutral.keys():
                        fila = random.randint(0,29)
                    random_neutral[fila] = 'True'
                    rellenar_matriz_x(train_x[i], matriz_neutral[fila])
                    train_y[i] = 0
                    num_Neutral = num_Neutral + 1
                    insert_element_train = True
            if (num_Hillary == 75):
                lista_aleatoria_candidato.remove(0)
            if (num_Trump == 75):
                posicion = len(lista_aleatoria_candidato)/2
                lista_aleatoria_candidato.remove(posicion)
            if (num_Neutral == 15):
                posicion = len(lista_aleatoria_candidato)
                lista_aleatoria_candidato.remove(posicion - 1)

        #print len(train_x[1])
        #sys.exit
        #for i in range ( len ( train_x[1] ) ):
        #    print train_x[1][i]
        #print train_y[1]
        #Composicion del test
        #sys.exit()
        print('Resampled dataset shape {}'.format(Counter(train_y)))
        #train_x_overSampling, train_y_overSampling = sm.fit_sample(train_x, train_y)
        #print('Resampled dataset shape {}'.format(Counter(train_y_overSampling)))
        sys.exit()
        num_Hillary = 0
        num_Trump = 0
        num_Neutral = 0

        for i in range (0,65):
            insert_element_test = False
            while insert_element_test == False:
                n = random.randint(1,3)
                if n==1 and num_Hillary < 25:
                    fila = random.randint(0,99)
                    while fila in random_hillary.keys():
                        fila = random.randint(0,99)
                    random_hillary[fila] = 'True'
                    rellenar_matriz_x(test_x[i], matriz_hillary[fila])
                    test_y[i] = 1
                    num_Hillary = num_Hillary + 1
                    insert_element_test = True
                elif n==2 and num_Trump < 25:
                    fila = random.randint(0,99)
                    while fila in random_trump.keys():
                        fila = random.randint(0,99)
                    random_trump[fila] = 'True'
                    rellenar_matriz_x(test_x[i], matriz_trump[fila])
                    test_y[i] = -1
                    num_Trump = num_Trump + 1
                    insert_element_test = True
                elif n==3 and num_Neutral < 15:
                    fila = random.randint(0,29)
                    while fila in random_neutral.keys():
                        fila = random.randint(0,29)
                    random_neutral[fila] = 'True'
                    rellenar_matriz_x(test_x[i], matriz_neutral[fila])
                    test_y[i] = 0
                    num_Neutral = num_Neutral + 1
                    insert_element_test = True



        #if n_time == 0:
        #   os.remove("resultados_accuracy_bayesiano.csv")
        #   f = open("resultados_accuracy_bayesiano.csv","w")
        #   f.write("execute,resultados_accuracy_bayesiano\n")
        #else:
        #   f = open("resultados_accuracy_bayesiano.csv","a")

        if n_time == 0:
           if (os.path.isfile("resultados_accuracy_SVM.csv")==True):
               os.remove("resultados_accuracy_SVM.csv")
           f = open("resultados_accuracy_SVM.csv","w")
           f.write("execute,resultados_accuracy_SVM\n")
        else:
           f = open("resultados_accuracy_SVM.csv","a")



        #for i in range(1,100,10):
        #    tolerancia = i/float(1000)
        #    print tolerancia
        clf = svm.SVC(kernel='linear', tol=1e-2)
        prediccion = clf.fit(train_x, train_y).predict(test_x)
        #prediccion = clf.predict(test_x).predict(test_x)
        #print prediccion
        #gnb = GaussianNB()
        #prediccion = gnb.fit(train_x, train_y).predict(test_x)
        accuraccy_test  = accuracy_score(test_y,prediccion,normalize=True)
        f.write(format(n_time) + "," + format(accuraccy_test)+"\n")
        #f.write(format(test_y)+"\n")

            #prediccion_train = clf.predict(train_x)

            #accuraccy_train  = accuracy_score(train_y,prediccion_train,normalize=True)
            #f.write("\n####### Accuracy Train #########\n")
            #f.write(format(accuraccy_train)+"\n")
            #f.write(format(train_y)+"\n")
        print format(accuraccy_test) + "Iteracion numero:" + format(n_time)

        f.close()
        return accuraccy_test

def rellenar_matriz_x(train_x, array):
    for i in range(len(array)):
        train_x[i] = array[i]

def dar_valor_matriz(matriz,vector_word,lista_frases):
   for fila_frase in range(len(lista_frases)):
     for columna_frase in range(len(lista_frases[fila_frase])):
         for columna_vector in range(len(vector_word)):
            if vector_word[columna_vector] == lista_frases[fila_frase][columna_frase]:
                 matriz[fila_frase][columna_vector] = 1

def matriz_candidatos(fichero, vector_word, lista_frases):
     line_count = 0
     word_count = 0
     insert_element = True


     for line in fichero:
         #print " " + line[i]
         letters_only = re.sub("[^@a-zA-Z]"," ",line)
         letters_only = re.sub("@\w*","",letters_only )
         lower_case = letters_only.lower()
         words = lower_case.split()
         lista_frases[line_count] = []
         for w in words:
             if not w in stopwords.words("english"):
                 lista_frases[line_count].append(w)
                 for i in range(len(vector_word)):
                     if vector_word[i] == w:
                        insert_element = False
                 if insert_element == True:
                    vector_word.append(w)
                    word_count = word_count + 1
                 else:
                    insert_element = True

         line_count = line_count + 1

     return word_count


if __name__ == "__main__":
    accuracy = 0
    for n_time in range (100):
        accuracy += main(n_time)

    accuracy = accuracy / 100.0
    print "Total Accuracy: " + format(accuracy)
    f = open("resultados_accuracy_bayesiano.csv","a")
    f.write("Total,"+ format(accuracy))
    f.close()
