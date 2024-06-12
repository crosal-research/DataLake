# import from system
from typing import List, Optional
# import from packages
import pandas as pd

# import from app
from DBtransactions.DBtypes import Observation
from DBtransactions.loaders.fred import fred_obs
from DBtransactions.loaders.bls import bls_obs
from DBtransactions.loaders.ipea import ipea_obs
from DBtransactions.loaders.ibge import ibge_obs
from DBtransactions.loaders.bcb import bcb_obs
from DBtransactions.loaders.imf import imf_obs
from DBtransactions.loaders.bcb_exp import bcb_exp_obs
from DBtransactions.loaders.ons import ons_obs
from DBtransactions.loaders.bis import bis_obs
from DBtransactions.loaders.bea import bea_obs
from DBtransactions.loaders.cepea import cepea_obs
from DBtransactions.loaders.cpb import cpb_obs
from DBtransactions.loaders.nbsc import nbsc_obs
from DBtransactions.loaders.caged import caged_obs
from DBtransactions.loaders.nasdaq import nasdaq_obs
from DBtransactions.loaders.cni import cni_obs
from DBtransactions.loaders.anfavea import anfavea_obs
from DBtransactions.loaders.stn import stn_obs
from DBtransactions.loaders.ecb import ecb_obs


fetchers = {
    "FRED":fred_obs.fetch, 
    "BLS": bls_obs.fetch, 
    "IPEA":ipea_obs.fetch, 
    "IBGE":ibge_obs.fetch,
    "BCB": bcb_obs.fetch, 
    "IMF": imf_obs.fetch,
    "BCB_EXP": bcb_exp_obs.fetch, 
    "ONS": ons_obs.fetch,
    "BIS": bis_obs.fetch,
    "BEA": bea_obs.fetch,
    "CEPEA": cepea_obs.fetch,
    "CPB": cpb_obs.fetch,
    "NBSC": nbsc_obs.fetch,
    "CAGED": caged_obs.fetch, 
    "NASDAQ": nasdaq_obs.fetch,
    "CNI": cni_obs.fetch,
    "ANFAVEA": anfavea_obs.fetch,
    "STN": stn_obs.fetch,
    "ECB": ecb_obs.fetch
    }


def fetch(tickers: List[str],
          limit:Optional[str]=None) -> List[List[Observation]]:
    """
    Funcao que agrega of fetchers the todas as fontes.
    Precisa organizar as lista de data frame de acordo
    com a ordem em que são listadas no input
    """
    sources = {}
    for tck in tickers: # group ticker by source
        s = tck.split(".")[0]
        # exceptions to the rule the before dot maps to directly fetchers
        if (s.upper() == "BCB") and ("EXP" in tck.upper()): 
                s = "BCB_EXP"
        if s in sources:
            sources[s].append(tck)
        else: 
            sources[s] = [tck]

    llobs = []
    for s in sources:
        llobs= llobs + fetchers[s](sources[s], limit=limit)
    return llobs
