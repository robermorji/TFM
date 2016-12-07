figure; ax = usamap('all');
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
for i=1:indexConus
   stateColor = arrayStateColor(1,:);
   geoshow(ax(1), states(i),  'FaceColor', stateColor)
end
%geoshow(ax(1), states(indexConus),  'FaceColor', stateColor)
geoshow(ax(2), states(indexAlaska), 'FaceColor', stateColor)
geoshow(ax(3), states(indexHawaii), 'FaceColor', stateColor)

for k = 1:3
    setm(ax(k), 'Frame', 'off', 'Grid', 'off',...
      'ParallelLabel', 'off', 'MeridianLabel', 'off')
end