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

# with open(os.getcwd() + "/DBtransactions/loaders/stn/data.json", "r") as f:
#     DATA = json.loads(f.read())


def fetch(tickers:List[str], limit=None):
    headers = {'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    url = "https://www.tesourotransparente.gov.br/publicacoes/boletim-resultado-do-tesouro-nacional-rtn"
    dat = pendulum.today()
    i = 0
    while i < 10:
        dat_new = dat.subtract(months=i)
        new_url = url + f'/{dat_new.year}/{dat_new.month - i}'
        resp = requests.get(new_url, headers=headers)
        if resp.ok:
            soup = bs(resp.text, "html.parser")
            url_final = [a for a in soup.find_all('a') if ('title' in a.attrs) and ('serie_historica' in a.attrs['title'])][0].attrs['href']
            break
        else:
            i = i + 1


    new_resp = requests.get(url_final, headers=headers)
    content = bs(new_resp.text, "html.parser")
    new_url = content.find_all("frame")[0].attrs["src"]
    
    result = requests.get(new_url, headers=headers)
    with BytesIO() as f:
        f.write(result.content)
        excel = pd.ExcelFile(f, engine="openpyxl")
        df = pd.read_excel(excel, sheet_name="1.2", 
                           index_col=[0], 
                           header=[0], 
                           skiprows=[0, 1, 2, 3] + list(range(164, 200))).T
    df.columns = ["STN." + c.split(" ")[0].replace(".", "") for c in df.columns]
    dfinal = df if not limit else df.tail(limit)
    d = {}
    for c in tickers:
        for i in dfinal.index:
            if c not in d:
                d[c] = []
            v = dfinal.loc[i,c]    
            if not np.isnan(v):
                d[c].append(Observation(**{'series_id': c, 'dat': i.strftime("%Y-%m-%d"), 'valor': dfinal.loc[i, c]}))
    return list(d.values())
