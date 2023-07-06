# import from the system
from typing import Optional, List
from datetime import datetime as dt

# imports from packages
import requests, pendulum
import pandas as pd
from bs4 import BeautifulSoup as bs

# imports from app
from DBtransactions.DBtypes import Observation

URL = "https://www.cpb.nl/en/worldtrademonitor"

def process(excel: pd.ExcelFile, ticker:str, dateFinal:str, limit) -> List[Observation]:
    sheet_name = "inpro_out" if "IPZ" in ticker else "trade_out"
    dates = [t.strftime("%Y-%m-%d") for t in 
                  pd.period_range(start="2000-01-01", end=dateFinal, freq="M")]
    df = excel.parse(sheet_name=sheet_name, 
                     skiprows=list(range(0,7)), 
                     nrows=31, header=None,
                     usecols= [2] + list(range(5, len(dates) + 5)), 
                     index_col=[0]).dropna(axis=0)
    df.columns = [t.strftime("%Y-%m-%d") for t in 
                  pd.period_range(start="2000-01-01", end=dateFinal, freq="M")]
    df.index = [i.upper() for i in df.index]
    return [Observation(**{
        'series_id': ticker,
        'dat': c,
        'valor': df.loc[ticker.split(".")[1], c]}) for c in df.columns]


def fetch(tickers: List[str], limit: Optional[int]=None) -> List[List[Observation]]:
    """
    ingest a list of tickers (str) and returns a list of list
    of observations, each one of which pertaining to a particular
    ticker
    """
    headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
    resp = requests.get(URL, headers=headers)
    soup = bs(resp.text, "html.parser")
    url = [l for l in soup.find_all('a') if 'Download' in l][0].attrs['href']
    dateFinal = pendulum.from_format((url.split("Monitor-")[1]).split(".")[0], "MMMM-YYYY")
    excel = pd.ExcelFile(url)
    lxs = [process(excel, tck, dateFinal, limit) for tck in tickers]
    return lxs

