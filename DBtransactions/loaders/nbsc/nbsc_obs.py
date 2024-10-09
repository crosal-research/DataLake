#######################################################################
# see: https://github.com/mbk-dev/nbsc/blob/master/nbsc/request_data.py
#######################################################################

# imports from system
import json
from datetime import datetime as dt
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor as executor
import re
from functools import reduce

# import from packages
import pendulum as pd
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# import from app
from DBtransactions.DBtypes import Observation


requests.packages.urllib3.disable_warnings()

# file constantes
BASE_URL_ENG = "http://data.stats.gov.cn/english/easyquery.htm"
default_timeout = 240  # seconds


dir = "/home/jmrosal/datalake/api/DBtransactions/loaders/nbsc/"

with open(dir + 'data.json', 'r') as f:
    DATA = json.loads(f.read())
requests.packages.urllib3.disable_warnings()


LLower = "1996"
LUpper = f"{dt.today().year}"



def _process(resp: dict) -> List[str]:
    def _to_date(dat):
        if (x:=re.search("[A-D]", dat)):
            d = dat.replace(x[0], {"A": "01", "B": "04", 
                                   "C": "07", "D": "10"}[x[0]])
        else:
            d = dat
        return (pd.from_format(d, "YYYYMM")).format("YYYY-MM-DD")

    def _normalize(info):
        if (info[:5] !=  "A0B01"):
            return 0
        else:
            return 0

    return [Observation(**{'series_id':'NBSC.' + d['wds'][0]['valuecode'] + '_' + resp['survey'].split("_")[1], 
             'dat':_to_date(d['wds'][1]['valuecode']).format("Y-MM-DD"), 
             'valor': str(float(d['data']['strdata']) + _normalize(d['wds'][0]['valuecode']))}) 
            for d in resp['returndata']['datanodes']  if d['data']['strdata'] != '']

   
def fetch(series: List[str], limit=None) -> List[List[Observation]]:
    """
    Fetch & parse from the China National Bureau of Statistics web data API.
    """
    periods = limit if limit else f"{LLower}-{LUpper}"
    surveys = list(set([srs.split(".")[0] + "_" + srs.split("_")[1] for srs in series]))
    # Prepare the HTTP request
    session = requests.session()
    retry_strategy = Retry(total=3, backoff_factor=0.1, 
                           status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)

    def _fetch(survey):
        # Parameters for constructing the query string
        
        valuecode = [d['valuecode'] for d in DATA if d['survey'] == survey][0]
        params = {
            "m": "QueryData", # Method of easyquery.htm to call
            "colcode": "sj", # Periods are always one dimension of the returned data
            "k1": int(dt.now().timestamp() * 1000), # Timestamp
        }

        # Wrap series and periods in the form expected by the query string
        _survey = {"wdcode": "zb", "valuecode": valuecode}
        _periods = {"wdcode": "sj", "valuecode": periods}
        freq = [d['freq'] for d in DATA if d['survey']== survey][0].lower()
        d_freq = {'month':   'hgyd',
              'quarter': 'hgjd',
              'annual':  'hgnd'}

        params["dbcode"] = d_freq[freq]
        params['rowcode'] = "zb"

        # Two dimensional data: leave this blank
        wds = []
        # Select both series and periods
        dfwds = [_survey, _periods]

        # Convert the wds and dfwds parameters to stringified JSON
        seps = (",", ":")
        params["wds"] = json.dumps(wds, separators=seps)
        params["dfwds"] = json.dumps(dfwds, separators=seps)

        try:
            r = session.get(BASE_URL_ENG, params=params, 
                            verify=False, timeout=default_timeout)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise requests.exceptions.HTTPError( f"HTTP error fetching data for {survey}:",
                r.status_code,
                r.reason,
                BASE_URL_ENG,) from err
        response = r.json()
        response['survey'] = survey
        if response["returncode"] == 501:
            raise requests.exceptions.HTTPError(f"{survey} is not found in the database.", 501)
        return _process(response)

    with executor(max_workers=2) as e:
        srs = e.map(_fetch, surveys)
    session.close()                                            

    lsrs = list(srs)
    lxs = {}
    for sr in reduce(lambda x, y: x + y, lsrs, []):
        k = sr.series_id
        if k in series:
            if k in lxs:
                lxs[k].append(sr)
            else:
                lxs[k] = [sr]
    return list(lxs.values())
