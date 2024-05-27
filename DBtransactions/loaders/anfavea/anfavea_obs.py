# import from system
from io import BytesIO
from typing import List, Optional
import json, os

# import from packages
import requests
import pandas as pd
import numpy as np
import openpyxl

# import from App
from DBtransactions.DBtypes import Observation


with open(os.getcwd() + "/DBtransactions/loaders/anfavea/data.json", 'r') as f:
    dat = json.loads(f.read())
    DATA = []
    for d in dat:
        DATA.append(dict((k, (lambda i: None if (i=="") else i)(d[k])) for k in d))


def fetch(tickers:List[str], limit=Optional[int]) -> List[List[Observation]]:
    headers = {'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    url = "https://anfavea.com.br/docs/SeriesTemporais_Autoveiculos.xlsm"

    resp = requests.get(url, headers=headers)
    with BytesIO() as f:
        f.write(resp.content)
        excel = pd.ExcelFile(f, engine="openpyxl")
        df = excel.parse(sheet_name=0).dropna()

    series_ids = [d['series_id'] for d in DATA]
    df.columns = ['data'] + series_ids
    df.set_index('data', inplace=True)
    df = df[df.apply(lambda x: x.sum() != 0, axis=1).values]
    if limit:
        df = df.tail(limit)

    d = {}
    for c in tickers:
        for i in df.index:
            if not c in d:
                d[c] = []
            if not np.isnan(df.loc[i,c]):
                d[c].append(Observation(**{'series_id': c, 
                                           'dat': i.date().strftime("%d-%m-%Y"), 
                                           'valor': df.loc[i, c]}))
    return list(d.values())
