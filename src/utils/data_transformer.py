import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv('../../config/.env')
DATE_FILTER = os.getenv('DATE_FILTER', None)

def process_townChunk(np_data, headers):
    print("process_townChunk")
    df = pd.DataFrame(np_data)
    df = clean_duplicates(df)


def process_globalChunk(np_data, headers):
    print("process_globalChunk")
    df = pd.DataFrame(np_data)
    df = clean_duplicates(df)

def clean_dateColumns(df):
    print("clean_dateColumns")
    df = df[df['Date'] != DATE_FILTER]
    return df

def clean_duplicates(df):
    print("clean_duplicates")
    df_clean = df.drop_duplicates()
    return df_clean