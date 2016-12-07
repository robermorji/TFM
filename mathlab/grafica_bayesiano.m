close all;
name = '/home/roberto/Escritorio/Proyectos/Elecciones_USA/resultados_accuracy_bayesiano.csv';
cell = tdfread(name,',');
name_2 = '/home/roberto/Escritorio/Proyectos/Elecciones_USA/resultados_accuracy_SVM.csv';
cell2 = tdfread(name_2,',');
plotyy(cell.execute, cell.resultados_accuracy_bayesiano,cell2.execute, cell2.resultados_accuracy_SVM)

title('Comparacion Bayesiano y Suport Vector Machine')
xlabel('Iteraciones')
legend('Bayesiano','SVM');

