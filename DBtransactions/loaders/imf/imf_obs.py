############################################################
# Ingeri dados de observações de series disponibilizadas
# pelo o IMF
############################################################


# import from system
from concurrent.futures import ThreadPoolExecutor as executor
from typing import List, Optional
import time

# import form packages
import requests
import pendulum


# import from App
from DBtransactions.DBtypes import Observation

URL = "http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/"
ticker = ["IMF.PCPS/M.W00.PAGRI.IX", "IMF.PCPS/M.W00.PRAWM.IX"]
surveys = {"IMF_PCPS": "PCPS/M.W00..IX"}

# @FREQ: "M",
# @REF_AREA: "W00",
# @COMMODITY: "PAGRI",
# @UNIT_MEASURE: "IX",
# @UNIT_MULT: "0",
# @TIME_FORMAT: "P1M",
# dots separe features


def _build_url(ticker:Optional[str]=None, 
               survey:Optional[str]=None) -> str:
    return URL + ticker.partition(".")[-1]



def _process(resp:requests.Response) -> List[Observation]:
    """
    Processes response from IMF api into a 
    DataFrame:
    df.index.name = 'dat'
    df.columns = [ticker]
    """
    if resp.ok:
        data = resp.json()['CompactData']['DataSet']['Series']['Obs']
        ticker = (resp.url).split('CompactData/')[1]
        return [Observation(**{'series_id': "IMF." + ticker, 
                            'dat': pendulum.parse(d['@TIME_PERIOD']).to_date_string(), 
                            'valor': d['@OBS_VALUE']}) for d in data]
    else:
        print("Fail to reach IMF API")


def fetch(tickers: List[str],
          ini: Optional[str]=None, 
          end: Optional[str]=None, 
          limit:Optional[int]=None) -> List[List[Observation]]:
    """
    Fetches, process and returns a list of dataframe with 
    observations fetched from IMf's api
    """
    llobs = []
    urls = [_build_url(tck) for tck in tickers]
    for url in urls:
        llobs.append(_process(requests.get(url)))
        time.sleep(0.6) # necessary, given the api time limit
    return llobs

