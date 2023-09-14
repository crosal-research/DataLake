# import system
from concurrent.futures import ThreadPoolExecutor as executor
from typing import List, Tuple
import json, os


# import from packages
import requests

# import from app
from DBtransactions.DBtypes import Series

INFO_FRED: List[Tuple[str]] = [
    ('FRED.UNRATE', 'TAXA DE DESEMPREGO DOS E.U.A.', 'FRED_ECON', 'MENSAL'),
    ('FRED.CFNAI', 'INDICE DE ATIVIDADE NACIONAL E.U.A. DO FED DE CHICAGO', 'FRED_ECON', 'MENSAL'),
    ('FRED.USRECD', 'INDICADOR DE RECESSAO DOS E.U.A. PUBLICADO PELA NBER', 'FRED_ECON', 'MENSAL'),
    ('FRED.PCEPI', 'INDICE DE PRECOS PCE', 'FRED_ECON', 'MENSAl'),
    ('FRED.PCEPILFE', 'NUCLEO DO PCE POR EXCLUSAO DE ALIMENTOS E ENERGIA', 'FRED_ECON', 'MENSAL'),
    ('FRED.T10YIE', 'INFLACAO IMPLICITA de 10 ANOS EXTRAIDA DOS TITULO SOBERANDO E.U.A.', 'FRED_FIN', 'DIARIA'),
    ('FRED.VIXCLS', 'VOLATILIDADE IMPLICITA DO S&P500', 'FRED_FIN', 'DIARIA'),
    ('FRED.CIVPART', 'TAXA DE PARTICIPAÇAO DA MAO-DE-OBRA DOS E.U.A.', 'FRED_ECON', "MENSAL"),
    ('FRED.UMCSENT', 'SENTIMENTO DO CONSUMIDOR DOS E.U.A. DA UNIVERSIDADE DE MICHIGAN', 'FRED_ECON', 'MENSAL'),
    ('FRED.CPILFESL', 'NUCLEO DO INDICE DE PREÇOS AO CONSUMIDOR DOS E.U.A (CPI) POR EXCLUSAO DE ALIMENTOS E ENERGIA', 'FRED_ECON', 'MENSAL'),
    ('FRED.CPIAUCSL', 'INDICE DE PREÇOS AO CONSUMIDOR DOS E.U.A (CPI)', 'FRED_ECON', 'MENSAL'),
    ('FRED.PAYEMS', 'TOTAL DE EMPREGOS CRIADOS NOS E.U.A. EXCLUIDO O SETOR AGRĨCOLA (NONFARM PAYROLL)', 'FRED_ECON', 'MENSAL'),
    ('FRED.INDPRO', 'PRODUCAO INDUSTRIAL DOS E.U.A. COM AJUSTE SAZONAL', 'FRED_ECON', 'MENSAL'),
    ('FRED.ICSA', 'PEDIDOS INICIAIS DE SEGURO DESEMPREGO', 'FRED_ECON', "MENSAL"),
    ('FRED.DGS10', 'TAXA DE JUROS DA TAXA DE 10 ANOS DO TÍTULO DO GOVERNO DOS E.U.A (TREASURY)', 'FRED_FIN', 'DIARIA'),
    ('FRED.EFFR', 'TAXA FED FUNDS EFETIVA', 'FRED_FIN', "DIARIA"),
    ('FRED.VXEWZCLS', 'VOLATILIDADE IMPLICITA DO ETF EWZ DE ACÕES BRASILEIRAS', 'FRED_FIN', 'DIARIA'),
    ('FRED.UMCSENT', 'SENTIMENTO DO CONSUMIDOR DA UNIVERSIDADE DE MICHIGAN, E.U.A.', 'FRED_ECON', 'MENSAL'),
    ('FRED.MICH', ' EXPECTATIVA DE INFLACAO DA UNIVERSIDADE DE MICHIGAN, E.U.A.', 'FRED_ECON', 'MENSAL'), 
    ('FRED.GFDEGDQ188S', 'RELACAO DIVIDA PUBLICA FEDERAL SOBRE PIB, E.U.A.', 'FRED_ECON', 'TRIMESTRAL'), 
    ('FRED.DCOILBRENTEU', 'PREÇO DO BARRIL DO PETROLEO EXTRAIDO NO MAR NO NORTE (BRENT)', 'FRED_FIN', 'DIARIA')]


def fetch_info(info) -> List[Series]:
    return [Series(**{'series_id': d[0], 
                      'description': d[1], 
                      'survey_id': d[2],
                      'last_update': None,
                      'frequency': d[3]}) for d in info]

