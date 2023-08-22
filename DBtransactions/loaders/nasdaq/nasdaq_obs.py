# import from system
from typing import List, Optional, Dict
from concurrent.futures import ThreadPoolExecutor as executor
import json

# import from packages
import requests
from dotenv import dotenv_values
import pendulum 

# import from App
from DBtransactions.DBtypes import Observation


config = dotenv_values("./.env")
_key = config["NASDAQ_KEY"]


def _process(resp: requests.Response, limit):
    if resp.ok:
        dataset = resp.json()['dataset']
        ticker = f"NASDAQ.{dataset['database_code']}/{dataset['dataset_code']}"
        if limit:
            return [Observation(**{'series_id': ticker, 'dat': d[0], 'valor': d[1]}) for d in dataset['data'] 
                    if pendulum.parse(d[0]) >= pendulum.parse(limit)]
        return [Observation(**{'series_id': ticker, 'dat': d[0], 'valor': d[1]}) for d in dataset['data']] 
    else:
        {'status': 'fail', 
         'series': ""}
        return None
    

def fetch(tickers: List[str], limit:Optional[str]=None) -> List[List[Dict[str, str]]]:
    """
    fetches a list of series from their tickers. limit is currenlty in the form of
    yyyy-mm-dd
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
    return [_process(r, limit) for r in resps]
