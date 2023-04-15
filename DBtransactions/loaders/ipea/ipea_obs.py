###################################
# Estudar API do IPEA
# http://www.ipeadata.gov.br/api/
###################################

# import from system
from concurrent.futures import ThreadPoolExecutor as executor
from datetime import datetime as dt
from typing import Optional, List

#import from packages
import requests
import pandas as pd

#import forom app
from DBtransactions.DBtypes import Observation

URL = "http://www.ipeadata.gov.br/api/odata4/"


def build_url(tck:str) -> str:  # adicionar a possibilidade de usar limit
    """
    builds the url to fetch the data at ipeadatas webpage. 
    """
    return  URL + f"Metadados('{tck}')/Valores"

def process(resp:str, limit:Optional[int]=None) -> Optional[List[Observation]]:
    """
    fetch the data returning a dataframe
    """
    url = resp.url
    ticker = "IPEA." + (resp.url).split("('")[1].split("')")[0]
    dd = resp.json()['value'][limit:] if limit is not None else resp.json()['value']
    if resp.ok:
        return [Observation(**{"dat": d['VALDATA'].split("T")[0], 
                               "valor": float(d["VALVALOR"]), 
                               "series_id": ticker}) for d in dd
                if d["VALVALOR"] is not None ]
    else:
        print(f"Could not reach {resp.url}")

def fetch(tickers:List[str], limit:Optional[int]=None) -> List[List[Observation]]:
    """
    Fetch list of the tickers of ipea's series for which observations
    are update/fetched. If limit is None, fetch all observations,
    else fetches only the last limit observations
    """
    urls =[build_url(tck.split(".")[1]) for tck in tickers]
    with requests.session() as session:
        with executor() as e:
            obs = list(e.map(lambda u: process(session.get(u), limit), urls))
    return obs

