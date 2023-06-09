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
                "IPEA.ANFAVE12_QCAMINM12",
                "IPEA.ANFAVE12_QONIBUM12",
                "IPEA.ANFAVE12_QPASSAM12",
                "IPEA.ANFAVE12_QVEICLM12",
                "IPEA.ANFAVE12_QVETOTM12",
                "IPEA.ANFAVE12_LICCAMINM12",
                "IPEA.ANFAVE12_LICCAMINN12",
                "IPEA.ANFAVE12_LICCAMINTOT12",
                "IPEA.ANFAVE12_LICNCL12",
                "IPEA.ANFAVE12_LICNONI12",
                "IPEA.ANFAVE12_LICONIM12",
                "IPEA.ANFAVE12_LICONITOT12",
                "IPEA.ANFAVE12_LICPASSAMM12",
                "IPEA.ANFAVE12_LICPASSAMN12",
                "IPEA.ANFAVE12_LICPASSAMTOT12",
                "IPEA.ANFAVE12_LICVEM12",
                "IPEA.ANFAVE12_LICVETOT12",
                "IPEA.ANFAVE12_XCAMINM12",
                "IPEA.ANFAVE12_XONIBUM12",
                "IPEA.ANFAVE12_XPASSAM12",
                "IPEA.ANFAVE12_XVEICLM12",
                "IPEA.ANFAVE12_XVETOTM12",
                "IPEA.ANP12_PDGASN12",
                "IPEA.ANP12_PDPET12",
                "IPEA.ANP_CALCO",
                "IPEA.ANP_CODP",
                "IPEA.ANP12_CALCO12",
                "IPEA.ANP12_CDEPET12",
                "IPEA.ANP12_CGASOL12",
                "IPEA.ANP12_CGLP12",
                "IPEA.ANP12_CODP12",
                "IPEA.ANP12_COLCOM12",
                "IPEA.ANP12_COLDIE12",
                "IPEA.CEF12_FGTS12",
                "IPEA.SNIC12_V50KGSCC12",
                "IPEA.SNIC12_VKGSCC12",
                "IPEA.SNIC12_VTONSCC12",
                "IPEA.ELETRO_CEECOM",
                "IPEA.ELETRO_CEEIND",
                "IPEA.ELETRO_CEEOUT",
                "IPEA.ELETRO_CEERES",
                "IPEA.ELETRO_CEET",
                "IPEA.ELETRO_CEETCOM",
                "IPEA.ELETRO_CEETIND",
                "IPEA.ELETRO_CEETRES",
                "IPEA.ELETRO_CEETT",
                "IPEA.ELETRO12_CEECO12",
                "IPEA.ELETRO12_CEECOM12",
                "IPEA.ELETRO12_CEEIND12",
                "IPEA.ELETRO12_CEENE12",
                "IPEA.ELETRO12_CEENO12",
                "IPEA.ELETRO12_CEEOUT12",
                "IPEA.ELETRO12_CEERES12",
                "IPEA.ELETRO12_CEESE12",
                "IPEA.ELETRO12_CEESU12",
                "IPEA.ELETRO12_CEET12",
                "IPEA.FCESP12_IICA12",
                "IPEA.FCESP12_IIC12",
                "IPEA.FCESP12_IICF12",
                "IPEA.FENABRAVE12_VENDAUTO12",
                "IPEA.FENABRAVE12_VENDVETOT12",
                "IPEA.CE_CUTIND",
                "IPEA.CE12_CUTIND12",
                "IPEA.FIPE12_TXARJ12",
                "IPEA.FIPE12_TXASP12",
                "IPEA.FIPE12_VENBH12",
                "IPEA.FIPE12_VENBR12",
                "IPEA.FIPE12_VENDF12",
                "IPEA.FIPE12_VENFO12",
                "IPEA.FIPE12_VENRE12",
                "IPEA.FIPE12_VENRJ12",
                "IPEA.FIPE12_VENSA12",
                "IPEA.FIPE12_VENSP12",
                "IPEA.FNDE12_SALEDU12",
                "IPEA.FUNCEX_MDPBCD",
                "IPEA.FUNCEX_MDPBCND",
                "IPEA.FUNCEX_MDPBI",
                "IPEA.FUNCEX_MDPBK",
                "IPEA.FUNCEX_MDPCOMB",
                "IPEA.FUNCEX_MDPT",
                "IPEA.FUNCEX_MDQBCD",
                "IPEA.FUNCEX_MDQBCND",
                "IPEA.FUNCEX_MDQBI",
                "IPEA.FUNCEX_MDQBK",
                "IPEA.FUNCEX_MDQCOMB",
                "IPEA.FUNCEX_MDQT",
                "IPEA.FUNCEX12_MDPBCDGCE12",
                "IPEA.FUNCEX12_MDPBCNDGCE12",
                "IPEA.FUNCEX12_MDPBIGCE12",
                "IPEA.FUNCEX12_MDPBKGCE12",
                "IPEA.FUNCEX12_MDPCOMBGCE12",
                "IPEA.FUNCEX12_MDPT12",
                "IPEA.FUNCEX12_MDQBCDGCE12",
                "IPEA.FUNCEX12_MDQBCNDGCE12",
                "IPEA.FUNCEX12_MDQBIGCE12",
                "IPEA.FUNCEX12_MDQBKGCE12",
                "IPEA.FUNCEX12_MDQCOMBGCE12",
                "IPEA.FUNCEX12_MDQT12",
                "IPEA.FUNCEX12_MPAGP2N12",
                "IPEA.FUNCEX12_MPAL2N12",
                "IPEA.FUNCEX12_MPBEB2N12",
                "IPEA.FUNCEX12_MPCAL2N12",
                "IPEA.FUNCEX12_MPDIV2N12",
                "IPEA.FUNCEX12_MPEMM2N12",
                "IPEA.FUNCEX12_MPEMNM2N12",
                "IPEA.FUNCEX12_MPEPET2N12",
                "IPEA.FUNCEX12_MPFARM2N12",
                "IPEA.FUNCEX12_MPFUMO2N12",
                "IPEA.FUNCEX12_MPIMPG2N12",
                "IPEA.FUNCEX12_MPMAD2N12",
                "IPEA.FUNCEX12_MPMAQELET2N12",
                "IPEA.FUNCEX12_MPMAQEQU2N12",
                "IPEA.FUNCEX12_MPMAQINF2N12",
                "IPEA.FUNCEX12_MPMET2N12",
                "IPEA.FUNCEX12_MPMETBAS2N12",
                "IPEA.FUNCEX12_MPMNM2N12",
                "IPEA.FUNCEX12_MPMOV2N12",
                "IPEA.FUNCEX12_MPOUTTRANS2N12",
                "IPEA.FUNCEX12_MPPAP2N12",
                "IPEA.FUNCEX12_MPPES2N12",
                "IPEA.FUNCEX12_MPPETCOMB2N12",
                "IPEA.FUNCEX12_MPPLAS2N12",
                "IPEA.FUNCEX12_MPPRF2N12",
                "IPEA.FUNCEX12_MPQUIM2N12",
                "IPEA.FUNCEX12_MPTEXT2N12",
                "IPEA.FUNCEX12_MPVEIC2N12",
                "IPEA.FUNCEX12_MPVEST2N12",
                "IPEA.FUNCEX12_MQAGP2N12",
                "IPEA.FUNCEX12_MQAL2N12",
                "IPEA.FUNCEX12_MQBEB2N12",
                "IPEA.FUNCEX12_MQCAL2N12",
                "IPEA.FUNCEX12_MQDIV2N12",
                "IPEA.FUNCEX12_MQEMM2N12",
                "IPEA.FUNCEX12_MQEMNM2N12",
                "IPEA.FUNCEX12_MQEPET2N12",
                "IPEA.FUNCEX12_MQFARM2N12",
                "IPEA.FUNCEX12_MQFUMO2N12",
                "IPEA.FUNCEX12_MQIMQG2N12",
                "IPEA.FUNCEX12_MQMAD2N12",
                "IPEA.FUNCEX12_MQMAQELET2N12",
                "IPEA.FUNCEX12_MQMAQEQU2N12",
                "IPEA.FUNCEX12_MQMAQINF2N12",
                "IPEA.FUNCEX12_MQMET2N12",
                "IPEA.FUNCEX12_MQMETBAS2N12",
                "IPEA.FUNCEX12_MQMNM2N12",
                "IPEA.FUNCEX12_MQMOV2N12",
                "IPEA.FUNCEX12_MQOUTTRANS2N12",
                "IPEA.FUNCEX12_MQPAP2N12",
                "IPEA.FUNCEX12_MQPES2N12",
                "IPEA.FUNCEX12_MQPETCOMB2N12",
                "IPEA.FUNCEX12_MQPLAS2N12",
                "IPEA.FUNCEX12_MQPRF2N12",
                "IPEA.FUNCEX12_MQQUIM2N12",
                "IPEA.FUNCEX12_MQTEXT2N12",
                "IPEA.FUNCEX12_MQVEIC2N12",
                "IPEA.FUNCEX12_TTR12",
                "IPEA.FUNCEX12_XPAGP2N12",
                "IPEA.FUNCEX12_XPAL2N12",
                "IPEA.FUNCEX12_XPB12",
                "IPEA.FUNCEX12_XPBCDGCE12",
                "IPEA.FUNCEX12_XPBCNDGCE12",
                "IPEA.FUNCEX12_XPBEB2N12",
                "IPEA.FUNCEX12_XPBIGCE12",
                "IPEA.FUNCEX12_XPBKGCE12",
                "IPEA.FUNCEX12_XPCAL2N12",
                "IPEA.FUNCEX12_XPCOMBGCE12",
                "IPEA.FUNCEX12_XPDIV2N12",
                "IPEA.FUNCEX12_XPEMM2N12",
                "IPEA.FUNCEX12_XPEMNM2N12",
                "IPEA.FUNCEX12_XPEPET2N12",
                "IPEA.FUNCEX12_XPFARM2N12",
                "IPEA.FUNCEX12_XPFUMO2N12",
                "IPEA.FUNCEX12_XPIXPG2N12",
                "IPEA.FUNCEX12_XPM12",
                "IPEA.FUNCEX12_XPMAD2N12",
                "IPEA.FUNCEX12_XPMAQELET2N12",
                "IPEA.FUNCEX12_XPMAQEQU2N12",
                "IPEA.FUNCEX12_XPMAQINF2N12",
                "IPEA.FUNCEX12_XPMET2N12",
                "IPEA.FUNCEX12_XPMETBAS2N12",
                "IPEA.FUNCEX12_XPMNM2N12",
                "IPEA.FUNCEX12_XPMOV2N12",
                "IPEA.FUNCEX12_XPOUTTRANS2N12",
                "IPEA.FUNCEX12_XPPAP2N12",
                "IPEA.FUNCEX12_XPPES2N12",
                "IPEA.FUNCEX12_XPPETCOMB2N12",
                "IPEA.FUNCEX12_XPPLAS2N12",
                "IPEA.FUNCEX12_XPPRF2N12",
                "IPEA.FUNCEX12_XPQUIM2N12",
                "IPEA.FUNCEX12_XPS12",
                "IPEA.FUNCEX12_XPT12",
                "IPEA.FUNCEX12_XPTEXT2N12",
                "IPEA.FUNCEX12_XPVEIC2N12",
                "IPEA.FUNCEX12_XPVEST2N12",
                "IPEA.FUNCEX12_XQAGP2N12",
                "IPEA.FUNCEX12_XQAL2N12",
                "IPEA.FUNCEX12_XQB12",
                "IPEA.FUNCEX12_XQBCDGCE12",
                "IPEA.FUNCEX12_XQBCNDGCE12",
                "IPEA.FUNCEX12_XQBEB2N12",
                "IPEA.FUNCEX12_XQBIGCE12",
                "IPEA.FUNCEX12_XQBKGCE12",
                "IPEA.FUNCEX12_XQCAL2N12",
                "IPEA.FUNCEX12_XQCOMBGCE12",
                "IPEA.FUNCEX12_XQDIV2N12",
                "IPEA.FUNCEX12_XQEMM2N12",
                "IPEA.FUNCEX12_XQEMNM2N12",
                "IPEA.FUNCEX12_XQEPET2N12",
                "IPEA.FUNCEX12_XQFARM2N12",
                "IPEA.FUNCEX12_XQFUMO2N12",
                "IPEA.FUNCEX12_XQIXQG2N12",
                "IPEA.FUNCEX12_XQM12",
                "IPEA.FUNCEX12_XQMAD2N12",
                "IPEA.FUNCEX12_XQMAQELET2N12",
                "IPEA.FUNCEX12_XQMAQEQU2N12",
                "IPEA.FUNCEX12_XQMAQINF2N12",
                "IPEA.FUNCEX12_XQMET2N12",
                "IPEA.FUNCEX12_XQMETBAS2N12",
                "IPEA.FUNCEX12_XQMNM2N12",
                "IPEA.FUNCEX12_XQMOV2N12",
                "IPEA.FUNCEX12_XQOUTTRANS2N12",
                "IPEA.FUNCEX12_XQPAP2N12",
                "IPEA.FUNCEX12_XQPES2N12",
                "IPEA.FUNCEX12_XQPETCOMB2N12",
                "IPEA.FUNCEX12_XQPLAS2N12",
                "IPEA.FUNCEX12_XQPRF2N12",
                "IPEA.FUNCEX12_XQQUIM2N12",
                "IPEA.FUNCEX12_XQS12",
                "IPEA.FUNCEX12_XQT12",
                "IPEA.FUNCEX12_XQTEXT2N12",
                "IPEA.FUNCEX12_XQVEIC2N12",
                "IPEA.FUNCEX12_XQVEST2N12",
                "IPEA.FUNCEX12_XR12",
                "IPEA.FUNCEX12_XVOUTTRANS2N12",
                "IPEA.FUNCEX12_XVPAP2N12",
                "IPEA.IBSIE_QSCAB",
                "IPEA.IBSIE_QSCFG",
                "IPEA.IBSIE_QSCL",
                "IPEA.IBSIE12_QSCAB12",
                "IPEA.IBSIE12_QSCFG12",
                "IPEA.IBSIE12_QSCL12",
                "IPEA.GAC12_FBKFCAMI12",
                "IPEA.GAC12_FBKFCAMIDESSAZ12",
                "IPEA.GAC12_INDFBCF12",
                "IPEA.GAC12_INDFBCFCC12",
                "IPEA.GAC12_INDFBCFCCDESSAZ12",
                "IPEA.GAC12_INDFBCFDESSAZ12",
                "IPEA.DIMAC_INF1",
                "IPEA.DIMAC_INF2",
                "IPEA.DIMAC_INF3",
                "IPEA.DIMAC_INF4",
                "IPEA.DIMAC_INF5",
                "IPEA.DIMAC_INF6",
                "IPEA.PAN4_FBKFI90G4",
                "IPEA.PAN4_FBKFPIBV4",
                "IPEA.PAN4_TCERXTINPC4",
                "IPEA.DIMAC_DCONSTNRESDE",
                "IPEA.DIMAC_DCONSTNRESINF",
                "IPEA.DIMAC_DCONSTRES",
                "IPEA.DIMAC_DCONSTTOT",
                "IPEA.DIMAC_DEFBRUTINF",
                "IPEA.DIMAC_DMAQE",
                "IPEA.DIMAC_DOUT",
                "IPEA.DIMAC_DTOT",
                "IPEA.DIMAC_ECFLIQCONSTNRESDE",
                "IPEA.DIMAC_ECFLIQCONSTNRESINF",
                "IPEA.DIMAC_ECFLIQCONSTRES",
                "IPEA.DIMAC_ECFLIQCONSTTOT",
                "IPEA.DIMAC_ECFLIQMAQE",
                "IPEA.DIMAC_ECFLIQOUT",
                "IPEA.DIMAC_ECFLIQTOT",
                "IPEA.DIMAC_ECFLIQTOT12",
                "IPEA.DIMAC_ECFLIQTOT4",
                "IPEA.DIMAC_ILIQTOT112",
                "IPEA.DIMAC_TDICONSTNRESDE",
                "IPEA.DIMAC_TDICONSTNRESINF",
                "IPEA.DIMAC_TDICONSTRES",
                "IPEA.DIMAC_TDICONSTTOT",
                "IPEA.DIMAC_TDIMAQE",
                "IPEA.DIMAC_TDIOUT",
                "IPEA.DIMAC_TDITOT",
                "IPEA.JPM366_EMBI366",
                "IPEA.SECEX12_XGASOL12",
                "IPEA.SECEX12_XGASOLKG12",
                "IPEA.MME_CAPINSTEE",
                "IPEA.MME_HIDRAU",
                "IPEA.MME_NUCLEAR",
                "IPEA.MME_PENREC",
                "IPEA.MME_PENRECM",
                "IPEA.MME_PENREGN",
                "IPEA.MME_PENREP",
                "IPEA.MME_PENRETOT",
                "IPEA.MME_PENREU",
                "IPEA.MME_PERECA",
                "IPEA.MME_PEREHIDR",
                "IPEA.MME_PEREL",
                "IPEA.MME_PEREOUT",
                "IPEA.MME_PERETOT",
                "IPEA.MME_PETOT",
                "IPEA.MME_TERMICA",
                "IPEA.MME_CEAGRO",
                "IPEA.MME_CECOM",
                "IPEA.MME_CEENE",
                "IPEA.MME_CEIND",
                "IPEA.MME_CENE",
                "IPEA.MME_CENID",
                "IPEA.MME_CEPUBL",
                "IPEA.MME_CERES",
                "IPEA.MME_CETOT",
                "IPEA.MME_CETRANS",
                "IPEA.ONS12_CONV12",
                "IPEA.ONS12_HIDR12",
                "IPEA.ONS12_NUCL12",
                "IPEA.DERAL12_ATARP12",
                "IPEA.DERAL12_ATARPO12",
                "IPEA.DERAL12_ATBCAD12",
                "IPEA.DERAL12_ATBCAT12",
                "IPEA.DERAL12_ATBSUI12",
                "IPEA.DERAL12_ATCAM12",
                "IPEA.DERAL12_ATFEC12",
                "IPEA.DERAL12_ATFECU12",
                "IPEA.DERAL12_ATFEP12",
                "IPEA.DERAL12_ATFMAC12",
                "IPEA.DERAL12_ATFMAT12",
                "IPEA.DERAL12_ATFMP12",
                "IPEA.DERAL12_ATFRC12",
                "IPEA.DERAL12_ATFRM12",
                "IPEA.DERAL12_ATFRR12",
                "IPEA.DERAL12_ATFSO12",
                "IPEA.DERAL12_ATFTRC12",
                "IPEA.DERAL12_ATFTRE12",
                "IPEA.DERAL12_ATFUA12",
                "IPEA.DERAL12_ATMAE12",
                "IPEA.DERAL12_ATMC12",
                "IPEA.DERAL12_ATOLB12",
                "IPEA.DERAL12_ATOLR12",
                "IPEA.DERAL12_ATOVE12",
                "IPEA.DERAL12_ATOVG12",
                "IPEA.DERAL12_ATOVM12",
                "IPEA.DERAL12_ATPIC12",
                "IPEA.DERAL12_ATPIP12",
                "IPEA.DERAL12_ATQMF12",
                "IPEA.DERAL12_ATQMZ12",
                "IPEA.DERAL12_ATQPA12",
                "IPEA.DERAL12_ATQPR12",
                "IPEA.DERAL12_ATSCAR12",
                "IPEA.DERAL12_ATSULO12",
                "IPEA.DERAL12_ATSUPA12",
                "IPEA.DERAL12_ATSUPE12",
                "IPEA.DERAL12_ATTRG12",
                "IPEA.DERAL12_PRARIR12",
                "IPEA.DERAL12_PRARSE12",
                "IPEA.DERAL12_PRBGO12",
                "IPEA.DERAL12_PRBMA12",
                "IPEA.DERAL12_PRCAN12",
                "IPEA.DERAL12_PRCCO12",
                "IPEA.DERAL12_PRFEC12",
                "IPEA.DERAL12_PRFEP12",
                "IPEA.DERAL12_PRFRV12",
                "IPEA.DERAL12_PRLECO12",
                "IPEA.DERAL12_PRMAN12",
                "IPEA.DERAL12_PRMI12",
                "IPEA.DERAL12_PROVG12",
                "IPEA.DERAL12_PROVM12",
                "IPEA.DERAL12_PRSO12",
                "IPEA.DERAL12_PRSUC12",
                "IPEA.DERAL12_PRTRG12",
                "IPEA.SNIC12_QSCC12",
                "IPEA.SNIC12_QCASCC12",
                "IPEA.SNIC12_QDSCC12"]
    

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


