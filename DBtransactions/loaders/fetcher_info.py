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
from DBtransactions.loaders.cpb import cpb_fetch_info
from DBtransactions.loaders.nbsc import nbsc_fetch_info
from DBtransactions.loaders.caged import caged_fetch_info
from DBtransactions.loaders.nasdaq import nasdaq_fetch_info
from DBtransactions.loaders.cni import cni_fetch_info
from DBtransactions.loaders.anfavea import anfavea_fetch_info
from DBtransactions.loaders.stn import stn_fetch_info
from DBtransactions.loaders.ecb import ecb_fetch_info
from DBtransactions.loaders.anbima import anbima_fetch_info
#from DBtransactions.loaders.nucleos_ipca import nucleos_ipca_fetch_info

dispatcher = {
    "FRED": fred_fetch_info.fetch_info,
    "IPEA": ipea_fetch_info.fetch_info, 
    "BLS": bls_fetch_info.fetch_info,
    "BIS": bis_fetch_info.fetch_info,
    "IBGE": ibge_fetch_info.fetch_info, 
    "BCB": bcb_fetch_info.fetch_info,
    "IMF": imf_fetch_info.fetch_info,
    "BCB_EXP": bcb_exp_fetch_info.fetch_info, 
    "ONS": ons_fetch_info.fetch_info, 
    "BEA": bea_fetch_info.fetch_info,
    "CEPEA": cepea_fetch_info.fetch_info,
    "CPB": cpb_fetch_info.fetch_info,
    "NBSC": nbsc_fetch_info.fetch_info,
    "CAGED": caged_fetch_info.fetch_info,
    "NASDAQ": nasdaq_fetch_info.fetch_info,
    "CNI": cni_fetch_info.fetch_info,
    "ANFAVEA": anfavea_fetch_info.fetch_info,
    "STN": stn_fetch_info.fetch_info,
#    "NUCLEOS_IPCA": nucleos_ipca_fetch_info.fetch_info,
    "ECB": ecb_fetch_info.fetch_info,
    "ANBIMA": anbima_fetch_info.fetch_info
 }


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
        elif source == "CPB":
            srs = dispatcher[source](cpb_fetch_info.INFO)
        elif source == "NSBC":
            srs = dispatcher[source](nbsc_fetch_info.DATA)
        elif source == "CAGED":
            srs = dispatcher[source](caged_fetch_info.DATA)
        elif source == "NASDAQ":
            srs = dispatcher[source](caged_fetch_info.TICKERS)
        elif source == "CNI":
            srs = dispatcher[source](cni_fetch_info.DATA)
        elif source == "ANFAVEA":
            srs = dispatcher[source](anfavea_fetch_info.DATA)
        elif source == "STN":
            srs = dispatcher[source](stn_fetch_info.DATA)
        elif source == "ECB":
            srs = dispatcher[source](ecb_fetch_info.DATA)
        elif source == "ANBIMA":
            srs = dispatcher[source]()

        # elif source == "NUCLEOS_IPCA":
        #     srs = dispatcher[source](nucleos_ipca_fetch_info.SERIES)
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
            else:
                srs = [s for s in dispatcher["BCB"](bcb_fetch_info.pfile)] # need to refine to survey. Not its upload all source
        elif "ONS" in survey:
            srs = dispatcher["ONS"]()
        elif "BEA" in survey:
            srs = dispatcher["ONS"](bea_fetch_info.TABLES[survey])
        elif "CEPEA" in survey:
            srs = dispatcher["CEPEA"](cepea_fetch_info.INFO)
        elif "CPB" in survey:
            srs = dispatcher["CPB"](cpb_fetch_info.INFO)
        elif "BLS" in survey:
            srs = dispatcher["BLS"](survey)
        elif "NBSC" in survey:
            srs = dispatcher["NBSC"](survey)
        elif "CAGED" in survey:
            srs = dispatcher["CAGED"](caged_fetch_info.DATA)
        elif "NASDAQ" in survey:
            if "ML" in survey:
                srs = dispatcher["NASDAQ"](nasdaq_fetch_info.TICKERS_ML)
            else:
                srs = dispatcher["NASDAQ"](nasdaq_fetch_info.TICKERS_MULTPL)
        elif "CNI" in survey:
            srs = dispatcher["CNI"](cni_fetch_info.DATA)
        elif "ANFAVEA" in survey:
            srs = dispatcher["ANFAVEA"](anfavea_fetch_info.DATA)
        elif "STN" in survey:
            srs = dispatcher["STN"](stn_fetch_info.DATA)
        elif "ECB" in survey:
            srs = dispatcher["ECB"](ecb_fetch_info.DATA)
        elif "ANBIMA" in survey:
            srs = dispatcher["ANBIMA"]()
        # elif "IPCA" in survey:
        #     srs = dispatcher["NUCLEOS_IPCA"](s for s in nucleos_ipca_fetch_info.SERIES if s['survey_id'] == survey)
        else:
            pass
        return srs
    else:
        sources = set([tck.split(".")[0] for tck in tickers])
        srs = []
        for s in sources: # precisa fazer asincrono
            aux = [tck for tck in tickers 
                   if tck.split(".")[0] == s]
            srs = srs + dispatcher[s](aux)
    return srs
