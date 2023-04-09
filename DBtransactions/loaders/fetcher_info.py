##################################################
# Upserts series into the database
##################################################
# import from system
from typing import List, Optional, Tuple

# import from packages
import pandas as pd


# import from app
from DBtransactions.loaders.fred import fred_fetch_info
from DBtransactions.loaders.ipea import ipea_fetch_info
from DBtransactions.loaders.bls import bls_fetch_info


dispatcher = {"FRED": fred_fetch_info.fetch_info,
              "IPEA": ipea_fetch_info.fetch_info, 
              "BLS": bls_fetch_info.fetch_info }


def fetch_infos(source:str=None, 
               tickers:Optional[List[str]]=None)-> List[Tuple[str]]:
    if source == "IPEA":
       dfs = dispatcher[source](ipea_fetch_info.tickers_ipea)
    elif source == "BLS":
       dfs = dispatcher[source](bls_fetch_info.path_to_file)
    else:
        sources = set([tck.split(".")[0] for tck in tickers])
        dfs = []
        for s in sources: # precisa fazer asincrono
            aux = [tck for tck in tickers 
                      if tck.split(".")[0] == s]
            dfs = dfs + dispatcher[s](aux)
    return dfs

