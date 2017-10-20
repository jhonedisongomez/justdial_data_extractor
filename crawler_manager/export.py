import csv, os
import pandas as pd
import re


output_file = "./output.csv"
if not os.path.exists(output_file):
    open(output_file, 'w').close() 



try:


    salidacsv = open('./output.csv', 'w')
    campos = ['Campo1', 'Campo2']
    salida = csv.DictWriter(salidacsv, fieldnames=campos)
    salida.writeheader()
    for indice in range(6):
        salida.writerow({ 'Campo1':indice+1,
                          'Campo2':chr(ord('a') + indice)})



 
    print('Se ha creado el archivo "output.csv"')

finally:
    salidacsv.close()