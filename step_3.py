import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

import sys
import os
from  os import walk


def word_feats(words):
    return dict([(word, True)for word in words])

#print movie_reviews.fileids("pos")

Hillary = "/home/roberto/Escritorio/Proyecto/Data/election/Hillary/"
Trump = "/home/roberto/Escritorio/Proyecto/Data/election/Trump/"
Neutral = "/home/roberto/Escritorio/Proyecto/Data/election/Neutral/"


for (path, ficheros, archivos) in walk(Hillary):
    #print archivos
    posids = "pos/"+archivos[0]


for (path, ficheros, archivos) in walk(Trump):
    #print archivos
    negids = "neg/"+archivos[0]


for (path, ficheros, archivos) in walk(Neutral):
    #print archivos
    neutralids = "neu/"+archivos[0]


#negids = movie_reviews.fileids('pos')
#posids = movie_reviews.fileids('neg')


reader = nltk.corpus.CategorizedPlaintextCorpusReader(\
'Data/election/',\
r'.*\.txt', cat_pattern=r'(\w+)/*')
posids = reader.fileids('Hillary')
negids = reader.fileids('Trump')
neutralids = reader.fileids('Neutral')

print negids
print posids
print neutralids

negfeats = [(word_feats(reader.words(fileids=[f])), 'Trump') for f in negids]
posfeats = [(word_feats(reader.words(fileids=[f])), 'Hillary') for f in posids]
neufeats = [(word_feats(reader.words(fileids=[f])), 'Neutral') for f in neutralids]
#print neufeats

#sys.exit()

#negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
#posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

print len(negfeats)
print len(posfeats)

listas = list(posfeats[0])
hillary_list = []
for key,values in listas[0].items():
    list_aux = ()
    diccionario = {}
    diccionario[key] = format(values)
    list_aux = (diccionario,"Hillary")
    hillary_list.append(list_aux)

#hillary_list.append(listas[1])
#print hillary_list
listas = list(negfeats[0])

trump_list = []
for key,values in listas[0].items():
    list_aux = ()
    diccionario = {}
    diccionario[key] = format(values)
    list_aux = (diccionario,"Trump")
    trump_list.append(list_aux)

#trump_list.append(listas[1])
#print trump_list

#print len(trump_list)

listas = list(neufeats[0])
neutral_list = []
for key,values in listas[0].items():
    list_aux = ()
    diccionario = {}
    diccionario[key] = format(values)
    list_aux = ( diccionario, "Neutral")
    neutral_list.append(list_aux)

neutral_list.append(listas[1])
#print neutral_list
#sys.exit()

#print trump_list
#sys.exit()
negcutoff = len(trump_list)*3/4
poscutoff = len(hillary_list)*3/4
neucutoff = len(neutral_list)*3/4

#print negcutoff
#print poscutoff
#print neucutoff

trainfeats = trump_list[:negcutoff] + hillary_list[:poscutoff]
testfeats = trump_list[negcutoff:] + hillary_list[poscutoff:]
print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))
#print trainfeats
classifier = NaiveBayesClassifier.train(trainfeats)
print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
classifier.show_most_informative_features()
