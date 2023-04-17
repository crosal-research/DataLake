# import from system
from typing import List
from concurrent.futures import ThreadPoolExecutor as executor
import re
import json, time

# import from packges
import requests
import pandas as pd
import numpy as np
import pendulum

#import from app
from DBtransactions.DBtypes import Observation

def _build_url(tck:str, limit=None) -> str:
    """
    builids the write url string to fetch observations, according to
    ibge's ipea. 
    """
    new_tck = tck.split(".")[1]
    if not limit:
        return f"http://api.sidra.ibge.gov.br/values/t/{new_tck}/p/all/d/2/n1/1"
    return f"http://api.sidra.ibge.gov.br/values/t/{new_tck}/p/last {limit}/d2/n1/1"


def _process(resp: requests.models.Response)-> List[Observation]:
    """
    Handles the sucessful response to a request to the ibge api.
    Return a Dataframe per respoonse
    """
    tbl = (re.compile("\d+")).findall(resp.url)[0]
    ticker = "IBGE." + ((resp.url).split("t/")[1]).split("/p")[0]
    ls = resp.json()
    c = [k for k in ls[0] if (("Mês" in ls[0][k]) or ("Trimestre" in ls[0][k]))][0]
    dt = "m" if "Mês" in ls[0][c] else "T"
    if dt == 'm':
        return [Observation(**{'dat': pendulum.from_format(l[c], "YYYYMM").to_date_string(), 
                               'valor': l["V"], 
                               'series_id': ticker}) for l in ls[1:] if l["V"] != '-']

    return [(Observation(**{'dat': pendulum.from_format(l[c][:4] + str(l[c][4:6][1]), "YYYYQ").to_date_string(), 
                           'valor': l["V"], 
                            'series_id': ticker}), print(l[c])) for l in ls[1:] if l["V"] != '-']


def fetch(tickers:List[str], limit=None) -> List[List[Observation]]:
    """
    Fetch the observations for tickers list of ibge's series.
    Limit defines the last n-limit observations to be fetched, where 
    Return a list of list of Observations, each of one of them representing
    the observations pertaining to a series
    """
    urls = [_build_url(tck, limit=limit) for tck in tickers]
    with requests.session() as session:
        with executor() as e:
            ls = list(e.map(lambda url: _process(session.get(url)), urls))
    return ls

