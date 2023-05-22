############################################################
# Ingeri dados de observações de series disponibilizadas
# pelo o BIS
############################################################

# import from system
from concurrent.futures import ThreadPoolExecutor as executor
from typing import List, Optional
import xml.etree.ElementTree as ET

# import from packages
import requests
import pendulum

# import from App
from DBtransactions.DBtypes import Observation


URL = "https://stats.bis.org/api/v1/data/"
INI = "1980-01-01"


# WS_CBPOL_D: daily policy rate
# WS_XRU_D: daily exchange rate

def _build_url(ticker:str) -> str:
    """
    Builds the url from the tickers of series
    to be used to fetch data from BIS api
    """
    return URL + ticker.partition(".")[-1] + "?" 


def _process(resp: requests.Response) -> List[Observation]:
    """
    Process the response from the BIS and returns
    a DataFrame whose content are the observations
    of a particular series
    """
    root = ET.fromstring(resp.text)
    child = root[1].find("Series")
    info = [child.get(k) for k in child.keys()]
    ticker = f"BIS.WS_EER_M/{info[0]}.{info[1]}.{info[2]}.{info[3]}"
    return [Observation(**{'series_id': ticker, 
                           'dat': pendulum.parse(c.get('TIME_PERIOD'), exact=True).to_date_string(), 
                           'valor': float(c.get('OBS_VALUE'))}) 
            for c in child ]

def fetch(tickers:List[str], 
          ini:str=INI, end:str=None, limit:Optional[int]=None) -> List[List[Observation]]:
    """
    Fetches observations for tickers from BIS api
    and return a List of Lists of Observaton, each one with
    with one of the series.
    """
    urls = [_build_url(tck) for tck in tickers]
    with requests.sessions.Session() as session:
        with executor() as e:
            srs = list(e.map(lambda url:
                             _process(session.get(url, 
                                                  params={'startPeriod': ini, 
                                                        'detail': 'dataonly'})), urls))
    return srs
