# import from system
from typing import List, Optional, Dict
from concurrent.futures import ThreadPoolExecutor as executor
import json

# import from packages
import requests
from dotenv import dotenv_values

config = dotenv_values("./.env")
_key = config["NASDAQ_KEY"]


ticker = "NASDAQ.MULTPL/SHILLER_PE_RATIO_MONTH"

"https://data.nasdaq.com/api/v3/datasets/ML/EMHYY.json?api_key=YLLy-zR6Y3fdQPkUzeyE" # EM corporate bonds
"https://data.nasdaq.com/api/v3/datasets/ML/AAAEY.json?api_key=YLLy-zR6Y3fdQPkUzeyE" # US AAA
"https://data.nasdaq.com/api/v3/datasets/ML/AEY.json?api_key=YLLy-zR6Y3fdQPkUzeyE"   # US A
"https://data.nasdaq.com/api/v3/datasets/ML/BEY.json?api_key=YLLy-zR6Y3fdQPkUzeyE"   # US B
"https://data.nasdaq.com/api/v3/datasets/ML/BBBEY.json?api_key=YLLy-zR6Y3fdQPkUzeyE" # US BBB


def _process(resp: requests.Response):
    if resp.ok:
        dataset = resp.json()['dataset']
        ticker = f"NASDAQ.{dataset['database_code']}/{dataset['dataset_code']}"
        return [Observation(**{'series_id': ticker, 'dat': d[0], 'valor': d[1]}) for d in dataset['data']]
    else:
        {'status': 'fail', 
         'series': ""}
        return None
    

def fetch(tickers: List[str]) -> List[List[Dict[str, str]]]:
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
