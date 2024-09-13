# import from system
import io, re
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor as executor

# import from packages
import requests
import pandas as pd

# import from app
from DBtransactions.DBtypes import Observation
from DBtransactions.loaders.eurostat.eurostat_fetch_info import _form_full_ticker

url = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT'

def parse_date_q(dat: str):
    """
    convert a date in a format like 2010-Q1
    to 2010-01-01
    """
    ds = {"Q1": "01-01", 
          "Q2": "04-01",
          "Q3": "07-01",
          "Q4": "10-01"}
    y,t = dat.split("-")
    if "Q" in t:
        return f"{y}-{ds[t]}"
    return f"{y}-{t}-01"


def build_url(ticker):
    """
    forms the url for a particular series in order to fetch
    observations from eurostat's api
    """
    new_ticker = _form_full_ticker(ticker)
    return f"{url}/{'.'.join(new_ticker.split('.')[1:])}?format=csvdata&compress=false"


def _process(resp):
    """
    processes the response from the eurostat api
    """
    if resp.ok:
        s, e = re.search("(1.0)(.*)\?", resp.url).span()
        ticker = "EUROSTAT." + (resp.url)[s + 4: e -1]
        df = pd.read_csv(io.StringIO(resp.text))
        df = df.iloc[:, [-3, -2]].set_index("TIME_PERIOD").dropna()
        df.index = [parse_date_q(d) for d in df.index]
        df.columns = [ticker]
        return [Observation(**{'dat': i,
                 'valor': df.loc[i,ticker],
                 'series_id': ticker }) for i in df.index]
    else:
        print("Could not fetch data from eurostats api")

def fetch(tickers: List[str], limit=None) -> Dict:
    """
    Fetches the observations from the eurostat's api.
    ex:
    tickers = []
    """
    urls = (build_url(tck) for tck in tickers)
    
    with requests.session() as session:
        with executor() as e:
            llxs = e.map(lambda url:_process(session.get(url)), list(urls), timeout=20)
    return list(llxs)
