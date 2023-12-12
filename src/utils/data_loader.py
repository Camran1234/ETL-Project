# Tareas:
# 1. Terminar la carga de archivos COMPLETO
# 2. Crear un arreglo NumPy con los datos del archivo de municipios
# 3. Crear un arreglo NumPy con los datos del archivo global
# 4. Limpiar las tuplas de los arreglos
# 5. Reimprimir los arreglos
# 6. Realizar la operación vectorizada
# 7. Imprimir el resultado
# 8. Guardar el resultado en el dataset de salida

import csv
import requests
import numpy as np
from io import BytesIO, TextIOWrapper
from utils import data_transformer

def file_process(array, file):
    with open(file, 'a') as output_file:
        print(array, file=output_file)

def download_csv(url, initFlag, lastFlag, limited):
    response = requests.get(url)
    data = []
    headers = None
    end_of_file = False
    if response.status_code == 200:                
        csv_reader = csv.reader(TextIOWrapper(BytesIO(response.content), encoding='utf-8-sig'))
        if limited:            
            headers = next(csv_reader)
            if headers is not None:
                data.append(headers)

            for _ in range(initFlag):
                next(csv_reader, None)

            for _ in range(lastFlag):
                row = next(csv_reader, None)
                if row is not None:
                    data.append(row)
                else:
                    end_of_file = True
                    break
            np_data = np.array(data)
            return np_data, headers, end_of_file
        else:
            for row in csv_reader:
                data.append(row)
            np_data = np.array(data)
            return np_data, headers, True
        
#        for row in response.iter_lines(decode_unicode=True):
#            print(row)            
    else:
        print('Could not read file in url', url)
        return None 

def local_csv(fileRoute, initFlag, lastFlag):
    # Dynamic charge of the csv file
    data = [] 
    headers = None
    end_of_file = False
    # Open the file, its a pointer not a object with all the data in memoery
    with open(fileRoute, 'r') as deceased_per_town_file:
        csv_reader = csv.reader(deceased_per_town_file)
        headers = next(csv_reader)  # Header, it omits if exists
        if headers is not None:
            data.append(headers)

        # Read the file till initFlag
        for _ in range(initFlag):
            next(csv_reader, None)

        # Read the file till lastFlag
        for _ in range(lastFlag):
            row = next(csv_reader, None)
            if row is not None:
                data.append(row)
            else:
                end_of_file = True
                break
        np_data = np.array(data)
        return np_data, headers, end_of_file        


def process_csv(type, fileRoute, chunkSize):
    chunkFlag=0;
    while True:        
        baseIndex = chunkFlag*chunkSize
        pdArray = None
        if type == 'local':
            data,headers, finished = local_csv(fileRoute, baseIndex, baseIndex+chunkSize)
            pdArray = data_transformer.process_townChunk(data, headers)
        elif type == 'global':
            data,headers, finished = download_csv(fileRoute, baseIndex, baseIndex+chunkSize)
            pdArray = data_transformer.process_globalChunk(data, headers)
        else:
            print('Invalid type') 
            return None, None, None
        #Process data
        #I recommend call the file data_transformer.py        
        #EoF
        if finished:
            return data, headers, finished            
        else:
            print("Chunk ", chunkFlag, " processed")
        chunkFlag+=1        

