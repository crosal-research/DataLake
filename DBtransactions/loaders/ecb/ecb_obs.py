# import from app
from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor
import functools as ft

# import from packages
import requests
import pendulum
import pandas as pd

# import from app
from DBtransactions.DBtypes import Observation
from DBtransactions.loaders.ecb.ecb_fetch_info import _fetch_dataflow


DATE_INI = "2020-01-01"
URL = 'https://data-api.ecb.europa.eu/service/data'
surveys = {"ECB_EXR": {'dataflow': "EXR", 'freq': "D", 'ident': "SP00.A"}, 
           "EXC_FM":  {'dataflow':  "FM", 'freq': "D"}}


def _build_url(ticker:str) -> str:
    """
    takes a string with ticker format from database, 
    optional star periodand return the url to fetch the data
    """
    dataflow = _fetch_dataflow(ticker)
    if dataflow == "EXR":
        if ticker in ["ECB.USD/EUR", "ECB.EUR/USD"]:
            cur = "USD"
        else:
            cur1, cur2 = (ticker.split(".")[1]).split("/")
            cur = cur1 if cur1 != 'USD' else cur2
        survey = surveys['ECB_EXR']
        df, f, i = [survey[s] for s in ['dataflow', 'freq', 'ident']]
        return f"{URL}/{dataflow}/{f}.{cur}.{'EUR'}.{i}"
    else:
        rate = ticker.split(".")[1]
        return f"{URL}/{dataflow}/D.U2.EUR.4F.KR.{rate}.LEV"

        
def _process(resp: requests.Response) -> List[Observation]:
    """
    process response from franfurt app for 
    sigle ticker
    """
    info = resp.json()
    if (resp.url).split('data/')[1].split("/")[0]  == "EXR":
        cur = info['structure']['dimensions']['series'][1]['values'][0]['id']
        obs = [i[0] for i in info['dataSets'][0]['series']['0:0:0:0:0']['observations'].values()]
        dat = [d['name'] for d in info['structure']['dimensions']['observation'][0]['values']]
        return  pd.DataFrame(data = obs, index = dat, columns = [cur])

    cur = info['structure']['dimensions']['series'][5]['values'][0]['id']
    obs = [i[0] for i in info['dataSets'][0]['series']['0:0:0:0:0:0:0']['observations'].values()]
    dat = [d['name'] for d in info['structure']['dimensions']['observation'][0]['values']]
    df = pd.DataFrame(data = obs, index = dat, columns = [cur])
    return df


def fetch(tickers: List[str], limit:Optional[str]=None) -> List[List[Observation]]:
    """
    takes a list of tickers and initial date (str)
    and return a list of Observations
    """
    are_there_currencies = any(["EXR" == _fetch_dataflow(tck) for  tck in tickers])
    
    if are_there_currencies:
        ntickers = list(set(tickers + ["ECB.EUR/USD"])) # need this to convert currencies.
    else:
        ntickers = tickers
    if limit in [None, '']:
        limit = pendulum.today().diff(pendulum.parse(DATE_INI)).in_days()
    urls = [_build_url(tck) for tck in ntickers]
    lxs = []
    session = requests.Session()

    def _fetch(u):
        try:
            resp = session.get(u, params={'lastNObservations': limit, 
                                          'format': 'jsondata', 
                                          'detail': 'dataonly'})
            if resp.ok:
                return _process(resp)
        except:
            print(f'couldnt reacch {u}')
        return None

    with ThreadPoolExecutor(max_workers=5) as executor:
        dfs = list(executor.map(lambda url: _fetch(url), urls, timeout=60))

    dfs_new = ft.reduce(lambda left, right: 
                        pd.merge(left, right, left_index=True, right_index=True, how='outer'), dfs)
    
    def _filter_ticker(ticker):
        """
        Defines temporary ticker to calculate the reciprocate of the
        fetched exchanges rates
        """
        return (ticker.split(".")[1]).split("/")

    def _new_df(df: pd.DataFrame, ticker):
        """
        Needed to:
        - calculate the relevante exchange rates
        - define the right ticker for the series to be inserted
        """
        if _fetch_dataflow(ticker) == 'EXR':
            ftcks = _filter_ticker(ticker)
            if ticker in ["ECB.EUR/USD", "ECB.USD/EUR"]:
                ds = pd.DataFrame(df.loc[: , 'USD'])
                ds.columns = [ticker]
                return ds
            else:
                return  pd.DataFrame(df.loc[: , ftcks[1]]/df.loc[:, ftcks[0]], columns=[ticker])
        else:
            return pd.DataFrame(data=dfs_new.loc[:, ticker.split(".")[1]].values, 
                                columns=[ticker], index=dfs_new.index)

    dfs_final =  [ _new_df(dfs_new, tck) for tck in tickers]

    session.close()

    series_obs = []
    for d in dfs_final:
        obs = []
        for i in d.index:
            obs.append(Observation(**{'series_id': d.columns[0], 'dat': i, 'valor': d.loc[i].values}))
        series_obs.append(obs)
    return series_obs
