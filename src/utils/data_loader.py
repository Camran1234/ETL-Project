# Tareas:
# 1. Terminar la carga de archivos
# 2. Crear un arreglo NumPy con los datos del archivo de municipios
# 3. Crear un arreglo NumPy con los datos del archivo global
# 4. Limpiar las tuplas de los arreglos
# 5. Reimprimir los arreglos
# 6. Realizar la operación vectorizada
# 7. Imprimir el resultado
# 8. Guardar el resultado en el dataset de salida

import csv
import requests
from io import StringIO
#Archivos csv
deceased_per_town_csv = '../../data/processed/municipio.csv'
deceased_per_global_csv = 'https://seminario2.blob.core.windows.net/fase1/global.csv?sp=r&st=2023-12-06T03:45:26Z&se=2024-01-04T11:45:26Z&sv=2022-11-02&sr=b&sig=xdx7LdUOekGyBvGL%2FNE55ZZj9SBvCC%2FWegxtpSsKjJg%3D'
route_file = '../../data/output/output.txt'

def row_process(row):
    print(row)


def file_process(array, file):
    with open(file, 'a') as output_file:
        print(array, file=output_file)

def download_csv(url):
    response = requests.get(url)
    if response.status_code == 200:
        return StringIO(response.text)
        for line in response.iter_lines(decode_unicode=True):
            row_process(line)
    else:
        print('Could not read file in url', url)
        return None    

# Dynamic charge of the csv file
with open(deceased_per_town_csv, 'r') as deceased_per_town_file:
    csv_reader = csv.reader(deceased_per_town_file)
    encabezado = next(csv_reader)  # Header, it omits if exists
    #file_process(encabezado, route_file)
    for row in csv_reader:
        #row_process(fila)
        file_process(row, route_file)

'''with open(deceased_per_town_csv, 'r') as deceased_per_global_file:
    csv_reader = csv.reader(deceased_per_global_file)
    header = next(csv_reader)
    limitLine = 5  
    print(header)
    counter = 0
    for row in csv_reader:
        counter+=1
        if counter == limitLine:
            break
        row_process(row)'''
