# import from system
from io import BytesIO
from typing import List

# import from packages
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs


headers = {'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

url_ind = 'https://www.portaldaindustria.com.br/estatisticas/indicadores-industriais/'
url_ici = 'https://www.portaldaindustria.com.br/estatisticas/icei-indice-de-confianca-do-empresario-industrial/'

series = [{'series_id':"CNI.FATREAL", 'description': "FATURAMENTO REAL DA INDUSTRIA" , 
               'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ATIV"}, 
             {'series_id': "CNI.FATRAEL_DEZ", 'description':'FATURAMENTO REAL DA INDUSTRIA COM AJUSTE SAZONAL', 
              'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ATIV"},
             {'series_id': "CNI.EMP",'description': 'EMPREGO NA INDUSTRIA', 
              'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ATIV"}, 
             {'series_id': "CNI.EMP_DEZ",'description': 'EMPREGO NA INDUSTRIA COM AJUSTE SAZONAL', 
              'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ATIV"},
             {'series_id': "CNI.HT",'description': 'HORAS TRABALHADAS NA INDUSTRIA', 
              'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ATIV"}, 
             {'series_id': "CNI.NT_DEZ",'description': 'HORAS TRABALHADAS NA INDUSTRIA COM AJUSTE SAZONAL', 
              'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ATIV"}, 
             {'series_id': "CNI.MS", 'description': 'MASSA SALARIAL NO SETOR INDUSTRIAL', 
              'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ATIV"},
             {'series_id': "CNI.MS_DEZ", 'description': 'MASSA SALARIAL REAL NO SETOR INDUSTRIAL', 
              'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ATIV"}, 
             {'series_id': "CNI.REND",'description': 'RENDIMENTO MEDIO REAL NO SETOR INDUSTRIAL', 
              'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ATIV"},
             {'series_id': "CNI.REND_DEZ",'description': 'RENDIMENTO MEDIO REAL NO SETOR INDUSTRIAL COM AJUSTE SAZONAL', 
              'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ATIV"},
             {'series_id': "CNI.UCI", 'description': 'UTILIZACAO DA CAPACIDADE INSTALADA DA INDUSTRIAL', 
              'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ATIV"}, 
             {'series_id': "CNI.UCI_DEZ", 'description': 'UTILIZACAO DA CAPACIDADE INSTALADA DA INDUSTRIAL COM AJUSTE SAZONAL', 
              'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ATIV"},
             {'series_id': "CNI.ICEI", 'description': 'INDICE DE CONFIACA DO EMPRESARIO INDUSTRIAL', 
              'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ICEI"},
             {'series_id': "CNI.CA", 'description': 'INDICE DE CONDICOES ATUAIS DO EMPRESARIO INDUSTRAIL', 
              'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ICEI"},
              {'series_id': "CNI.EXP", 'description': 'INDICE DE EXPECTATIVAS DO EMPRESARIO INDUSTIRAL', 
              'frequency': "MENSAL", 'last_updata': None, 'survey_id': "CNI_ICEI"}]


def _process(resp:requests.Response):
    """
    Prosses response
    """
    f = BytesIO()
    f.write(resp.content)
    excel = pd.ExcelFile(f)
    if "indicadoresindustriais" in resp.url:
        df = excel.parse(sheet_name="Indicadores", skiprows=list(range(0,15))).dropna(axis=1, how='all')
        dg = df.applymap(lambda x: np.NaN if x == 0  else x).dropna(axis=1, how='all').dropna(axis=0)
        dh = dg.applymap(lambda x: np.NaN if (isinstance(x, float) and abs(x) < 10) else x).dropna(axis=1, how='all').dropna(axis=1)
        dh.columns = ['data']  + [d['series_id'] for d in series if d['survey'] == 'CNI_ATIV']
        dh = dh.set_index('data')

    elif "indicedeconfiancadoempresarioindustrial" in resp.url:
        df = excel.parse(sheet_name="Geral", skiprows=list(range(0,7))).dropna(axis=0, how='all').dropna(axis=1).head().T
        dh = df.iloc[:,[0, 1, 4]]
        dh.columns = [d['series_id'] for d in series if d['survey_id'] == 'CNI_ICEI']
    else:
        pass
    return dh


def fetch(survey: str):
    """
    Fetches ...
    """
    if survey == "CNI_ATIV":
        resp = requests.get(url_ind, headers=headers)
    else:
        resp = requests.get(url_ici, headers=headers)
    soup = bs(resp.text, "html.parser")
    url = [a for a in soup.find_all('a') if 'xlsx' in a.attrs['href']][0].attrs['href']
    return _process(requests.get(url))

def fetch_obs(tickers: List[str]):
    pass

