# import from system
import io
from typing import List, Dict, Optional

# import from packages
import requests
import pandas as pd
import pendulum

# import from app
from DBtransactions.DBtypes import Series


def _build_url(dat:str):
    return f"https://www.anbima.com.br/informacoes/merc-sec/arqs/ms{dat}.txt"


def _process(df: pd.DataFrame) -> List[Dict[str, str]]:
    """
    Takes a dataframe with information on public bonds
    and returns list of List
    missing: falta separa os ativos em lista, cada uma relacionada a
    um ticker
    """
    lx = [{'series_id': f"ANBIMA.{'_'.join([str(df.loc[i,'Titulo']), str(df.loc[i, 'Data Vencimento'])])}" ,
           'frequency': "DIARIA",
           'description': f"Taxa indicativas da {df.loc[i, 'Titulo']} com vencimento em {df.loc[i, 'Data Vencimento']}", 
           'survey_id': "ANBIMA_TAXAS", 
           'last_update': None} 
            for i in df.index ]
    return [Series(**l) for l in lx]


def fetch_info(limit: Optional[int]=3):
    d = (pendulum.now()).subtract(days=limit)
    dd = (d.to_date_string()).replace("-", "")[2:]
    resp = requests.get(_build_url(dd))
    if resp.ok:
        df = pd.read_table(io.StringIO(resp.text), 
                           skiprows=[0],
                           sep="@", 
                           decimal=",", 
                           usecols=[0, 1, 4, 7])
        df.loc[:, 'Titulo'] = [t.replace("-", "") for t in df.loc[:, 'Titulo']]
        return  _process(df)
    else:
        print("Date not available")
    
