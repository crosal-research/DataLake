###################################
# Estudar API do IPEA
# http://www.ipeadata.gov.br/api/
###################################

# import from system
from concurrent.futures import ThreadPoolExecutor as executor
from datetime import datetime as dt
import time
from typing import Optional, List

#import from packages
import requests
import pandas as pd


#app imports
# from DB.transactions import add_obs

URL = "http://www.ipeadata.gov.br/api/odata4/"



def build_url(tck:str) -> str:  # adicionar a possibilidade de usar limit
    """
    builds the url to fetch the data at ipeadatas webpage. 
    """
    return  URL + f"Metadados('{tck}')/Valores"

def process(resp:str, limit:Optional[int]=None) -> pd.DataFrame:
    """
    fetch the data returning a dataframe
    """
    dd = resp.json()['value'][limit:] if limit is not None else resp.json()['value']
    if resp.ok:
        return [(dt.fromisoformat(d['VALDATA'].split("T")[0]), float(d["VALVALOR"])) for d in dd
                if d["VALVALOR"] is not None]
    else:
        print(f"Could not reach {resp.url}")

def fetch(tickers:List[str], limit:Optional[int]=None):
    """
    list of the tickers of ipea's series for which observations
    are update/fetched. If limit is None, fetch all observations,
    else fetches only the last limit observations
    """
    t0 = time.time()
    urls =[build_url(tck.split(".")[1]) for tck in tickers]
    with requests.session() as session:
        with executor() as e:
            ds = list(e.map(lambda u: process(session.get(u), limit), urls))
    for dd, tck in zip(ds, tickers):
        for d in dd:
            print(d)
            add_obs(tck, *d)
    print(f"series from IPEA added to the database: {time.time() -t0}")    

