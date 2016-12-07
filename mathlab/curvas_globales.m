close all;
name = '/home/roberto/Escritorio/Proyectos/Elecciones_USA/GlobalEvent/';
list = dir(name);

tam_elemento_1 = 1;

vector = zeros(1,14);

for c=3:length(list)
    filename=sprintf('/home/roberto/Escritorio/Proyectos/Elecciones_USA/GlobalEvent/%s',list(c).name);
    title_map = strsplit(filename,'.');
    title_map = strsplit(title_map{1},'/');
    h = figure('Name',title_map{8},'NumberTitle','off');
    cell = tdfread(filename,',');
    for contador=1:length(cell.semana)
        vector(tam_elemento_1) = cell.numero_totales_tweets(contador);
        tam_elemento_1 = tam_elemento_1 + 1;
    end;
end;

x = 1:14;
y = vector;
plot(x,y,'g');
vector;
