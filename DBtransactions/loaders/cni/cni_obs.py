# import from system
from io import BytesIO
import os, json
from typing import List
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

headers = {'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

url_ind = 'https://www.portaldaindustria.com.br/estatisticas/indicadores-industriais/'
url_ici = 'https://www.portaldaindustria.com.br/estatisticas/icei-indice-de-confianca-do-empresario-industrial/'


with open(os.getcwd() + "/DBtransactions/loaders/cni/data.json", 'r') as f:
    dat = json.loads(f.read())
    DATA = []
    for d in dat:
        DATA.append(dict((k, (lambda i: None if (i=="") else i)(d[k])) for k in d))



def _process(resp:requests.Response):
    """
    Prosses response
    """
    f = BytesIO()
    f.write(resp.content)
    excel = pd.ExcelFile(f)
    if "indicadoresindustriais" in resp.url:
        df = excel.parse(sheet_name="Indicadores", skiprows=list(range(0,15))).dropna(axis=1, how='all')
        dg = df.applymap(lambda x: np.NaN if x == 0  else x).dropna(axis=1, how='all').dropna(axis=0)
        dh = dg.applymap(lambda x: np.NaN if (isinstance(x, float) and abs(x) < 10) else x).dropna(axis=1, how='all').dropna(axis=1)
        dh.columns = ['data']  + [d['series_id'] for d in DATA if d['survey_id'] == 'CNI_ATIV']
        dh = dh.set_index('data')
        dh.index = [pendulum.instance(pendulum.from_format(i, "MM/YYYY")) for i in dh.index]

    elif "indicedeconfiancadoempresarioindustrial" in resp.url:
        df = excel.parse(sheet_name="Geral", skiprows=list(range(0,7))).dropna(axis=0, how='all').dropna(axis=1).head().T
        dh = df.iloc[:,[0, 1, 4]]
        dh.columns = [d['series_id'] for d in DATA if d['survey_id'] == 'CNI_ICEI']
        dh.index = [pendulum.instance(i) for i in dh.index]
        
    else:
        pass
    return dh


def _fetch(survey: str) -> pd.DataFrame:
    """
    Fetches
    """
    if survey == "CNI_ATIV":
        resp = requests.get(url_ind, headers=headers)
    else:
        resp = requests.get(url_ici, headers=headers)
    soup = bs(resp.text, "html.parser")
    url = [a for a in soup.find_all('a') if 'xlsx' in a.attrs['href']][0].attrs['href']
    return _process(requests.get(url))


def fetch(tickers: List[str], limit=None) -> List[List[Observation]]:
    """
    Takes a list of tickes fetches the observations for those
    serie, limited by the limit variable.
    Still needs to implement the limit in the final output
    """
    surveys = list(set([d['survey_id'] for tck in tickers for d in DATA if d['series_id'] == tck]))

    with executor() as e:
        dfs = list(e.map(_fetch, surveys))

    df = reduce(lambda dfx, dfy: dfx.merge(dfy, left_index=True, right_index=True, how="outer"), 
                dfs, pd.DataFrame(data=[]))
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

