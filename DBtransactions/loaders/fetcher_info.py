##################################################
# Upserts series into the database
##################################################
# import from system
from typing import List, Optional

# import from packages
import pandas as pd


# import from app
from DBtransactions.loaders.fred import fred_series_add
from DBtransactions.loaders.ipea import ipea_info


def fetch_infos(source:str=None, 
               tickers:Optional[List[str]]=None)-> pd.DataFrame:
    if source:
        if source == "IPEA":
               df = ipea_info.fetch_info(ipea_info.tickers_ipea[0:1])
        else:
               pass
    else:
        pass

