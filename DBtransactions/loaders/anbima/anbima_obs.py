# import from system
import io
from typing import List, Dict, Optional

# import from packages
import requests
import pandas as pd
import pendulum

# import from app
from DBtransactions.DBtypes import Observation


def _build_url(dat:str):
    return f"https://www.anbima.com.br/informacoes/merc-sec/arqs/ms{dat}.txt"


def _process(df: pd.DataFrame, tickers: List[str]) -> List[Dict[str, str]]:
    """
    Takes a dataframe with information on public bonds
    and returns list of List
    missing: falta separa os ativos em lista, cada uma relacionada a
    um ticker
    """
    lx = [{'series_id': f"ANBIMA.{'_'.join([str(df.loc[i,'Titulo']), str(df.loc[i, 'Data Vencimento'])])}" , 
             'dat': pendulum.parse(str(df.loc[i, 'Data Referencia'])).to_date_string(),
             'valor': df.loc[i, 'Tx. Indicativas']} for i in df.index ]
    dd = {}

    for l in lx:
        if l['series_id'] in tickers:
            if l['series_id'] not in dd:
                dd[l['series_id']] = [Observation(**l)]
            else:
                dd[l['series_id']] = append(Observation(**l))
    return list(dd.values())


def fetch(tickers: List[str], limit: Optional[int]=1):
    limit = int(limit)
    d = pendulum.now().subtract(days=limit)
    while True:
        if d.day_of_week not in [0, 6]:
            break
        d = d.subtract(days=limit)
    dd = (d.to_date_string()).replace("-", "")[2:]
    resp = requests.get(_build_url(dd))
    if resp.ok:
        df = pd.read_table(io.StringIO(resp.text), 
                           skiprows=[0],
                           sep="@", 
                           decimal=",", 
                           usecols=[0, 1, 4, 7])
        df.loc[:, 'Titulo'] = [t.replace("-", "") for t in df.loc[:, 'Titulo']]
        lx = _process(df, tickers)
        return lx
    else:
        print("Date not available")
    
