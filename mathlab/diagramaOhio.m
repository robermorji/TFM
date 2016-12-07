close all;
name = '/home/roberto/Escritorio/Proyectos/Elecciones_USA/Stastic/';
list = dir(name);

tam_elemento_1 = 1;
tam_elemento_2 = 1;
tam_elemento_3 = 1;
tam_elemento_4 = 1;
tam_elemento_5 = 1;
vector = zeros(5,length(list)-2);

for c=3:length(list)
    filename=sprintf('/home/roberto/Escritorio/Proyectos/Elecciones_USA/Stastic/%s',list(c).name);
    title_map = strsplit(filename,'.');
    title_map = strsplit(title_map{1},'/');
    %h = figure('Name',title_map{8},'NumberTitle','off');
    cell = tdfread(filename,',');
    pos = 1;
    for contador=1:length(cell.zone)
        a = regexp(cell.zone(contador,:),' ', 'split');
        state = sprintf('%s%s',cell2mat(a(:,1)),cell2mat(a(:,2)));
       
        if strcmp(state,'EasternTime')==1
            pos = contador;
            vector(1,tam_elemento_1) = cell.perc(pos);
            tam_elemento_1  = tam_elemento_1 + 1;
       
        elseif strcmp(state,'PacificTime')==1
            pos = contador;
            vector(2,tam_elemento_2) = cell.perc(pos);
            tam_elemento_2  = tam_elemento_2 + 1;
           
        elseif strcmp(state,'CentralTime')==1
            pos = contador;
            vector(3,tam_elemento_3) = cell.perc(pos);
            tam_elemento_3  = tam_elemento_3 + 1;
            
       elseif strcmp(state,'AtlanticTime')==1
            pos = contador;
            vector(4,tam_elemento_4) = cell.perc(pos);
            tam_elemento_4  = tam_elemento_4 + 1;
       
       
       elseif strcmp(state,'MountainTime')==1
            pos = contador;
            vector(5,tam_elemento_5) = cell.perc(pos);
            tam_elemento_5  = tam_elemento_5 + 1;
        end
        
    end;
end
x = 1:14;
y = vector;
plot(x,y);
vector;
