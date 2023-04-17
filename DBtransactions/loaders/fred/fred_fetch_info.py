# import system
from concurrent.futures import ThreadPoolExecutor as executor
from typing import List, Tuple
import json, os


# import from packages
import requests

# import from app
from DBtransactions.DBtypes import Series

INFO_FRED: List[Tuple[str]] = [('FRED.UNRATE', 'TAXA DE DESEMPREGO DOS E.U.A.', 'FRED_ECON'),
             ('FRED.CFNAI', 'INDICE DE ATIVIDADE NACIONAL E.U.A. DO FED DE CHICAGO', 'FRED_ECON'),
             ('FRED.USRECD', 'INDICADOR DE RECESSAO DOS E.U.A. PUBLICADO PELA NBER', 'FRED_ECON'),
             ('FRED.PCEPI', 'INDICE DE PRECOS PCE', 'FRED_ECON'),
             ('FRED.PCEPILFE', 'NUCLEO DO PCE POR EXCLUSAO DE ALIMENTOS E ENERGIA', 'FRED_ECON'),
             ('FRED.T10YIE', 'INFLACAO IMPLICITA de 10 ANOS EXTRAIDA DOS TITULO SOBERANDO E.U.A.', 'FRED_FIN'),
             ('FRED.VIXCLS', 'VOLATILIDADE IMPLICITA DO S&P500', 'FRED_FIN'),
             ('FRED.CIVPART', 'TAXA DE PARTICIPAÇAO DA MAO-DE-OBRA DOS E.U.A.', 'FRED_ECON'),
             ('FRED.UMCSENT', 'SENTIMENTO DO CONSUMIDOR DOS E.U.A. DA UNIVERSIDADE DE MICHIGAN', 'FRED_ECON'),
             ('FRED.CPILFESL', 'NUCLEO DO INDICE DE PREÇOS AO CONSUMIDOR DOS E.U.A (CPI) POR EXCLUSAO DE ALIMENTOS E ENERGIA', 'FRED_ECON'),
             ('FRED.CPIAUCSL', 'INDICE DE PREÇOS AO CONSUMIDOR DOS E.U.A (CPI)', 'FRED_ECON'),
             ('FRED.PAYEMS', 'TOTAL DE EMPREGOS CRIADOS NOS E.U.A. EXCLUIDO O SETOR AGRĨCOLA (NONFARM PAYROLL)', 'FRED_ECON'),
             ('FRED.INDPRO', 'PRODUCAO INDUSTRIAL DOS E.U.A. COM AJUSTE SAZONAL', 'FRED_ECON'),
             ('FRED.ICSA', 'PEDIDOS INICIAIS DE SEGURO DESEMPREGO', 'FRED_ECON'),
             ('FRED.DGS10', 'TAXA DE JUROS DA TAXA DE 10 ANOS DO TÍTULO DO GOVERNO DOS E.U.A (TREASURY)', 'FRED_FIN'),
             ('FRED.EFFR', 'TAXA FED FUNDS EFETIVA', 'FRED_FIN'),
             ('FRED.VXEWZCLS', 'VOLATILIDADE IMPLICITA DO ETF EWZ DE ACÕES BRAZILEIRAS', 'FRED_FIN')]


def fetch_info(info) -> List[Series]:
    return [Series(** {'series_id': d[0], 
                       'description': d[1], 
                       'survey_id': d[2]}) for d in info]

