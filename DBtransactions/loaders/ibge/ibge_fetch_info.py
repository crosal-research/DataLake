############################################################
# Build the series info for IBGE's data from its api
# 
############################################################
# import from system
from concurrent.futures import ThreadPoolExecutor as executor
from typing import List, Dict, Tuple
from functools import reduce

# import from packages
import requests, urllib3
from urllib3.util.ssl_ import create_urllib3_context

# import from app
from DBtransactions.DBtypes import Series


# IBGE's tables with relevant series
TABLES = [
    # Producao Industrial
    {'t':'8887', 'v': 12606, 'c543':'all', 's': "IBGE_PIM"},   # Produção Industrial categorias
    {'t':'8887', 'v': 12607, 'c543':'all', 's': "IBGE_PIM"},   # Produção Industrial categorias, sa
    {'t':'8886', 'v': 12606,               's': "IBGE_PIM"},   # Produção de insumos da const. civil.
    {'t':'8888', 'v': 12606, 'c544': 'all', 's': "IBGE_PIM"},  # Produção Industrial por secoes e atividades
    {'t':'8888', 'v': 12607, 'c544': 'all', 's': "IBGE_PIM"},  # Produção Industrial por secoes e atividades,sa
    # Varejo                                                           
    {'t':'8880', 'v': 7169, 'c11046': 56734, 's': "IBGE_PMC"}, # Comercio varejista
    {'t':'8880', 'v': 7170, 'c11046': 56734, 's': "IBGE_PMC"}, # comercio varejista sa 
    {'t':'8881', 'v': 7169, 'c11046': 56736, 's': "IBGE_PMC"}, # comercio varejista ampliado
    {'t':'8881', 'v': 7170, 'c11046': 56736, 's': "IBGE_PMC"}, # comercio varejista ambiliado sa 
    {'t':'8883', 'v': 7169, 'c11046': 56736, 'c85': 'all', 's': "IBGE_PMC"}, # comercio varejista ampliado por atividades
    {'t':'8883', 'v': 7170, 'c11046': 56736, 'c85': 'all', 's': "IBGE_PMC"}, # comercio varejista ampliado por atividades sa
    {'t':'8884', 'v': 7169, 'c11046': 56738, 's': "IBGE_PMC"}, # motos, auto e peças
    {'t':'8884', 'v': 7170, 'c11046': 56738, 's': "IBGE_PMC"}, # motos, atuo e peças  sa
    # servicos
    {'t':'8688', 'v': 7167, 'c11046': 56726, 'c12355': 'all', 's': "IBGE_PMS"}, # volume de serviços  
    {'t':'8688', 'v': 7168, 'c11046': 56726, 'c12355': 'all', 's': "IBGE_PMS"}, # volume de serviços  
    # contas nacionais
    {'t':'1620', 'v': 583, 'c11255': 'all','s': "IBGE_CN"}, # PIB volume setores
    {'t':'1621', 'v': 584, 'c11255': 'all','s': "IBGE_CN"}, # PIB volume setores sa
    {'t':'1846', 'v': 585, 'c11255': 'all','s': "IBGE_CN"}, # PIB precos correntes
    # mercado de trabalho
    {'t':'6022', 'v': 606                  ,'s': "IBGE_PNAD"}, # Populacao
    {'t':'6318', 'v': 1641, 'c629':   'all','s': "IBGE_PNAD"}, # Forca de trabalho e status laboral
    {'t':'6320', 'v': 4090, 'c11913': 'all','s': "IBGE_PNAD"}, # Por tipo de vinculo empregaticio
    {'t':'6387', 'v': 5935                ,'s': "IBGE_PNAD"},   # Rendimento médio
    {'t':'6388', 'v': 5934                ,'s': "IBGE_PNAD"},   # Rendimento real médio
    {'t':'6389', 'v': 5932, 'c11913': 'all','s': "IBGE_PNAD"},   # Rendimento real médio por tipo de vínculo
    {'t':'6389', 'v': 5932, 'c11913': 'all','s': "IBGE_PNAD"},   # Rendimento real médio por tipo de vínculo
    {'t':'6390', 'v': 5933                 ,'s': "IBGE_PNAD"},   # Rendimento real médio de todos os trabalhadores
    {'t':'6390', 'v': 5929                 ,'s': "IBGE_PNAD"},   # Rendimento nominal médio de todos os trabalhadores
    {'t':'6391', 'v': 5932                 ,'s': "IBGE_PNAD"},   # Rendimento real médio do trabalho principal
    {'t':'6392', 'v': 6293                 ,'s': "IBGE_PNAD"},   # massa real de todos os trabalhdores
    {'t':'6392', 'v': 6288                 ,'s': "IBGE_PNAD"},   # mass moninal de todos os trabalhdores
    {'t':'6393', 'v': 6295                 ,'s': "IBGE_PNAD"},   # massa real de todos os trabalhdores effetiva
    {'t':'6393', 'v': 6291                 ,'s': "IBGE_PNAD"},   # massa nominal de todos os trabalhdores effetiva
    {'t':'6438', 'v': 1641,'c604': 'all'   ,'s': "IBGE_PNAD"},   # força de trabalho por tipo de subutilizacao
    {'t':'6439', 'v': 4114                 ,'s': "IBGE_PNAD"},   # força de trabalho sub-utilizada por horas trabalhadas
    {'t':'6440', 'v': 4116                 ,'s': "IBGE_PNAD"},   # força de trabalho desocupda e potencial
    {'t':'6441', 'v': 4118                 ,'s': "IBGE_PNAD"},   # força de trabalho desocupda e potencial (%)
    # ipca
    {'t':'7060', 'v': 63, 'c315': 'all'    ,'s': "IBGE_IPCA"},   # Indice nacional de precos amplo, variacao (%): 
    {'t':'7060', 'v': 66, 'c315': 'all'    ,'s': "IBGE_IPCA"},   # Indice nacional de precos amplo, peso (%):
    {'t':'7062', 'v': 355, 'c315': 'all'    ,'s': "IBGE_IPCA15"},# Indice nacional de precos amplo 15, variacao (%): 
    {'t':'7062', 'v': 357, 'c315': 'all'    ,'s': "IBGE_IPCA15"} # Indice nacional de precos amplo 15, pesos (%):
]     

URL = "https://apisidra.ibge.gov.br/values/"


def _form_params(d:dict) -> str:
    """
    from the params of the url from line in TABLES
    """
    return "/".join(["/".join([str(k), str(d[k])]) 
                     for k in d if k != 's'])

def _build_url(input:dict) -> str:
    """
    Build the relevante url    
    """
    params = _form_params(input)
    return URL + params + "/d/2/n1/1"


# def _aux_fetch_info(tbl: dict, session: requests.sessions.Session) -> List[Series]:
def _aux_fetch_info(tbl: dict, pool: urllib3.PoolManager) -> List[Series]:
    """
    Fetch info from a IBGE's table and build tickers, info, etc 
    into a series
    """
    url = _build_url(tbl)
    resp = pool.request("GET", url, timeout=4.0, retries=10)
    ls = resp.json()
    tck = ((resp.url).split("t/")[1]).split("/d")[0]
    survey = tbl['s'] 
    ch = 'D3C' if len(tbl) > 4 else 'D2C'
    freq = ""
    if len(tbl) > 4:
        freq = ls[0]['D5C']
    elif len(tbl) == 4:
        freq  = ls[0]['D4C']
    else:
        freq = ls[0]['D3C']

    def _freq(dat: str) -> str:
        """
        Helper para 
        """
        if 'Mês' in dat:
            return "MENSAL"
        elif "Trimestre" in dat:
            return "TRIMESTRAL"
        return "ANUAL"
        
    srs = []
    for l in ls[1:]:
        cn = f"{l['D2N']}, {l['D1N']}, Brasil" if ch == 'DC2' else f"{l['D2N']},{l['D3N']} {l['D1N']}, Brasil"
        srs.append(Series(**{'series_id': f"IBGE.{tck.replace('all', l[ch])}" if 'all' in tck else f"IBGE.{tck}",
                             'description': cn, 
                             'survey_id': survey,
                             'last_update': None,
                             'frequency': 'TRIMESTRAL' if survey == "IBGE_CN" else "MENSAL"}))
    return srs


def fetch_info(tbls: List[dict]) -> List[Tuple[Series]]:
    """
    Fetch info from a IBGE's table and build tickers, info, etc 
    into a series
    """
    # session = requests.session()
    # with requests.session() as session:
    # https = urllib3.HTTPSConnectionPool("apisidra.ibge.gov.br", maxsize=100)

    ctx = create_urllib3_context()
    ctx.load_default_certs()
    ctx.options |= 0x4  # ssl.OP_LEGACY_SERVER_CONNECT
    with urllib3.PoolManager(ssl_context=ctx) as https:
        with executor() as e:
            srs = list(e.map(lambda t: _aux_fetch_info(t, https), tbls))
    return reduce(lambda x, y: x + y, srs)
