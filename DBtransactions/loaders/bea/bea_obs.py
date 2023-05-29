# import system
from concurrent.futures import ThreadPoolExecutor as executor
import locale
from typing import List, Optional
from functools import reduce

# import from packages
import requests
from dotenv import dotenv_values
import pendulum

# import from app
from DBtransactions.DBtypes import Observation


config = dotenv_values("./.env")
_bea_key=config["BEA_KEY"]
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def grab_tables(tickers: list) -> set:
    """
    ex: tickers = ['BEA.NIPA/T10106/A191RX/Q', 'BEA.NIPA/T10106/B009RX/Q'] -> 
    """
    def _rem(lsep):
        return "/".join([lsep[0].split(".")[1], lsep[1], lsep[3]])
    return set([_rem(tck.split("/")) for tck in tickers])


def build_url(table:str, key:str, limit) -> str:
    """"
    - table: for the relevant bea table
    - key for bea api
    ex: 
    table = NIPA/T10101/M
    key = _bea_key
    """
    url_bea = f'https://apps.bea.gov/api/data?&UserID={key}&method=GetData'
    t = table.split('/')
    if limit is None:
        per = "X"
    else:
        year = pendulum.now().year
        per = ",".join([str(p) for p in range(year-limit, year+1)])
    return f"{url_bea}&datasetname={t[0]}&Tablename={t[1]}&Frequency={t[2]}&Year={per}"

            
def process(resp:requests.models.Response) -> List[Observation]:
    """
    takes a response from a request pertaining to a table, process it into 
    a dataframe, filter the relevant tickers and return the final
    dataframe
    """
    global r
    r = resp.json()
    freq = [d['ParameterValue'] for d in r["BEAAPI"]["Request"]["RequestParam"] 
            if d['ParameterName'] == "FREQUENCY"][0]
    data = r["BEAAPI"]["Results"]["Data"]
    
    def _date(date:str, freq):
        """helper function to return data string in the right format
        date: input string date
        freq: frequency
        """
        d = date.replace(freq, "-")
        return (pendulum.from_format(d, f"YYYY-{freq}")).format("YYYY-MM-DD")
    
    return [Observation(
        **{'series_id':f"BEA.NIPA/{d['TableName']}/{d['SeriesCode']}/{freq}" ,
           'valor': locale.atof(d['DataValue']),
           'dat': _date(d['TimePeriod'], freq)}) for d in data]


def fetch(tickers: List[str], limit:Optional[int]=None) -> List[List[Observation]]:
    """
    
    """
    urls = [build_url(t, _bea_key, limit) for t in grab_tables(tickers)]
    with requests.Session() as session:
        with executor() as e:
            srs = list(e.map(lambda u: process(session.get(u)), urls))
    
    ds = {}

    for l in [d for d in reduce(lambda x, y: x + y, srs) if d.series_id in tickers]:
        if (l.series_id in ds):
            ds[l.series_id].append(l)
        else:
            ds[l.series_id] = [l]
    return list(ds.values())
