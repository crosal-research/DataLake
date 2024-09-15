# import from system
from io import BytesIO
import os, json
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor as executor
from functools import reduce

# import from packages
import requests
import pandas as pd
import pendulum
import numpy as np

from bs4 import BeautifulSoup as bs


# import from App
from DBtransactions.DBtypes import Observation


def fetch(tickers:List[str], limit: Optional[int]=None)-> List[Observation]:
    """
    Takes a list of tickers (str) and return a List of Observation
    """
    headers = {'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    url = "https://melhoresrodovias.org.br/indice-abcr/"
    resp = requests.get(url, headers=headers)
    soup = bs(resp.text, "html.parser")
    las = [a for a in soup.find_all('a')]
    new_url = ''
    for a in las:
        try:
            if 'xlsx' in a.attrs['href']:
                new_url = a.attrs['href']
                break
        except KeyError as e:
            continue
    
    if new_url == '':
        print("File for ABCR survey is not available")
        return None

    result = requests.get(new_url, headers=headers)
    with BytesIO() as f:
        f.write(result.content)
        excel = pd.ExcelFile(f, engine="openpyxl")
        ds = pd.read_excel(excel, sheet_name= 2, 
                           index_col=[0], 
                           header=[0], 
                           skiprows=[0, 1], usecols=[0, 1, 2, 3, 5, 6, 7, 13, 14, 15])
        ds.columns = [f'ABCR.{c}'.upper() for c in ['bzleves', 'bzpesados', 'bztotal', 
                                                    'spleves', 'sppesados', 'sptotal', 
                                                    'rjleves', 'rjpesados', 'rjtotal']]

        da = pd.read_excel(excel, sheet_name= 3,
                           index_col=[0], 
                           header=[0], 
                           skiprows=[0, 1],
                           usecols=[0, 1, 2, 3, 8, 9, 10, 22, 23, 24])
        da.columns = [f'{c}_adjs'.upper() for c in ds.columns]
                                                   
    dg = ds.merge(da, how='outer', left_index=True, right_index=True)
    dfinal = dg if not limit else dg.tail(limit)
    d = {}
    for c in tickers:
        for i in dfinal.index:
            if c not in d:
                d[c] = []
            v = dfinal.loc[i,c]    
            if not np.isnan(v):
                d[c].append(Observation(**{'series_id': c, 'dat': i.strftime("%Y-%m-%d"), 'valor': dfinal.loc[i, c]}))
    return list(d.values())
