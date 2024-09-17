##################################################
# Fetchs ons data
#
##################################################
# import from system
from typing import List, Optional
from functools import reduce
from concurrent.futures import ThreadPoolExecutor as executor
from io import StringIO

# packages import
import requests, pendulum
import pandas as pd

# import app
from DBtransactions.DBtypes import Observation

URL = 'https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/ena_subsistema_di/'
FINAL = 2024
INI = 2001

def _build_url(ano:str):
    """
    build the relevant url to fetch data
    """
    # return URL + f"ENA_DIARIO_SUBSISTEMA_{ano}.csv"
    return URL + f"ENA_DIARIO_SUBSISTEMA_{ano}.csv"


def _process(resp:requests.Response) -> Optional[List[Observation]]:
    """
    Takes a resquests.Response object, processes it and returns
    a list of the Observation object
    """
    # info = list(map(lambda line: line.split(';'), 
    #            (resp.text).split("\n")))
    
    if(resp.ok):
        df = pd.read_csv(StringIO(resp.text), sep=";", decimal=",")
        return [Observation(**{'series_id': f"ONS.ENAPERC_{df.loc[i, ['id_subsistema']][0]}", 
                               'dat': df.loc[i, ["ena_data"]][0], 
                               'valor': df.loc[i, ["ena_bruta_regiao_percentualmlt"]][0]}) for i in df.index]
    return None

def fetch(tickers: List[str], limit:Optional[str]=None) -> List[List[Observation]]:
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
