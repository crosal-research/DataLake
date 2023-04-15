# import from system
from typing import List
# import from packages
import pandas as pd

# import from app
from DBtransactions.DBtypes import Observation
from DBtransactions.loaders.fred import fred_obs
from DBtransactions.loaders.bls import bls_obs
from DBtransactions.loaders.ipea import ipea_obs
from DBtransactions.loaders.ibge import ibge_obs


fetchers = {"FRED":fred_obs.fetch, 
            "BLS": bls_obs.fetch, 
            "IPEA":ipea_obs.fetch, 
            "IBGE":ibge_obs.fetch}

def fetch(tickers:[List[str]]) -> List[List[Observation]]:
    """
    Funcao que agrega of fetchers the todas as fontes.
    Precisa organizar as lista de data frame de acorod
    com a ordem em que são listadas no input
    """
    sources = {}
    for tck in tickers: # group ticker by source
        s = tck.split(".")[0]
        if s in sources:
            sources[s].append(tck)
        else:
            sources[s] = [tck]
    llobs = []
    for s in sources:
        lobs = fetchers[s](sources[s])
        llobs= llobs + lobs
    return llobs
