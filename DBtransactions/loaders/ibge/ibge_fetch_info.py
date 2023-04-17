############################################################
# Build the series info for IBGE's data from its api
# 
############################################################
# import from system
from concurrent.futures import ThreadPoolExecutor as executor
from typing import List, Dict, Tuple
from functools import reduce

# import from packages
import requests

# import from app
from DBtransactions.DBtypes import Series


#__all__ == ['TABLES', 'fetch_info']

# IBGE's tables with relevant series
TABLES = [
    # Producao Industrial
    {'t':'8887', 'v': 12606, 'c543':'all', 's': "IBGE_PIM"},   # Produção Industrial categorias
    {'t':'8887', 'v': 12607, 'c543':'all', 's': "IBGE_PIM"},   # Produção Industrial categorias, sa
    {'t':'8886', 'v': 12606,               's': "IBGE_PIM"},   # Produção de insumos da const. civil.
    {'t':'8888', 'v': 12606, 'c544': 'all', 's': "IBGE_PIM"},  # Produção Industrial por secoes e atividades
    {'t':'8888', 'v': 12607, 'c544': 'all', 's': "IBGE_PIM"},  # Produção Industrial por secoes e atividades,sa
    # Varejo                                                           
    {'t':'8757', 'v': 7169, 'c11046': 56732, 's': "IBGE_PMC"}, # material de construcao sa
    {'t':'8757', 'v': 7170, 'c11046': 56732, 's': "IBGE_PMC"}, # material de construcao 
    {'t':'8880', 'v': 7169, 'c11046': 56734, 's': "IBGE_PMC"}, # Comercio varejista
    {'t':'8880', 'v': 7170, 'c11046': 56734, 's': "IBGE_PMC"}, # comercio varejista sa 
    {'t':'8881', 'v': 7169, 'c11046': 56736, 's': "IBGE_PMC"}, # comercio varejista ampliado
    {'t':'8881', 'v': 7170, 'c11046': 56736, 's': "IBGE_PMC"}, # comercio varejista ambiliado sa 
    {'t':'8882', 'v': 7169, 'c11046': 56734, 'c85': 'all', 's': "IBGE_PMC"}, # comercio varejista por atividades
    {'t':'8882', 'v': 7170, 'c11046': 56736, 'c85': 'all', 's': "IBGE_PMC"}, # comercio varejista por atividades sa
    {'t':'8883', 'v': 7169, 'c11046': 56734, 'c85': 'all', 's': "IBGE_PMC"}, # comercio varejista ampliado por atividades
    {'t':'8883', 'v': 7170, 'c11046': 56736, 'c85': 'all', 's': "IBGE_PMC"}, # comercio varejista ampliado por atividades sa
    {'t':'8884', 'v': 7169, 'c11046': 56738, 's': "IBGE_PMC"}, # motos, auto e peças
    {'t':'8884', 'v': 7170, 'c11046': 56738, 's': "IBGE_PMC"}, # motos, atuo e peças  sa
    # servicos
    {'t':'8161', 'v': 11621, 'c11046': 56736, 's': "IBGE_PMS"}, # volume de serviços
    {'t':'8161', 'v': 11622, 'c11046': 56736, 's': "IBGE_PMS"}, # volume de serviços sa
    {'t':'8162', 'v': 11621, 'c11046': 56736, 'c12355': 'all', 's': "IBGE_PMS"}, # volume de serviços, por atividades
    {'t':'8162', 'v': 11622, 'c11046': 56736, 'c12355': 'all', 's': "IBGE_PMS"}, # volume de serviços, por atividas sa
    {'t':'8165', 'v': 11621, 'c11046': 56728, 's': "IBGE_PMS"}, # volume de serviços, turismos
    {'t':'8165', 'v': 11622, 'c11046': 56728, 's': "IBGE_PMS"}, # volume de serviços turismo sa
    {'t':'8166', 'v': 11621, 'c11046': 56726, 'c12355': 'all' ,'s': "IBGE_PMS"}, # volume de serviços, transportes
    {'t':'8166', 'v': 11622, 'c11046': 56726, 'c12355': 'all', 's': "IBGE_PMS"}, # volume de serviços  trnsportes sa
    # contas nacionais
    {'t':'1620', 'v': 583, 'c11255': 'all','s': "IBGE_CN"}, # PIB volume setores
    {'t':'1621', 'v': 584, 'c11255': 'all','s': "IBGE_CN"}, # PIB volume setores sa
    {'t':'1846', 'v': 585, 'c11255': 'all','s': "IBGE_CN"}, # PIB precos correntes
    # mercado de trabalho
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


def _aux_fetch_info(tbl: dict, session: requests.sessions.Session) -> List[Tuple[Series]]:
    """
    Fetch info from a IBGE's table and build tickers, info, etc 
    into a series
    """
    url = _build_url(tbl)
    resp = requests.get(url)
    # process resposes
    ls = resp.json()[1:]
    tck = ((resp.url).split("t/")[1]).split("/d")[0]
    survey = tbl['s'] 
    ch = 'D3C' if len(tbl) > 4 else 'D2C'
    srs = []
    for l in ls:
        cn = f"{l['D2N']}, {l['D1N']}, Brasil" if ch == 'DC2' else f"{l['D2N']},{l['D3N']} {l['D1N']}, Brasil"
        srs.append(Series(**{'series_id': f"IBGE.{tck.replace('all', l[ch])}" if 'all' in tck else f"IBGE.{tck}",
                            'description': cn, 'survey_id': survey}))
    return srs


def fetch_info(tbls: List[dict]) -> List[Tuple[Series]]:
    """
    Fetch info from a IBGE's table and build tickers, info, etc 
    into a series
    """
    with requests.session() as session:
        with executor() as e:
            srs = list(e.map(lambda t: _aux_fetch_info(t, session), tbls))
    return reduce(lambda x, y: x + y, srs)
