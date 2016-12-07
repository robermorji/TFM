close all;
name = '/home/roberto/Escritorio/Proyectos/Elecciones_USA/GlobalEvent/Tweets_Semanales_Totales.csv';
cell = tdfread(name,',');
plot( cell.semana,cell.numero_totales_tweets)
title('Numero Totales de tweets');
xlabel('Semanas')
ylabel('Numero total de tweets');
legend('Numero totales de tweets');