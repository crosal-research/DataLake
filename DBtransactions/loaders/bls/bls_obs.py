###########################################################
# Fetch data from Bls api
# 
# For CPI codes and example on how to build them, see: 
# https://www.bls.gov/cpi/additional-resources/index-publication-level.htm
# https://beta.bls.gov/dataQuery/find?fq=survey:[cu]&s=popularity:D
# https://www.bls.gov/help/hlpforma.htm#CU

# Makes sure the fetch function return List[Observation]
# date: 11/04/2023
###########################################################

# import from the system
import json, io
from functools import reduce
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor

# import from packages
import requests
import pandas as pd
import numpy as np
from dotenv import dotenv_values

# import from app
from DBtransactions.DBtypes import Observation


config = dotenv_values("./.env")
_key_bls=config["BLS_KEY"]

URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
INI = 2010
END = 2025


def _process(resp: requests.Response)-> List[List[Observation]]:
    """
    Takes a request response, processes into a dataframe
    """
    srs = resp.json()["Results"]["series"]
    multi = []
    for s in srs:
        tck = s["seriesID"]
        info = s["data"]
        ser = [Observation(**{'dat':f"{i['year']}-{i['period'][1:]}-01", 
                              'valor': float(i['value']), 
                              'series_id':f"BLS.{tck}"})
               for i in info]       # List[Observation]
        multi.append(ser)   # List[List[Observation]]
    return multi


def _fetch_aux(tickers:List[str], ini:int=INI,
           end:int=END) -> Optional[List[List[Observation]]]:
    """
    Takes list of tickers as input and makes a single request
    from source api. Returns a DataFrame with a processed 
    request response
    """
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": tickers,
                       "startyear": str(ini),
                       "endyear": str(end),
                       "registrationkey": _key_bls})
    resp = requests.post(URL, 
                         data=data, 
                         headers=headers)
    
    if resp.ok:
        return _process(resp)
    else:
        None


def fetch(tickers: List[str], ini: int=INI, 
              end:int=END, limit:Optional[str]=None) -> List[List[Observation]]:
    """
    List of tickers as input and return a consolidade 
    dataframe with all requests make in an async manner
    """
    tickers = [tck.split(".")[1] for tck in tickers]
    with ThreadPoolExecutor(max_workers=None) as executor:
        dfs = list(executor.map(lambda x: _fetch_aux(list(x)),
                                np.array_split(tickers, 9)))
    if len(dfs) <= 1:
        return dfs
    obs_all = reduce(lambda x, y: x + y, dfs)
    return obs_all

