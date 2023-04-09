# imports from system
from concurrent.futures import ThreadPoolExecutor as executor
from typing import Optional, List
from datetime import datetime as dt
import time, json, os
from dotenv import dotenv_values

# import from backages
import requests
import pandas as pd


__all__ = ["fetch"]

config = dotenv_values(".env")


def build_fred(key, ticker, limit: Optional[int]=None):
    """
    builds url to fetch observations, depending on whether
    fetches all observations or only the n-limit last.
    """
    if not limit:
        return f"https://api.stlouisfed.org/fred/series/observations?" + \
            f"series_id={ticker}&api_key={key}&file_type=json"
    else:
        return f"https://api.stlouisfed.org/fred/series/observations?" + \
            f"series_id={ticker}&api_key={key}&file_type=json" + \
            "&limit=10&sort_order=desc"


def process(resp: requests.models.Response) -> List[pd.DataFrame]:
    """
    processes (handles) the response from the fred's api
    and returns dataframe with processed observations
    """
    dj = resp.json()["observations"]
    df = pd.DataFrame(dj).iloc[:, [2,3]].set_index(["date"])
    df.index = [dt.strptime(i, "%Y-%m-%d") for i in df.index]
    return (df.applymap(lambda v: float(v) if v != "." else None)).sort_index().dropna()


def fetch(tickers: List[str], limit: Optional[int] = None) -> List[pd.DataFrame]:
    """
    fetches observations from fred's api for tickers. If limit is None, add
    full observations, else the last n-limit observations.
    """
    key = config['FRED_KEY']
    global dfs
    urls =[build_fred(key, tck.split(".")[1], limit) for tck in tickers]
    with requests.session() as session:
        with executor() as e:
            dfs = list(e.map(lambda url: process(session.get(url)), urls))
    for i,df in enumerate(dfs):
        df.columns = [tickers[i].upper()]
    return dfs    
