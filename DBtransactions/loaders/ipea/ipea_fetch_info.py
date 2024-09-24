#############################################
# Data from http://www.ipeadata.gov.br/api/
# Estudar a possibilidade de incluir frequencia
# através da api
#############################################

# import from system
from concurrent.futures import ThreadPoolExecutor as executor
from typing import List, Dict, Tuple

#import from packages
import requests
import pandas as pd

#import from app
from DBtransactions.DBtypes import Series


__all__ = ["tickers_ipea", "fetch_info"]

#app imports
# from DB.transactions import add_series

URL = "http://www.ipeadata.gov.br/api/odata4/"

# series to be fetched from api
tickers_ipea = ["IPEA.ABPO12_PAPEL12",
                "IPEA.ANDA_PFERTILIZ",
                "IPEA.ANDA12_PFERTILIZ12",
                "IPEA.ANDA_VFERTILIZ",
                "IPEA.ANDA12_VFERTILIZ12",
                "IPEA.ANDA_MFERTILIZ",
                "IPEA.ANDA12_MFERTILIZ12",
                "IPEA.ANFAVE_QVEICL",
                "IPEA.ANFAVE12_LICVEN12",
                # "IPEA.ANFAVE12_QCAMINM12",
                # "IPEA.ANFAVE12_QONIBUM12",
                # "IPEA.ANFAVE12_QPASSAM12",
                # "IPEA.ANFAVE12_QVEICLM12",
                # "IPEA.ANFAVE12_QVETOTM12",
                # "IPEA.ANFAVE12_LICCAMINM12",
                # "IPEA.ANFAVE12_LICCAMINN12",
                # "IPEA.ANFAVE12_LICCAMINTOT12",
                # "IPEA.ANFAVE12_LICNCL12",
                # "IPEA.ANFAVE12_LICNONI12",
                # "IPEA.ANFAVE12_LICONIM12",
                # "IPEA.ANFAVE12_LICONITOT12",
                # "IPEA.ANFAVE12_LICPASSAMM12",
                # "IPEA.ANFAVE12_LICPASSAMN12",
                # "IPEA.ANFAVE12_LICPASSAMTOT12",
                # "IPEA.ANFAVE12_XCAMINM12",
                # "IPEA.ANFAVE12_XONIBUM12",
                # "IPEA.ANFAVE12_XPASSAM12",
                # "IPEA.ANFAVE12_XVEICLM12",
                # "IPEA.ANFAVE12_XVETOTM12",
                "IPEA.ANP12_PDGASN12",
                "IPEA.ANP12_PDPET12",
                "IPEA.ANP12_CALCO12",
                "IPEA.ANP12_CDEPET12",
                "IPEA.ANP12_CGASOL12",
                "IPEA.ANP12_COLDIE12",
                "IPEA.CEF12_FGTS12",
                "IPEA.FENABRAVE12_VENDAUTO12",
                "IPEA.FENABRAVE12_VENDVETOT12",
                "IPEA.CE12_CUTIND12",
                'IPEA.FIPE12_VENBR12',
                'IPEA.FIPE12_IPCFIPE12',
                "IPEA.FUNCEX12_XVAGP2N12",
                "IPEA.FUNCEX12_XPAGP2N12",
                "IPEA.FUNCEX12_XQAGP2N12",
                "IPEA.FUNCEX12_XQBEB2N12",
                "IPEA.FUNCEX12_XQBKGCE12",
                "IPEA.FUNCEX12_XQPAP2N12",
                "IPEA.FUNCEX12_XQEPET2N12",
                "IPEA.FUNCEX12_XPT12",
                "iPEA.FUNCEX12_XQFARM2N12",
                "IPEA.FUNCEX12_XQT12",
                "IPEA.FUNCEX12_MVAGP2N12",
                "IPEA.FUNCEX12_MQAGP2N12",
                "IPEA.FUNCEX12_MQVEST2N12",
                "IPEA.FUNCEX12_MQEPET2N12",
                "IPEA.FUNCEX12_MDPT12",
                "IPEA.FUNCEX12_MQFARM2N12",
                "IPEA.FUNCEX12_MDQT12",
                "IPEA.FUNCEX12_TTR12",
                "IPEA.IBSIE12_QSCAB12",
                "IPEA.IBSIE12_QSCFG12",
                "IPEA.IBSIE12_QSCL12",
                "IPEA.GAC12_FBKFCAMI12",
                "IPEA.GAC12_FBKFCAMIDESSAZ12",
                "IPEA.GAC12_INDFBCF12",
                "IPEA.GAC12_INDFBCFCC12",
                "IPEA.GAC12_INDFBCFCCDESSAZ12",
                "IPEA.GAC12_INDFBCFDESSAZ12",
                "IPEA.JPM366_EMBI366",
                "IPEA.ONS12_CONV12",
                "IPEA.ONS12_HIDR12",
                "IPEA.CNC12_IEEC12",
                "IPEA.CNC12_ICEC12",
                "IPEA.CNC12_ICF12", 
                "IPEA.CNC12_PEICT12"]

def build_url(tck:str) -> str:
    """
    builds the url to fetch the metadados of a series 
    from ipeadatas webpage. 
    """
    return URL + f"Metadados('{tck}')"
    

def process(resp:requests.models.Response) ->  Series:
    """
    handles a response of a request to the ipea's ipea for
    metadados for a particular seires.
    """
    if resp.ok:
        js = resp.json()['value'][0]
        d = dict([(k, js[k]) for k in ('SERCODIGO', 'SERNOME', 'FNTSIGLA', "PERNOME")])
        d["survey_id"] = 'IPEA_FIN' if d['SERCODIGO'] == 'JPM366_EMBI366' else 'IPEA_ECON'
        d["series_id"] = f"IPEA.{d['SERCODIGO']}" 
        d["description"] = f"{d['SERNOME']}" + f", { d['PERNOME'] if d['PERNOME'].upper() else ''}"
        d["description"] = f"{d['description']}" + f", { d['FNTSIGLA'] if d['FNTSIGLA'].upper() else ''}"
        d["frequency"] = d["PERNOME"].upper()
        d['last_update'] = ''
        d.pop('SERCODIGO')
        d.pop('SERNOME')
        d.pop('FNTSIGLA')
        d.pop('PERNOME')
        return Series(**d)
    else:
        print(f"Could not reach {resp.url}")


def fetch_info(tickers: List[str]) -> List[List[Series]]:
    """
    takes a list of tickers, 
    fetches meta information on them from
    IPEA api and then inserts that information in the datebase
    """
    urls =[build_url(tck.split(".")[1]) for tck in tickers]
    with requests.session() as session:
        with executor() as e:
            srs = list(e.map(lambda u: process(session.get(u)), urls))
    return srs
