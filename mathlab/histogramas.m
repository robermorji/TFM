close all;
name = '/home/roberto/Escritorio/Proyectos/Elecciones_USA/Save_Bag_of_Word/';
list = dir(name);

for c=3:length(list)
    filename=sprintf('/home/roberto/Escritorio/Proyectos/Elecciones_USA/Save_Bag_of_Word/%s',list(c).name);
    title_map = strsplit(filename,'.');
    title_map = strsplit(title_map{1},'/');
    h = figure('Name',title_map{8},'NumberTitle','off', 'Position', [0, 0, 720, 460]);
    cell = tdfread(filename,',');
    frecuencia = cell.count;
    perc = frecuencia / sum(frecuencia) * 100;
    labels = cell.word;
    lowFrecuency = frecuencia(perc < 1.0);
    hightFrecuency = frecuencia(perc > 1.0);
    
    x = perc(perc > 1.0);
    str = cell.word(perc>1.0,:);
    bar(x(1:length(x)))
   
    for i=1:length(x)
        a = regexp(str(i,:),' ', 'split');
        cadena = sprintf('%s\n%s',cell2mat(a(:,1)),cell2mat(a(:,2)));
        h = text(i,x(i)+0.10,cadena);
        set(h,'rotation',90);
        
    end
    name_map_file_jpg = strcat(title_map{8},'.png');
    name_map_file_jpg = strcat('/home/roberto/Escritorio/Proyectos/Elecciones_USA/Graficas/words/',name_map_file_jpg);
    saveas(h,name_map_file_jpg);
    close all;
end
