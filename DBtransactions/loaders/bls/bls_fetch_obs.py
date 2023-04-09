###########################################################
# Fetch data from Bls api
# 
# For CPI codes and example on how to build them, see: 
# https://www.bls.gov/cpi/additional-resources/index-publication-level.htm
# https://beta.bls.gov/dataQuery/find?fq=survey:[cu]&s=popularity:D
# https://www.bls.gov/help/hlpforma.htm#CU
###########################################################

import json, io
from functools import reduce
from typing import List, Optional

import requests
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor


config = dotenv_values(".env")
_key_bls=config["BLS_key"]

URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
INI = 2015
END = 2023


def _process(resp: requests.Response) -> pd.DataFrame:
    """
    Takes a request response, processes into a dataframe
    """
    dat = resp.json()["Results"]["series"]
    multi = []
    for ser in dat:
        ac = []
        s = ser["seriesID"]
        info = ser["data"]
        for d in info:
            ac.append([f"{d['year']}-{d['period'][1:]}-01", 
                       float(d['value'])])
        df = pd.DataFrame(data=ac, columns = ['date', s]).set_index(['date'])
        multi.append(df)
    dfinal = reduce(lambda x, y: x.merge(y, 
                                         right_index=True,
                                         left_index=True, 
                                         how="outer"), multi)
    dfinal.index = pd.to_datetime(dfinal.index)
    return dfinal.sort_index()


def _fetch_aux(tickers:List[str], ini:int=INI,
           end:int=END) -> Optional[pd.DataFrame]:
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


def fetch(tickers: Liast[str], ini: ini=INI, 
              end:int=END) -> pd.DataFrame:
    """
    List of tickers as input and return a consolidade 
    dataframe with all requests make in an async manner
    """
    with ThreadPoolExecutor(max_workers=None) as executor:
        dfs = list(executor.map(lambda x: _fetch_aux(list(x)), 
                                np.array_split(tickers, 9)))

    # process and ship data    
    dfinal = reduce(lambda x, y: x.merge(y,
                                         right_index=True,
                                         left_index=True, 
                                         how="inner"), list(dfs))
    dfinal.columns = list(ds['Item title'].values)[2:]
    return  dfinal.dropna(axis=1, how="all")
