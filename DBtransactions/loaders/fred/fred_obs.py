# imports from system
from concurrent.futures import ThreadPoolExecutor as executor
from typing import Optional, List
from datetime import datetime as dt
import json, os

# import from backages
import requests
import pandas as pd
from dotenv import dotenv_values

# import from app
from DBtransactions.DBtypes import Observation

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


def process(resp: requests.models.Response) -> List[Observation]:
    """
    processes (handles) the response from the fred's api
    and returns dataframe with processed observations
    """
    dj = resp.json()["observations"]
    ticker = "FRED." + (resp.url).split("=")[1].split("&")[0]
    df = pd.DataFrame(dj).iloc[:, [2,3]].set_index(["date"])
    dfinal = (df.applymap(lambda v: float(v) if v != "." else None)).sort_index().dropna()
    return [Observation(**{'dat': i, 'valor': dfinal.loc[i].value, 'series_id': ticker}) 
            for i in dfinal.index]


def fetch(tickers: List[str], limit: Optional[int] = None) -> List[List[Observation]]:
    """
    fetches observations from fred's api for tickers. If limit is None, add
    all observations, or else the last n-limit observations. Returns a list
    of DataFrames, each one with a series linked to the tickers
    """
    key = config['FRED_KEY']
    urls =[build_fred(key, tck.split(".")[1], limit) for tck in tickers]
    with requests.session() as session:
        with executor() as e:
            obs = list(e.map(lambda url: process(session.get(url)), urls, timeout=20))
    return obs
