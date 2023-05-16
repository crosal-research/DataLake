##################################################
# Fetchs ons data
#
##################################################
# import from system
from typing import List, Optional
from functools import reduce
from concurrent.futures import ThreadPoolExecutor as executor

# packages import
import requests, pendulum

# import app
from DBtransactions.DBtypes import Observation


URL = 'https://ons-dl-prod-opendata.s3.amazonaws.com/dataset/ena_subsistema_di/'
FINAL = 2023
INI = 2000

def _build_url(ano:str):
    """
    build the relevant url to fetch data
    """
    return URL + f"ENA_DIARIO_SUBSISTEMA_{ano}.csv"


def _process(resp:requests.Response) -> Optional[List[Observation]]:
    """
    Takes a resquests.Response object, processes it and returns
    a list of the Observation object
    """
    info = list(map(lambda line: line.split(';'), 
               (resp.text).split("\n")))
    return [Observation(**{'series_id': f"ONS.ENAPERC_{l[0]}", 
             'dat': l[2], 
             'valor': l[-1]}) for l in info[1:-1]]


def fetch(tickers: List[str], limit=None) -> List[List[Observation]]:
    """
    takes of list of ons tickers, and return a list of list of Observation,
    each one pertaining to a particular series
    """
    ini = pendulum.now().subtract(days=limit + 5).year if limit else INI
    urls = [_build_url(ano) for ano in range(ini, FINAL + 1)]
    with requests.Session() as session:
        with executor() as e:
            obs = list(e.map(lambda u: _process(session.get(u)), urls))
    flatobs = reduce(lambda x, y: x + y, obs)
    sepobs = {k:[] for k in tickers}
    for o in flatobs:
        if o.series_id in tickers:
            sepobs[o.series_id].append(o)
    return [sepobs[k] for k in sepobs]
