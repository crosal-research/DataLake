##################################################
# Inserts information from nasdaq's data into 
# the DB
##################################################

# imports from System
import json
from typing import List, Optional, Dict
from concurrent.futures import ThreadPoolExecutor as executor

# import from packages
import requests
from dotenv import dotenv_values

# import from app
from DBtransactions.DBtypes import Series

config = dotenv_values("./.env")
_key = config["NASDAQ_KEY"]

TICKERS_ML = ["NASDAQ.ML/EMHYY", 
              "NASDAQ.ML/AAAEY",
              "NASDAQ.ML/AEY",
              "NASDAQ.ML/BEY",
              "NASDAQ.ML/BBBEY"]


TICKERS_MULTPL = ["NASDAQ.MULTPL/SHILLER_PE_RATIO_MONTH"]

TICKERS = TICKERS_ML + TICKERS_MULTPL


def _process(resp: requests.Response) -> str:
    if resp.ok:
        dataset = resp.json()['dataset']
        series_id = f"NASDAQ.{dataset['database_code']}/{dataset['dataset_code']}"
        description = f"{dataset['name']}, {dataset['description']}"
        survey_id = f"NASDAQ_{dataset['database_code']}"
        return Series(**{'series_id': series_id, 
                         'description': description, 
                         'survey_id': survey_id, 
                         'frequency': 'DIARIA' if dataset['frequency'] == 'daily' else "MENSAL", 
                         'last_update': None})
    return None
    

def fetch_info(tickers: List[str]) -> List[Dict[str, str]]:
    """
    fetches a list of series from their tickers
    """
    def _url(tck:str) -> str:
        """
        build the relevant url for a particular ticker
        """
        return f"https://data.nasdaq.com/api/v3/datasets/{tck.split('NASDAQ.')[1]}.json"
    
    adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
    with requests.Session() as session:
        session.mount("http://https://data.nasdaq.com/api/v3", adapter)
        with executor() as e:
            resps = e.map(lambda tck: session.get(_url(tck), params={'api_key': _key}), tickers)
                          
    return [_process(r) for r in resps]
