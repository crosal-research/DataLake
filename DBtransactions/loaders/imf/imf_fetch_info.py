##################################################
# Constroi informações para surveys do IMF
# 
##################################################


# import from system
from concurrent.futures import ThreadPoolExecutor as executor
from typing import List, Optional, Tuple
from functools import reduce

# import from packages
import requests

# import from App
from DBtransactions.DBtypes import Series

URL = "http://dataservices.imf.org/REST/SDMX_JSON.svc/DataStructure/"
DSURVEYS = {"IMF_PCPS": "IMF_PCPS"} # commodities



def _process(resp:requests.Response)-> Optional[List[Series]]:
    """
    Processes a requests.Response to capture info from series
    from a particular IMF's survey and return a list of tuples,
    each representing the following information: 
    (ticker, description, survey)
    """
    dfreq = {"M": "MENSAL"}
    
    if resp.ok:
        rj = resp.json()['Structure']['Concepts']['ConceptScheme']
        cl = resp.json()['Structure']['CodeLists']['CodeList']
        ident = rj['@id']
        name = rj['Name']['#text']

        survey = (resp.url).split("/")[-1]
        if survey in ['PCPS']:
            freq = 'M'
            area = 'W00'
            level = "IX"
        else:
            freq = 'M'
        aux = [c['Code'] for c in cl if c["@id"] == f"CL_INDICATOR_{survey}"][0]
        info = [Series(**{
            'series_id': f"IMF.{survey}/{freq}.{area}.{c['@value']}.{level}", 
            'description': c["Description"]["#text"], 
            'survey_id': f"IMF_{survey}",
            'frequency': dfreq[freq]}) for c in aux if c['@value'] != "All_Indicators"]
        return info
    return None


def fetch_info(surveys:List[str]) -> List[Series]:
    """
    Fetches the series' information belonging to the IMF's api.
    input: survey
    return: list(list(tuple(str, str, str) - [[(ticker, description, survey)]
    """
    urls = [URL + s.split("IMF_")[1] for s in surveys]
    with requests.sessions.Session() as session:
        with executor() as e:
            srs = list(e.map(lambda url: _process(session.get(url)), urls))
    return reduce(lambda x, y: x + y, srs)
