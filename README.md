# TFM
# Elecciones USA

## Introducción
El problema que planteo en mi trabajo se desarrolla en un contexto de incertidumbre cambiante  en el cual no se sabe qué resultados se va producir  debido a que cualquier hecho ocurrido a lo largo de la realización de este análisis podría desencadenar una variación completa de mis resultados. No es un contexto estático ya que como ya veremos a lo largo del paso de los meses los distintos eventos que se producen provoca el cambio de los resultados en nuestro análisis.


La motivación que me involucra en este proyecto era analizar el desarrollo de todas las elecciones de USA, pudiendo conseguir trazar los distintos eventos que se produjeron y como todos esos hechos le afectaron a los americanos en su modo de pensar. Este trabajo puede servir también de estudio del pensamiento de la sociedad americana debido a que como veremos más adelante conseguiremos  averiguar qué temas le interesan más a la sociedad ya que son de los que más hablan en la red  e incluso son los que más mencionan para que los distintos candidatos respondan sobre ellos, por ejemplo, una cosa curiosa y razonable es que cuando fue el atentado de New York la gente empezó a preguntar a los distintos candidatos sobre el ISIS y cómo lo iban a combatir.


En mi trabajo lo que voy  a realizar es un análisis de todo lo acontecido en estos tres meses de dura competencia para alcanzar la casa blanca, para ello me voy a ayudar de la api  de twitter para  conseguir, con una serie de script que he realizado, crearme el dataSet que voy a utilizar en mis experimentos, este DataSet fue recopilado desde el 2 de agosto de 2016 hasta el 14-11-2016 durante tres meses el script automáticamente me extraía los tweets en formato JSON y me los almacenaban en ficheros ordenados por día.


Una vez obtenido el DataSet lo que realizo es un BagOfWords que consiste en realizar un estudio sobre la frecuencia de las palabras que más aparecen en los textos de mi dataSet, empecé realizandolo por una palabra ( unigrama ) pero no me discriminaba eventos que surgían en esa semana por tanto decidí utilizar un conjunto de dos palabras ( bigramas ) todas estas frecuencias son representados mediante una serie de gráficas por mathlab.


Posteriormente lo que realizo es una geolocalización de donde se han realizado los distintos tweets de mi dataSet en mi caso he conseguido geolocalizar un 75% de los tweets, extrayendo también la propiedad de localización por aproximación, que aunque no consiga exactamente el lugar exacto consigo geolocalizar mediante la zona horaria, dandome una aproximación de desde donde se ha enviado el tweets y puedo más o menos situarlo en alguna comunidad. Una vez geolocalizados todos los tweets de los que dispongo pinto un mapa de los Estados Unidos, con un script realizado en mathlab, en él dibujo circunferencias para poder observar  las zonas más influyentes en los que se han producido emisiones de tweets.


A continuación, realizo el trabajo de predicción en el cual utilizo dos algoritmos de aprendizaje automático: bayesiano y  Support Vector Machine, comparo esos resultados y hago un análisis del rendimiento de cada uno obteniendo un accuracy distinto para cada uno de ellos y quedandome con el mejor.


Finalmente cojo todos los textos de mis tweets y los paso por mi modelo de predicción haciendo un clasificador de tres clases  en el cual distingo votos positivos de Hillary, votos positivos para Trump ( los que son negativos para Hillary ) y Neutrales.


El objetivo final de todos estos experimentos es  hacer un seguimiento y entender  más profundamente el desarrollo de las elecciones de USA. Podremos ver en todo momento qué eventos hacen cambiar la opinión de todos los votantes y que pensamiento tenían cada elector en sus votos.
