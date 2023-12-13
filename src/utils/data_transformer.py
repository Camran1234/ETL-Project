import pandas as pd
import numpy as np
from dateutil import parser
from dotenv import load_dotenv
import os
load_dotenv('../../config/.env')

DATE_FILTER = os.getenv('DATE_FILTER', 2020)
DATE_FORMAT = os.getenv('DATE_FORMAT', '%m/%d/%Y')

#Limpieza Country
COUNTRY_FILTER = os.getenv('COUNTRY_FILTER', 'NULL')
COUNTRY_COLUMN_NAME = os.getenv('COUNTRY_COLUMN_NAME', 'NULL')

#Limpieza headers TOWN
NUMERIC_HEADERS_TOWN = os.getenv('NUMERIC_HEADERS_TOWN', 'NULL')
TEXT_HEADERS_TOWN = os.getenv('TEXT_HEADERS_TOWN', 'NULL')

#Limpieza headers GLOBAL
NUMERIC_HEADERS_GLOBAL = os.getenv('NUMERIC_HEADERS_GLOBAL', 'NULL')
TEXT_HEADERS_GLOBAL = os.getenv('TEXT_HEADERS_GLOBAL', 'NULL')
def process_townChunk(np_data, headers):
    print("process_townChunk")
    df = pd.DataFrame(np_data)
    df = to_lowerCammelCase(df)
    df = clean_duplicates(df)
    df = cleanEmptyCols(df)
    df = clean_invalidDate(df)
    df = clean_negatives(df)
    df = clean_country(df, COUNTRY_COLUMN_NAME.lower(), COUNTRY_FILTER)
    df = clean_numeric_columns_null(df)
    date_headers = get_headers_date(df)
    numeric_headers = list(sum(zip(date_headers, NUMERIC_HEADERS_TOWN), ()))
    df = clean_numeric_columns_format(df, numeric_headers)
    df = clean_text_columns_format(df, TEXT_HEADERS_TOWN)
     


def process_globalChunk(np_data, headers):
    print("process_globalChunk")
    df = pd.DataFrame(np_data)
    df = to_lowerCammelCase(df)
    df = clean_duplicates(df)
    df = cleanEmptyCols(df)
    df = clean_negatives(df)
    df = clean_country(df, COUNTRY_COLUMN_NAME.lower(), COUNTRY_FILTER)
    df = clean_numeric_columns_null(df)
    df = clean_numeric_columns_format(df, NUMERIC_HEADERS_GLOBAL)
    df = clean_text_columns_format(df, TEXT_HEADERS_GLOBAL)
    

def cleanEmptyRows(df):
    df.replace("", np.nan, inplace=True)
    df.dropna(how='all', axis=0, inplace=True)
    return df

def cleanEmptyCols(df):
    df.replace("", np.nan, inplace=True)
    df.dropna(how='all', axis=1, inplace=True)
    return df

def clean_duplicates(df):
    print("clean_duplicates")
    df_clean = df.drop_duplicates()
    return df_clean

# Función para convertir a snake_case
def to_lowerCammelCase(df):
    df.columns = df.columns.str.lower()
    return df

# Función para verificar si un valor es una fecha válida
def valid_date(valor):    
    try:
        parser.parse(valor)
        return True
    except (ValueError, OverflowError):
        return False

def not_valid_date(valor):
    try:
        parser.parse(valor)
        return False
    except (ValueError, OverflowError):
        return True


def get_headers_date(df):
    headers = list(filter(valid_date, df.columns))
    return headers    

def get_headers_not_date(df):
    headers = list(filter(not_valid_date, df.columns))
    return headers    

def clean_invalidDate(df):
    # Identificar las columnas que son fechas y no son del año 2020    
    rows_to_delete = [col for col in df.columns if (
        pd.to_datetime(col, errors='coerce', format=DATE_FORMAT).year != int(DATE_FILTER)
    )]
    #print(rows_to_delete)
    rows_to_delete = list(filter(valid_date, rows_to_delete))
    #print(rows_to_delete)
    # Eliminar las columnas identificadas
    df = df.drop(columns=rows_to_delete)
    return df

def clean_country(df, columnName, country):
     # Asegurarse de que la columna exista en el DataFrame
    if columnName not in df.columns:
        raise ValueError(f"La columna '{columnName}' no existe en el DataFrame.")
    # Filtrar solo las filas donde el valor en la columna es 'Guatemala'
    df_filtrado = df[df[columnName] == country]
    return df_filtrado

def clean_negatives(df):
    # Seleccionar solo las columnas numéricas
    df_numeric = df.select_dtypes(include='number')
    # Eliminar registros que contienen al menos un número negativo
    df_sin_negativos = df[~(df_numeric < 0).any(axis=1)]
    return df_sin_negativos

def clean_numeric_columns_null(df):
    # Seleccionar solo las columnas numéricas
    df_numeric = df.select_dtypes(include='number')
    # Reemplazar NaN con 0 en las columnas numéricas
    df[df_numeric.columns] = df_numeric.fillna(0).astype(int)
    return df

def clean_text_columns_format(df, column_names):
    """
    Elimina los registros que contienen números y no texto en las columnas especificadas.

    Parameters:
        df (pd.DataFrame): El DataFrame de pandas.
        column_names (list): Lista de nombres de columnas a ser verificadas y limpiadas.

    Returns:
        pd.DataFrame: El DataFrame resultante después de la limpieza.
    """
    # Copiar el DataFrame original para evitar modificaciones inesperadas
    result_df = df.copy()

    # Iterar sobre las columnas especificadas
    for column_name in column_names:
        # Verificar si la columna existe en el DataFrame
        if column_name in result_df.columns:
            # Filtrar los registros que contienen números y no texto en la columna especificada
            result_df = result_df[pd.to_numeric(result_df[column_name], errors='coerce').isnull()]

    return result_df

def clean_numeric_columns_format(df, column_names):
    """
    Elimina los registros que no son numéricos en las columnas especificadas.

    Parameters:
        df (pd.DataFrame): El DataFrame de pandas.
        column_names (list): Lista de nombres de columnas a ser verificadas y limpiadas.

    Returns:
        pd.DataFrame: El DataFrame resultante después de la limpieza.
    """
    # Copiar el DataFrame original para evitar modificaciones inesperadas
    result_df = df.copy()

    # Iterar sobre las columnas especificadas
    for column_name in column_names:
        # Verificar si la columna existe en el DataFrame
        if column_name in result_df.columns:
            # Convertir la columna a numérico y eliminar los registros no numéricos
            result_df = result_df[pd.to_numeric(result_df[column_name], errors='coerce').notnull()]

    return result_df
