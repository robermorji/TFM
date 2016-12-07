close all
name = '/home/roberto/Escritorio/Proyectos/Elecciones_USA/Stastic/';
list = dir(name);
for c=3:length(list)
    filename=sprintf('/home/roberto/Escritorio/Proyectos/Elecciones_USA/Stastic/%s',list(c).name);
    title_map = strsplit(filename,'.');
    title_map = strsplit(title_map{1},'/');
    h = figure('Name',title_map{8},'NumberTitle','off');
    ax = usamap('all');
    set(ax, 'Visible', 'off')
    states = shaperead('usastatelo', 'UseGeoCoords', true);
    names = {states.Name};
    indexHawaii = strcmp('Hawaii',names);
    indexAlaska = strcmp('Alaska',names);
    indexConus = 1:numel(states);
    indexConus(indexHawaii|indexAlaska) = [];
    faceColors = makesymbolspec('Polygon',{'INDEX', [1 numel(states)],...
        'FaceColor',polcmap(numel(states))}); %NOTE - colors are random
    arrayStateColor = faceColors.FaceColor{3};
    geoshow(ax(1),states, 'DisplayType', 'polygon','SymbolSpec', faceColors)
    %geoshow(ax(2),states(indexAlaska), 'DisplayType', 'polygon','SymbolSpec', faceColors)
    %geoshow(ax(3),states(indexHawaii), 'DisplayType', 'polygon','SymbolSpec', faceColors)

    for k = 1:length(ax)
        setm(ax(k), 'Frame', 'off', 'Grid', 'off',...
          'ParallelLabel', 'off', 'MeridianLabel', 'off')
    end
       
    cell = tdfread(filename,',');
    for i=1:length(cell.lat)
        circlem(cell.lat(i),cell.lon(i),cell.perc(i)*10)
    end
    name_map_file_jpg = strcat(title_map{8},'.jpg');
    name_map_file_jpg = strcat('/home/roberto/Escritorio/Proyectos/Elecciones_USA/Graficas/maps/Ohio/',name_map_file_jpg);
    saveas(h,name_map_file_jpg);
    close all;
end