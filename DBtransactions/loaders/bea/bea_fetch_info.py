# imports from the system
from concurrent.futures import ThreadPoolExecutor as executor
from typing import List
from functools import reduce
import re


# imports from packages 
import requests
from dotenv import dotenv_values

# import from app
from DBtransactions.DBtypes import Series


config = dotenv_values("./.env")
_bea_key=config["BEA_KEY"]


dataset = {"NIPA": "National Accounts and Product Accounts"}

#dataset/table/freq
TABLES = {'BEA_GDP': ["NIPA/T10106/Q", #real gdp, chained usd (sea)
                      "NIPA/T10102/Q"], #real gdp, contribution
          'BEA_CONSUMER': ["NIPA/T20600/M", #personal income and its disposition
#                          "NIPA/T20806/M",
                           "NIPA/T20804/M"]} #real personal consumption


def build_url(tbl:str, key:str) -> str:
    """"
    - table: for the relevant bea table
    - key for bea api
    ex: 
    tbl = NIPA/T10101/Q
    key = bea api_key
    Y: Frequency
    """
    url_bea = f'https://apps.bea.gov/api/data?&UserID={key}&method=GetData'
    t = tbl.split('/')
    return f"{url_bea}&datasetname={t[0]}&Tablename={t[1]}&Frequency={t[2]}&Year=2020"

  
def _build_series(tbl:str, obs:dict, freq:str) -> Series:
    """
    from the information in the ticker defining a table, the dictionary
    derived from the resquest (after the due manipulation) and the frenquecy
    desired [Q, A] builds the ticker and a list of all the information needed
    to build a series to be added in the database.
    """
    ticker = f"BEA.{tbl}/{obs['TableName']}/{obs['SeriesCode']}/{freq}".upper()
    contrib = 'Contribution to GDP: ' if 'T10102' == obs['TableName'] else ''
    description = f"{obs['LineDescription']}, {obs['CL_UNIT']} - {dataset[tbl]}"
    country = "U.S.A"
    survey = "BEA_CONSUMER" if ("T2" in ticker) else "BEA_GDP"
    return Series(**{'series_id': ticker, 
                     'description': f"{contrib}" + description + f", {country} ", 
                     'survey_id': survey, 
                     'frequency': {"Q":'TRIMESTRAL',
                                   "M":'MENSAL',
                                   "A":'ANUAL'}[freq]})

 
def process(resp: requests.models.Response) -> List[Series]:
    """
    takes a response from a request and return a list of list.
    Each list within the output provides the information to be added into 
    the database as a series.
    """
    url =  resp.url
    freq = re.search(r"(?<=Frequency=)[A-Z]+(?=&)", url).group(0) #fetches frequency
    tbl =  re.search("(?<=datasetname=)[A-Z]+(?=&)", url).group(0) #fetches table info
    obs =  resp.json()["BEAAPI"]["Results"]["Data"]
    jump = {"Q": 4, "M": 12, "A": 1} 
    return [_build_series(tbl, obs[i], freq) for i in range(0, len(obs), jump[freq])]


def fetch_info(tables:List[str]) -> List[Series]:
    """
    takes a list of tables and returns
    list of Series
    """
    urls = [build_url(tbl, _bea_key) for tbl in tables]
    with requests.session() as session:
        with executor() as e:
            srs = list(e.map(lambda u: process(session.get(u)), urls))
    return reduce(lambda x, y: x + y, srs)
