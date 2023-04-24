# import from system
from typing import List, Tuple
import os

# import from packages
import pandas as pd

# import from app
from DBtransactions.DBtypes import Series


path_to_file = os.path.dirname(os.path.abspath(__file__)) + "/datasource.xlsx"

def fetch_info(p:str) -> List[Series]: 
    """
    Takes a string - path for the file - and returns
    a list of list, where the inner list is three dimnension
    with information about series
    """
    ds = pd.read_excel(p, sheet_name="Pub level",
                       usecols=[0, 1], skiprows=[0], skipfooter=3)
    return  [Series(**{'series_id': "BLS.CUSR0000" + i[0], 
                       'description': f"{i[1]}, U.S.A. Consumer Price Index (CPI)", 
                       'survey_id': "BLS_CPI", 'frequency': "MENSAL"}) for i in ds.values]
