############################################################
# Fetch observations for median expectations from
# BCB's Api
# Last modification: 4/05/2923
############################################################

# import from system
import re
from datetime import datetime as dt
from typing import Optional, List, Dict
from concurrent.futures import ThreadPoolExecutor as executor

# import from packages
import pendulum, requests
import pandas as pd

# import from app
from DBtransactions.DBtypes import Observation


URL:str = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/"
LIMIT:int = 5000
INDICADOR_MAP:dict = {"SELICEXP": "Selic", 
                      "PIBEXP": "PIB Total", 
                      "CAMBIOEXP": "Câmbio",
                      "IPCAEXP": "IPCA"} # relates API's name with BC's API.


def _build_url(ticker, limit:int= LIMIT) -> str:
    """
    Builds the relevant url for a particular ticker
    """
    ind, period = (ticker.split(".")[1]).split("_")
    QUERY = f"&$orderby=Data%20desc&$format=json&$select=Indicador,Data,Mediana&$top={limit}" + \
        f"&$filter=Indicador%20eq%20'{INDICADOR_MAP[ind]}'"
    if "FINAL" in period:
        year = re.match("\d+", period)[0]
        return URL + "ExpectativasMercadoAnuais?" + QUERY + \
            f"%20and%20DataReferencia%20eq%20'{year}'"
    return URL + "ExpectativasMercadoInflacao12Meses?" + QUERY
    

def _process(resp:requests.models.Response) -> List[Dict]:
    """
    Process response from BCB'api for expectations, return 
    a list with observations in the response
    """
    url = resp.url
    if "12Meses" in resp.url:
        ticker = "BCB.IPCAEXP_12M"
    else:    
        if "IPCA" in url:
            indicador = "IPCA"
        elif "C%C3%A2mbio" in url:
            indicador = "CAMBIO"
        elif "PIB" in url:
            indicador = "PIB"
        else:
            indicador = "SELIC"
        year = re.findall("\d+", url.split("DataReferencia")[1])[-1]
        ticker = f"BCB.{indicador}EXP_{year}FINAL"

    rd = resp.json()
    return [Observation(**{"series_id": ticker, "dat": d['Data'], "valor": d['Mediana']})
                for d in rd['value'][0::4]]


def fetch(tickers:List[str], limit:Optional[int]=LIMIT) -> List[List[Dict]]:
    """
    Feches list observations pertaining to a tickers. Length of the observations
    is given by limit
    """
    urls = [_build_url(tck) for tck in tickers]
    with requests.session() as session:
        with executor() as e:
            ls = list(e.map(lambda url:_process(session.get(url)), list(urls)))
    return ls
