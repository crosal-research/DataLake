#######################################################################
# see: https://github.com/mbk-dev/nbsc/blob/master/nbsc/request_data.py
#######################################################################

# date: 16/07/2023
# missing: paralellize the fetch code

# imports from system
import json
from datetime import datetime
from typing import List, Dict

# import from packages
import pandas as pd
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# import from app
from DBtransactions.DBtypes import Series

dir = "/home/jmrosal/datalake/api/DBtransactions/loaders/nbsc/"
 

with open(dir + 'data.json', 'r') as f:
    DATA = json.loads(f.read())
requests.packages.urllib3.disable_warnings()


# file constantes
BASE_URL_ENG = "http://data.stats.gov.cn/english/easyquery.htm"
default_timeout = 240  # seconds


def _process(resp: dict, data) -> List[str]:
    freq = resp['returndata']['wdnodes'][1]['wdname'].lower()
    new_freq = 'MENSAL' if (freq == 'month') else 'TRIMESTRAL'
    survey = [d for d in data if d['valuecode'] == resp['survey']][0]
    return [Series(**{'series_id':"NBSC." + r['code'] + '_' + survey['survey'].split('_')[1], 
            'description':r['cname'], 
             'survey_id': survey['survey'],
             'last_update': None,
             'frequency': new_freq }) for r in resp['returndata']['wdnodes'][0]['nodes']
            if all(f in r['cname'].upper() for f in survey['filter'])]

   
def fetch_info(survey: str) -> List[Series]:
    """
    Fetch & parse from the China National Bureau of Statistics web data API.
    survey's name follows the name by the DB (ex: 'NBSC_PIBY')
    """
    # Parameters for constructing the query string
    valuecode = [d['valuecode'] for d in DATA if d['survey'] == survey][0]
    
    params = {
        "m": "QueryData", # Method of easyquery.htm to call
        "colcode": "sj", # Periods are always one dimension of the returned data
        "k1": int(datetime.now().timestamp() * 1000), # Timestamp
    }

    # Wrap series and periods in the form expected by the query string
    _survey = {"wdcode": "zb", 
               "valuecode": valuecode}
    _periods = {"wdcode": "sj", "valuecode": "LAST1"}

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

    # Prepare the HTTP request
    session = requests.session()
    retry_strategy = Retry(total=3, backoff_factor=0.1, 
                           status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)

    try:
        r = session.get(BASE_URL_ENG, params=params, 
                        verify=False, timeout=default_timeout)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise requests.exceptions.HTTPError(
            f"HTTP error fetching data for {survey}:",
            r.status_code,
            r.reason,
            BASE_URL_ENG,
        ) from err
    finally:
        session.close()
    response = r.json()
    response['survey'] = valuecode
    if response["returncode"] == 501:
        raise requests.exceptions.HTTPError(f"{survey} is not found in the database.", 
                                            501)
    lxs = _process(response, DATA)
    return lxs

