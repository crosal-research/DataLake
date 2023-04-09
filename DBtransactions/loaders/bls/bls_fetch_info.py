# import from system
from typing import List

# import from packages
import pandas as pd

path_to_file = "DBtransactions/loaders/bls/datasource.xlsx"


def fetch_info(p:str) -> List[List[str]]:
    """
    Takes a string - path for the file - and returns
    a list of list, where the inner list is three dimnension
    with information about series
    """
    ds = pd.read_excel(p, usecols=[0, 1], skiprows=[0], skipfooter=3)
    return  [[i[0], 
              f"{i[1]}, U.S.A. Consumer Price Index (CPI)", 
              "BLS_CPI"] for i in ds.values]
