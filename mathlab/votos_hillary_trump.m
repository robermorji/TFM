close all;
name = '/home/roberto/Escritorio/Proyectos/Elecciones_USA/Votos/';
list = dir(name);
array_hillary = zeros(1,15);
array_trump = zeros(1,15);
array_semanas = zeros(1,15);
contador = 1;
for c=3:length(list)
    filename=sprintf('/home/roberto/Escritorio/Proyectos/Elecciones_USA/Votos/%s',list(c).name);
    num_col = strsplit(filename,'.');
    num_col = strsplit(num_col{1},'/');
    num_col = strsplit(num_col{8},'_');
    num_col = str2double(num_col{3});
    cell = tdfread(filename,',');
    array_hillary(num_col) = cell.count(1);
    array_trump(num_col) = cell.count(2);
    array_semanas(contador) = contador;
    contador = contador + 1;
end

[AX,H1,H2] = plotyy(array_semanas,array_hillary,array_semanas,array_trump,'plot');
title('Positivos para Trump y Positivos para Hillary')
xlabel('Semanas')
ylabel('Prediccion de votos');
legend('Hillary','Trump');
set(H1,'color','b') 
set(H2,'color','g')