import numpy as np
from utils import data_loader, data_transformer
from dotenv import load_dotenv
import pandas as pd
from dateutil import parser

import os

load_dotenv('../config/.env')

GLOBAL_CSV_PATH = os.getenv('GLOBAL_CSV_PATH', 'NULL')
TOWN_CSV_PATH = os.getenv('TOWN_CSV_PATH', 'NULL')
COUNTRY_FILTER = os.getenv('COUNTRY_FILTER', 'NULL')
COUNTRY_COLUMN_NAME = os.getenv('COUNTRY_COLUMN_NAME', 'NULL')

"""np_data, headers, finished = data_loader.local_csv(TOWN_CSV_PATH, 0, 20)
np_data, headers, finished = data_loader.download_csv(GLOBAL_CSV_PATH, 0, 30, False)
df = pd.DataFrame(np_data)
print(df)
data_loader.file_process(df, '../data/output/output.txt')"""

df = pd.DataFrame({'FirstName': ['Vipul', 'Ashish', '3'], 
                            "Gender": ["", "Femenino", ""], 
                            "Age": [0, 0, 0],
                            "11/03/2020": [0, -1, None],
                            "12/03/2020": [0, 0, 0],
                            "14/03/2021": ['ASD', 0, -9],
                            "13-03-2020": [0, -4, 'AC'],
                            "Country":["España", "Estados Unidos", "Guatemala"],
                })
df.columns = df.columns.str.lower()
df['Department'] = np.nan
df.replace("", np.nan, inplace=True)
print(df)
df.dropna(how='all', axis=1, inplace=True)
#df = data_transformer.clean_invalidDate(df)
#df = data_transformer.clean_negatives(df)
#df = data_transformer.clean_country(df, COUNTRY_COLUMN_NAME.lower(), COUNTRY_FILTER)
#df = data_transformer.clean_numeric_columns_null(df)
#date_headers = data_transformer.get_headers_date(df)
date_headers = data_transformer.get_headers_not_date(df)
#df = data_transformer.clean_numeric_columns_format(df, date_headers)
df = data_transformer.clean_text_columns_format(df, date_headers)

# Imprimir el DataFrame resultante
print(df)