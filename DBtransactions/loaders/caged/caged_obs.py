############################################################
# see: http://pdet.mte.gov.br/novo-caged 
# Fetches the observations for Caged
# last change:
############################################################
# import from app
from typing import List, Dict
from functools import reduce

# imports from packages
import requests, pendulum
import pandas as pd
from bs4 import BeautifulSoup as bs

# import from app
from DBtransactions.DBtypes import Observation



URL = "http://pdet.mte.gov.br/novo-caged"

SHEETS_NAMES = ["Tabela 5", # admissoes, cols
                "Tabela 5.1"] # admissoes com ajuste, cols


month_conversion = {'Janeiro': '01', 
                    'Fevereiro':'02',
                    'Março':'03',
                    'Abril':'04',
                    'Maio':'05',
                    'Junho':'06',
                    'Julho':'07',
                    'Agosto':'08',
                    'Setembro':'09',
                    'Outubro':'10',
                    'Novembro':'11',
                    'Dezembro':'12'}

def _fetch_link() -> str:
    """
    return the url to fetch the excel spreasheet
    with caged's data
    """
    resp = requests.get(URL)
    soup = bs(resp.text, "html.parser")
    return "http://pdet.mte.gov.br" + [l for l in 
                                       soup.find_all('a') if ("Tabelas" in l.text) ][0].attrs['href']


def fetch(tickers: List[str], limit=None) -> List[List[Dict]]:
    """
    Takes tickers and return list of lists of observations
    """
    global d
    url = _fetch_link()
    excel = pd.ExcelFile(url)

    def _re_index(df: pd.DataFrame) -> pd.DataFrame:
        """
        return teh same dataframe, but where indexes with dates defined as in caged
        to the format 'dd-mm-yyyy'
        """
        df.index =  [f"{d.split('/')[1]}-{month_conversion[d.split('/')[0]]}-01" 
                    for d in df.index]
        return df

    dfs = [excel.parse(sheet_name=sheet,
                        skiprows=list(range(0, 4)), 
                        header=0,
                        usecols= [2] + list(range(1, 6)), 
                        index_col=[0]).dropna(axis=0) 
           for sheet in SHEETS_NAMES]

    df = reduce(lambda dx, dy: dx.merge(dy, how='inner', left_index=True, right_index=True),
                dfs)
    df.columns = [f"CAGED.{t}".upper() for t in ('est', 'adm', 'deslig', 'saldo', 'est_adjs' , 'adm_adjs', 'deslig_adjs', 'saldo_adjs')]
    df = _re_index(df.copy())
    df = df.head(limit)
    d = {}
    for c in tickers:
        for i in df.index:
            if not c in d:
                d[c] = []
            d[c].append(Observation(**{'series_id': c, 'dat': i, 'valor': df.loc[i, c]}))
    return list(d.values())
