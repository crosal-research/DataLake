############################################################
# Ingeri dados de observações de series disponibilizadas
# pelo o BIS
############################################################

# import from system
from concurrent.futures import ThreadPoolExecutor as executor
from typing import List
import xml.etree.ElementTree as ET

# import from packages
import requests
import pandas as pd


URL = "https://stats.bis.org/api/v1/data/"
INI = "2023-01-01"



# WS_CBPOL_D: daily policy rate
# WS_XRU_D: daily exchange rate

def _build_url(ticker:str) -> str:
    """
    Builds the url from the tickers of series
    to be used to fetch data from BIS api
    """
    return URL + ticker.partition(".")[-1] + "?"


def _process(resp: requests.Response) -> pd.DataFrame:
    """
    Process the response from the BIS and returns
    a DataFrame whose content are the observations
    of a particular series
    """
    root = ET.fromstring(resp.text)
    child = root[1].find("Series")
    data = {'TIME_PERIOD': [], 'OBS_VALUE': []}
    info = [child.get(k) for k in child.keys()]
    ticker = f"BIS.WS_ERR_M/{info[0]}.{info[1]}.{info[2]}.{info[3]}"
    for c in child:
        data['TIME_PERIOD'].append(c.get('TIME_PERIOD'))
        data['OBS_VALUE'].append(c.get('OBS_VALUE'))
        df = pd.DataFrame(data)
        df.columns = ['dat', ticker]
        df.set_index(['dat'])
    return df


def fetch(tickers:List[str], 
          ini:str=INI, end:str=None, limit:Optional[int]=None) -> List[pd.DataFrame]:
    """
    Fetches observations for tickers from BIS api
    and return a List of DataFrames, each one with
    with one of the series.
    """
    urls = [_build_url(tck) for tck in tickers]
    with requests.sessions.Session() as session:
        with executor() as e:
            dfs = list(e.map(lambda url:
                             _process(session.get(url, 
                                                  params={'startPeriod': ini, 
                                                        'detail': 'dataonly'})), urls))
    return dfs
