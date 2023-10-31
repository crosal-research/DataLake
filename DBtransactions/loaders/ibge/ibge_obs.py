# import from system
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor as executor
import re
import json, time

# import from packges
import requests
import pandas as pd
import numpy as np
import pendulum
import urllib3
from urllib3.util.ssl_ import create_urllib3_context

#import from app
from DBtransactions.DBtypes import Observation

def _build_url(tck:str, limit:Optional[str]=None) -> str:
    """
    builids the write url string to fetch observations, according to
    ibge's ipea. 
    """
    new_tck = tck.split(".")[1]
    if not limit:
        return f"https://apisidra.ibge.gov.br/values/t/{new_tck}/p/all/d/2/n1/1"
    return f"https://apisidra.ibge.gov.br/values/t/{new_tck}/p/last {limit}/d/2/n1/1"


def _process(resp: requests.models.Response)-> List[Observation]:
    """
    Handles the sucessful response to a request to the ibge api.
    Return a Dataframe per response
    """
    tbl = (re.compile("\d+")).findall(resp.url)[0]
    ticker = "IBGE." + ((resp.url).split("t/")[1]).split("/p")[0]
    ls = resp.json()
    c = [k for k in ls[0] if (("Mês" in ls[0][k]) or ("Trimestre" in ls[0][k]))][0]
    dt = "T" if ls[0][c] == "Trimestre (Código)" else "M"
    if dt == 'M':
        return [Observation(**{'dat': pendulum.from_format(l[c], "YYYYMM").to_date_string(), 
                               'valor': l["V"], 
                               'series_id': ticker}) for l in ls[1:] if re.match("-?\d+", l["V"]) is not None ]

    return [Observation(**{'dat': pendulum.from_format(l[c][:4] + str(l[c][4:6][1]), "YYYYQ").to_date_string(), 
                           'valor': l["V"], 
                           'series_id': ticker}) for l in ls[1:] if re.match("-?\d+", l["V"]) is not None]


def fetch(tickers:List[str], limit:Optional[str]=None) -> List[List[Observation]]:
    """
    Fetch the observations for tickers list of ibge's series.
    Limit defines the last n-limit observations to be fetched, where 
    Return a list of list of Observations, each of one of them representing
    the observations pertaining to a series
    """
    # see: https://github.com/urllib3/urllib3/issues/2653
    ctx = create_urllib3_context()
    ctx.load_default_certs()
    ctx.options |= 0x4  # ssl.OP_LEGACY_SERVER_CONNECT
    urls = [_build_url(tck, limit=limit) for tck in tickers]
    with urllib3.PoolManager(ssl_context=ctx) as https: # used in order to circunvent ssl_legacy problem
    # with urllib3.HTTPSConnectionPool(host="apisidra.ibge.gov.br", maxsize=10, ssl_context=ctx) as https: # used in order to circunvent ssl_legacy problem        
        with executor() as e:
            ls = list(e.map(lambda url: _process(https.request("GET", url)), urls))
    return ls

