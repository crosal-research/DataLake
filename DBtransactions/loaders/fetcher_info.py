##################################################
# Upserts series into the database
##################################################
# import from system
from typing import List, Optional, Tuple
from functools import reduce

# import from packages
import pandas as pd

# import from app
from DBtransactions.DBtypes import Series
from DBtransactions.loaders.fred import fred_fetch_info
from DBtransactions.loaders.ipea import ipea_fetch_info
from DBtransactions.loaders.bls import bls_fetch_info
from DBtransactions.loaders.bis import bis_fetch_info
from DBtransactions.loaders.ibge import ibge_fetch_info
from DBtransactions.loaders.bcb import bcb_fetch_info
from DBtransactions.loaders.imf import imf_fetch_info
from DBtransactions.loaders.bcb_exp import bcb_exp_fetch_info
from DBtransactions.loaders.ons import ons_fetch_info
from DBtransactions.loaders.bea import bea_fetch_info
from DBtransactions.loaders.cepea import cepea_fetch_info


dispatcher = {"FRED": fred_fetch_info.fetch_info,
              "IPEA": ipea_fetch_info.fetch_info, 
              "BLS": bls_fetch_info.fetch_info,
              "BIS": bis_fetch_info.fetch_info,
              "IBGE": ibge_fetch_info.fetch_info, 
              "BCB": bcb_fetch_info.fetch_info,
              "IMF": imf_fetch_info.fetch_info,
              "BCB_EXP": bcb_exp_fetch_info.fetch_info, 
              "ONS": ons_fetch_info.fetch_info, 
              "BEA": bea_fetch_info.fetch_info,
              "CEPEA": cepea_fetch_info.fetch_info }


def fetch_infos(source:Optional[str]=None,
                survey:Optional[str]=None,
                tickers:Optional[List[str]]=None)-> List[Series]:
    if source:
        if source == "IPEA":
            srs = dispatcher[source](ipea_fetch_info.tickers_ipea)
        elif source == "BLS":
            srs = dispatcher[source](bls_fetch_info.path_to_file)
        elif source == "BIS":
            srs = dispatcher[source](bis_fetch_info.source)
        elif source == "IBGE":
            srs = dispatcher[source](ibge_fetch_info.TABLES)
        elif source == "BCB":
            srs = dispatcher[source](bcb_fetch_info.pfile)
        elif source == "IMF":
            srs = dispatcher[source](list(imf_fetch_info.DSURVEYS))
        elif source == "ONS":
            srs = dispatcher[source]()
        elif source == "BEA":
            srs = dispatcher[source](reduce(lambda x, y: x + y, bea_fetch_info.TABLES.values()))
        elif source == "CEPEA":
            srs = dispatcher[source](cepea_fetch_info.INFO)
        else: # FRED
            srs = dispatcher[source](fred_fetch_info.INFO_FRED)
        return srs
    
    elif survey:
        if "BIS" in survey:
            srs = dispatcher["BIS"](bis_fetch_info.surveys[survey])
        elif "IBGE" in survey:
            srs = dispatcher["IBGE"]([tbl for tbl in ibge_fetch_info.TABLES if tbl['s'] == survey])
        elif "FRED" in survey:
            srs = dispatcher["FRED"]([info for info in fred_fetch_info.INFO_FRED if info[2] == survey])
        elif "IMF" in survey:
            srs = dispatcher["IMF"]([imf_fetch_info.DSURVEYS[survey]])
        elif "BCB" in survey:
            if "EXP" in survey:
                srs = [s for s in dispatcher["BCB_EXP"]() if s.survey_id == survey]
        elif "ONS" in survey:
            srs = dispatcher["ONS"]()
        elif "BEA" in survey:
            srs = dispatcher["ONS"](bea_fetch_info.TABLES[survey])
        elif "CEPEA" in survey:
            srs = dispatcher["CEPEA"](cepea_fetch_info.INFO)
            print(srs)
        else:
            pass
        return srs
    else:
        sources = set([tck.split(".")[0] for tck in tickers])
        dfs = []
        for s in sources: # precisa fazer asincrono
            aux = [tck for tck in tickers 
                      if tck.split(".")[0] == s]
            dfs = dfs + dispatcher[s](aux)
    return srs
