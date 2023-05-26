# imports from python's system
from concurrent.futures import ThreadPoolExecutor as executor
from typing import Optional, List
from datetime import datetime as dt
import time, pickle, os


# import from packages
import requests
import pandas as pd
import suds.client
import suds_requests

# import from app
from DBtransactions.DBtypes import Series

pfile = "./DBtransactions/loaders/bcb"

tcks_off = []

gestores = {"DSTAT/DIFIN/SUFIP": "BCB_FISCAL",
            "DSTAT/DIMOB/SUSIF": "BCB_MERCADO-ABERTO",
           "DSTAT/DIMOB/SUCRE": "BCB_CREDITO",
           "DSTAT/DIMOB/SUMON": "BCB_CREDITO",
           "DEMAB/DIGER/SUSIS": "BCB_CREDITO",
           "DEMAB/DIGER/SUEST": "BCB_CREDITO",
            "DEMAB/DICEL": "BCB_CREDITO", 
           "DEMAB/DIGER": "BCB_CREDITO", 
           "DEPEC/GERIR/DIREG/COSUD/NUCMG": "BCB_CREDITO", 
           "DESIG/GERIM/DIRIM/COLIQ-01": "BCB_ESTAB", 
           "DESIG/GERIM/DIRIM/CORIM": "BCB_ESTAB", 
           "DESIG/GESEG/DIMAC/COMOC": "BCB_ESTAB", 
           "DESIG/GESEG/DISEF/COMOR": "BCB_ESTAB", 
           "DESIG/GERIM/DIRIM/CORAC": "BCB_ESTAB", 
           "DESIG/GERIS/DIRIM/COPAR": "BCB_ESTAB", 
           "DESIG/GERIS/DIRIS/COPAR": "BCB_ESTAB", 
           "DSTAT/DIBAP/SUBAP": "BCB_SE", 
           "DEPIN/GEROP/DICAM": "BCB_SE", 
           "DSTAT/DIBAP/SUDEX": "BCB_SE", 
           "DEPIN/GEROP/DILIF": "BCB_SE", 
           "DEPEC/COACE": "BCB_ECON", 
           "DEPEC/GECON/COSUL": "BCB_ECON", 
           "DEPEC/COACE/COATI": "BCB_ECON", 
           "DEPEC/COACE/COPRE": "BCB_ECON", 
            "DEPEC/GECON/COSUD/NUCMG": "BCB_ECON",
            "DEPEC/GEPRE/DIPRE": "BCB_ECON", 
            "DEPEC/GEPRE/DIPRE": "BCB_ECON",
            'DEPEC/GEATI/COACE': "BCB_ECON",
            'DEPEC/GERIR/DIREG/COSUL': "BCB_ECON", #atividade regional
            "DEMAB/DICEL/SUREM": "BCB_MERCADO-ABERTO"
}



fonte_in =  ["MF-STN", 
             "Fipe", 
             # "Anfavea", 
             "Anbima", 
             # "ANP", 
             "BCB e FGV", 
             "Sisbacen PESP300", 
            #  "Eletrobras", 
            # "Fiergs", 
             "PTAX",
             "Cetip", 
             "FGC",
             "BCB-Desig", #ok
             "FGV", 
             "Copom", 
           # "MF-Cotepe", 
             "Sisbacen PTAX800", 
             "CNI", 
             "BCB-Depin", #ok
           # "Fiesp", 
             "ME", 
             "Dieese", 
             "Fenabrave", 
             "BCB-Depec", 
             "BCB-DSTAT", 
             "BCB-Derin", 
             "BCB-Demab", 
             "BCB",
             "BCB-Depep", 
             "Abraciclo"]

remove = {"tickers":
          ['3',
           '18', # Taxa média pós-fixada de depósitos a prazo (CDB/RDB) - Total
           '1175',
           '1177',
           '405', 
           '406', 
           '407', 
           '408', 
           '409',
           '25623',
           '25624',
           '3543',
           '3455',
              '3691',
              '3692',
              '3695',
              '3696',
              '3700',
              '3701',
              '3704',
              '3705',
           '12461', # andima
           '12462', 
           '12463', 
           '12464', 
           '12465', 
           '194',  #dieese
           "7348",
           '1344', 
           '1345', 
           '1346', 
           '1347', 
           '1348', 
           '1349', 
           '1350', 
           '1351', 
           '1352', 
           '1353', 
           '1354', 
           '1355', 
           '1356', 
           '1357', 
           '1358', 
           '1359', 
           '1360', 
           '1361', 
           '1362', 
           '1363', 
           '1364', 
           '1365', 
           '1366', 
           '1367', 
           '1368', 
           '1369', 
           '1341',
           '1370',
           '1389', # AnP
           '1390',
           '1391',
           '1392',
           '1393',
           '1394',
           '1395',
           '1396',
           '1397',
           '1398',
           '1399',
           '1400',
           '1401', #ANP
           '7343', 
           '7344', 
           '7345', 
           '7346', 
           '7347', 
           '7353', 
           '24246', 
           '24350', 
           '2256', # MF-STN
           '2257', 
           '2258', 
           '2259', 
           '2260', 
           '2261', 
           '2262', 
           '2263', 
           '2264', 
           '2265', 
           '2266', 
           '2267', 
           '2268', 
           '2269', 
           '2270', 
           '2271', 
           '2272', 
           '2273', 
           '2274', 
           '2275', 
           '2276', 
           '2277', 
           '2278', 
           '2279', 
           '2280', 
           '2281', 
           '2282', 
           '2283', 
           '2284', 
           '2285', 
           '2286', 
           '2287', 
           '2288', 
           '2289', 
           '2290', 
           '2291', 
           '2292', 
           '2293', 
           '2294', 
           '2295', 
           '2296', 
           '2297', 
           '2298', 
           '2299', 
           '2300',           
           '4353', 
           '4354', 
           '4355', 
           '4356', 
           '4357', 
           '4358', 
           '4359', 
           '4360', 
           '4361', 
           '4362', 
           '4363', 
           '4364', 
           '4365', 
           '4366', 
           '4367', 
           '4368', 
           '4369', 
           '4370', 
           '4371', 
           '4372', 
           '4373', 
           '4374', 
           '4375', 
           '4376', 
           '4377', 
           '4378', 
           '4379',
           '7544', 
           '7545', 
           '7546', 
           '7547', 
           '7548', 
           '7549', 
           '7550', 
           '7551', 
           '7552', 
           '7553', 
           '7554', 
           '7555', 
           '7556', 
           '7557', 
           '7558', 
           '7559', 
           '7560', 
           '7561', 
           '7562', 
           '7563', 
           '7564', 
           '7565', 
           '7566', 
           '7567', 
           '7568', 
           '7569', 
           '7570', 
           '7571', 
           '7572', 
           '7573', 
           '7574', 
           '7575', 
           '7576', 
           '7577', 
           '7578', 
           '7579', 
           '7580', 
           '7581', 
           '7582', 
           '7583', 
           '7584', 
           '7585', 
           '7586', 
           '7587', 
           '7588', 
           '7589', 
           '7590', 
           '7591', 
           '7592', 
           '7593', 
           '7594', 
           '7595', 
           '7596', 
           '7597', 
           '7598', 
           '7599', 
           '7600', 
           '7601', 
           '7602', 
           '7603', 
           '7604', 
           '7605', 
           '7606', 
           '7607', 
           '7608', 
           '7609', 
           '7610', 
           '7611', 
           '7612', 
           '7613'
           '24389', 
           '24390', 
           '24391', 
           '24392', 
           '24393', 
           '14001', 
           '21559',
           '27603',
           '28183', # Saldo de crédito ampliado ao setor não financeiro - Total
           '28184',  # 	Saldo de empréstimos e financiamentos ao setor não financeiro - total
           '28185',  # 	Saldo de empréstimos e financiamentos do SFN ao setor não financeirol
           '28204',    # Saldo de empréstimos e financiamentos a empresas e famílias - Total
           '28203',    # Saldo de crédito ampliado concedido a empresas e famílias - Total
           '28205',    # Saldo de empréstimos e financiamentos do SFN a empresas e famílias
           '28859',    # Saldo de empréstimos e financiamentos a famílias - Total
           '28858'    # Saldo de crédito ampliado concedido a famílias - Total
]}


def _cleasing(series: Optional[dict], freq:list) -> dict:
    """
    Keep series to be added in the db based on not been in series
    and have freq = []
    """
    if series is not None:
        if series["freq"] in freq:
            if series["final"].year == 2023:
                if series["fonte"] in fonte_in:
                    if str(series["number"]) not in remove['tickers']:
                        return series


def _process_info(resp: suds.sudsobject) -> dict:
    """
    process resp from suds response (last observation)
    and grabs information for the series
    """
    last = resp.ultimoValor
    return dict(fonte = str(resp.fonte),
                gestor = str(resp.gestorProprietario),
                freq = str(resp.periodicidadeSigla),
                nome = str(resp.nomeCompleto),
                number = int(resp.oid),
                final = dt(last.ano, last.mes, last.dia))


def _fetch_series(tickers: List[str]) -> List[dict]:
    """
    Fetches the meta information for ticker list and returns
    a list of dictionaries with the information
    """
    with requests.Session() as session:
        c = suds.client.Client(
            'https://www3.bcb.gov.br/sgspub/JSP/sgsgeral/FachadaWSSGS.wsdl',
            transport=suds_requests.RequestsTransport(session))
        
        def _fetch(tck):
            try:
                resp = c.service.getUltimoValorVO(tck)
                if resp is not None:
                    return _process_info(resp)
            except:
                tcks_off.append(tck)

        with executor() as e:
            ls = list(e.map(_fetch, tickers))
        return ls


def fetch_final_series(pfile: str) -> None:
    """
    Generates the final list of series to be used (inserted)
    in the database. Raw input (by side effect) comes from 
    file codigos.xlsx
    """
    tickers = pd.read_excel(pfile + "/codigos.xlsx", header=[0]).values.flatten()
    ls = _fetch_series(list(set(tickers)))
    net_series = [s for s in ls if _cleasing(s, ["D", "M"]) is not None]
    with open(pfile + "/series_bcb", "wb") as f:
        pickle.dump(net_series, f)


def fetch_info(fpath: str) -> List[Series]:
    with open(fpath + "/series_bcb", "rb") as fp:
        lsseries = pickle.load(fp)
    return [Series(**{
        "series_id": f"BCB.{ls['number']}",
        "description": ls['nome'],
        "survey_id": gestores[ls['gestor']],
        'frequency': {'D': 'DIARIA', 'M': "MENSAL"}[ls['freq']]}) for ls in lsseries]

