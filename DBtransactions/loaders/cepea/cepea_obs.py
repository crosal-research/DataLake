################################################################################
# fetches data from cepea database
# and adds to the economic database
#
# Obs:
# for clarification in regards to the olefile module check
# this stackoverflow thread: https://stackoverflow.com/questions/
# 58336366/compdocerror-when-importing-xls-file-format-to-python-using-pandas-read-excel
################################################################################

# import form the system
from concurrent.futures import ThreadPoolExecutor as executor
import time, tempfile, re
from typing import Optional
from datetime import datetime as dt
from functools import reduce

# import from packages
import requests, xlrd
import pandas as pd

#app imports
from DBtransactions.DBtypes import Observation
from DBtransactions.loaders.cepea.cepea_fetch_info import INFO

__all__ = ["fetch", "tickers"]


def build_url(ticker) -> str:
    """builds the relevant url for the ticker in case
    """
    number = ticker.split(".")[1]
    cultura = [s[4] for s in INFO if s[0] == ticker][0]
    return f'https://cepea.esalq.usp.br/br/indicador/series/{cultura}.aspx?id={number}'


def process(resp:requests.models.Response, limit=None) -> pd.DataFrame:
    """
    fetches the series related to the url used as input. Return a 
    dataframe
    """
    if resp.ok:
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(resp.content)
            fp.seek(0)
            sheet = xlrd.open_workbook(fp.name, ignore_workbook_corruption=True).sheet_by_index(0)
        ind = [dt.strptime(c, "%d/%m/%Y") for c in sheet.col_values(0) if re.match("\d\d/\d\d/\d\d", c)]
        values = [c for c in sheet.col_values(1) if isinstance(c, float)]
        ticker = "CEPEA." + re.search("\d{1,3}", resp.url)[0]
        df = pd.DataFrame(data=values, index=ind, columns=[ticker])
        try: 
            df_new = df.applymap(lambda v: float(v)) # if limit is None else df.applymap(lambda v: float(v)).tail(limit)
        except:
            print('fail to convert')
        return [Observation(**{"series_id":df_new.columns[0], 
                               'dat': i.strftime("%Y-%m-%d"), 
                               'valor': df_new.loc[i, ticker]}) for i in df_new.index ]
    else:
        print(f"Could not reache {resp.url}")


def fetch(tickers: list, limit: Optional[int]=None) -> None:
    """Upserts data, fetching from sourcing and adding into the database.
    tickers defines which series should be upserted, and limit are the 
    tail observations to be inserted. If limit is None, all
    observations are inserted
    """
    urls = [build_url(tck) for tck in tickers]
    headers = {'User-Agent': 
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' + \
               "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
    with requests.session() as session:
        with executor() as e:
            srs = list(e.map(lambda url:process(session.get(url, headers=headers), limit=limit), 
                             list(urls)))
    
    return srs


