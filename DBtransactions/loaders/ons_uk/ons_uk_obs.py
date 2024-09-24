#import from system
from io import StringIO
from typing import List, Optional
from datetime import datetime as dt
from concurrent.futures import ThreadPoolExecutor as executor

# import from packages
import requests
import pandas as pd
import pendulum as pl

# import from app
from DBtransactions.DBtypes import Observation

URL = "https://www.ons.gov.uk/export"


def _process(resp: requests.Response, freq: str, ticker:Optional[str]=None) -> Optional[List[Observation]]:
    """
    process 
    """
    def _dat(date:pl.date):
        if date > pl.today():
            return date.subtract(years=100).to_date_string()
        return date.to_date_string()

    if resp.ok:
        df = pd.read_csv(StringIO(resp.text))
        result = []
        for i in df.index:
            try:
                if freq == "M":
                    dat = pl.from_timestamp(dt.timestamp((dt.strptime(df.iloc[i, 0], "%Y %b")))).to_date_string()
                else: #implemetar dados trimestrais
                    dat = pl.from_format(df.iloc[i, 0].replace("Q", ""), "YYYY Q").to_date_string()
                if isinstance(df.iloc[i, 1], str): 
                    srs = {"series_id": ticker.upper(), 
                           "dat": dat,
                           'valor': df.iloc[i, 1]}
                result.append(Observation(**srs))
            except Exception as e:
                pass
        return result

    else:
        print(f'ticker: {ticker} was not reached')


def _fetch(ticker:str, session, limit:Optional[int]=None):
    """
    Fecher auxiliar que faz todo trabalho de a) buscar as observações e b)
    processa-la
    """
    srs, ds = ticker.split(".")[1].split("_")
    freq = "M"
    if ds.lower() == 'mm23': # cpi
        uri = f"/economy/inflationandpriceindices/timeseries/{srs.lower()}/mm23"
    elif ds.lower() == "diop": # industry
        uri = f"economy/economicoutputandproductivity/output/timeseries/{srs.lower()}/diop"
    elif ds.lower() == "diop": # industry
        uri = f"economy/economicoutputandproductivity/output/timeseries/{srs.lower()}/diop"
    elif ds.lower() == "mgdp": # activity
        uri = f"/economy/grossdomesticproductgdp/timeseries/{srs.lower()}/mgdp"
    elif ds.lower() == "pn2": # GDP quartely
        freq = "Q"
        uri = f"economy/grossdomesticproductgdp/timeseries/ihyq/pn2"
    else: # retail
        uri = f"/businessindustryandtrade/retailindustry/timeseries/{srs.lower()}/drsi"
    
    headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    params = {'format': "csv",
              "uri": uri}
    resp = session.post(URL, data=params, headers=headers)
    return _process(resp, freq, ticker)


def fetch(tickers: List[str], limit:Optional[int]=None)-> List[List[Observation]]:
    """
    Fetch series from Office of National Statistics UK from
    tickers and retorn Series
    Ex:
    - srs = d7bt (cpi all items)
    - ds = mm23 (inflacao dateset)
    - see: https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/consumerpriceinflation
    """
    with requests.Session() as session:
        with executor() as e:
            obs = list(e.map(lambda tck: _fetch(tck.lower(), session), tickers, timeout=120))
    return obs
