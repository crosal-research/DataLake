# imports from system
from concurrent.futures import ThreadPoolExecutor as executor
import json, time
from typing import List, Optional
from datetime import datetime as dt

# import from packages
import requests
import pandas as pd
import pendulum

#import from app
from DBtransactions.DBtypes import Observation


__all__ = ["fetch"]


def build_url(fulltck: str, limit=None) -> str:
    """
    build the url of request to the BCB's api
    """""
    tck= fulltck.split(".")[1].upper()
    tck_new = tck if len(tck) > 2 else "0" + tck
    if not limit:
        return f"http://api.bcb.gov.br/dados/serie/bcdata.sgs.{tck_new}/dados?formato=json"
    return f"http://api.bcb.gov.br/dados/serie/bcdata.sgs.{tck_new}/dados/ultimos/{limit}?formato=json"


def _process(resp:requests.models.Response) -> Optional[dict]:
    """
    handles the successful response to a request the bcb api
    """
    if resp.ok:
        try:
            tck = str(int((resp.url).split("bcdata.sgs.")[1].split("/dados")[0]))
            obs = resp.json()
            return [Observation(**{'series_id': f"BCB.{tck}", 
                                   'dat': pendulum.from_format(o['data'], "DD/MM/YYYY").to_date_string(), 
                                   'valor': o['valor']}) for o in obs]
        except:
            print(f"Could not process {resp.url}")
    else:
        print("Failed request {resp.url}")
        return None
        

def fetch(tickers: List[str], limit: Optional[int]=None) -> List[Observation]:
    """
    Fetch the observations from the bcb's api. 
    """
    urls = (build_url(tck, limit=limit) for tck in tickers)
    with requests.session() as session:
        with executor() as e:
            js = list(e.map(lambda url:_process(session.get(url)), list(urls)))

    return js
