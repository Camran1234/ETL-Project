import numpy as np
from utils import data_loader
from dotenv import load_dotenv
import pandas as pd

import os

load_dotenv('../config/.env')

GLOBAL_CSV_PATH = os.getenv('GLOBAL_CSV_PATH', 'NULL')
TOWN_CSV_PATH = os.getenv('TOWN_CSV_PATH', 'NULL')

#np_data, headers, finished = data_loader.local_csv(TOWN_CSV_PATH, 0, 20)
np_data, headers, finished = data_loader.download_csv(GLOBAL_CSV_PATH, 0, 30, False)
df = pd.DataFrame(np_data)
print(df)
data_loader.file_process(df, '../data/output/output.txt')