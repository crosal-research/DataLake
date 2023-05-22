#import from system
from typing import Optional, List, Union
from functools import reduce

# import from app
from DBtransactions.DBtypes import Series

__all__ = ["fetch_into", "source", "surveys"]


surveys = {'BIS_WS_EER_M': 'WS_EER_M'}
source = list(surveys.keys())


Regions = {"DZ":"Algeria",
           "AR":"Argentina",
           "AU":"Australia",
           "AT":"Austria",
           "BE":"Belgica",
           "BA":"Bosnia & Herzegovina",
           "BR":"Brasil",
           "BG":"Bulgaria",
           "CA":"Canada",
           "CL":"Chile",
           "CN":"China",
           "TW":"China Taipei",
           "CO":"Colombia",
           "HR":"Croatia",
           "CY":"Ciprus",
           "CZ":"Republica Tcheca",
           "DK":"Dinamarca",
           "EE":"Estonia",
           "FI":"Finlandia",
           "FR":"Franca",
           "DE":"Alemanha",
           "GR":"Grecia",
           "HK":"Hong Kong SAR",
           "HU":"Hungria",
           "IS":"Islandia",
           "IN":"India",
           "ID":"Indonesia",
           "IE":"Irlandia",
           "IL":"Israel",
           "IT":"Italia",
           "JP":"Japaa",
           "KR":"Corea",
           "LV":"Latavia",
           "LT":"Lituania",
           "LU":"Luxembourg",
           "MY":"Malasia",
           "MT":"Malta",
           "MX":"Mexico",
           "MA":"Moroco",
           "NL":"Holanda",
           "NZ":"Nova Zelandia",
           "MK":"Macedonio do Norte",
           "NO":"Noruega",
           "PE":"Peru",
           "PH":"Filipinas",
           "PL":"Polonia",
           "PT":"Portugal",
           "RO":"Romenia",
           "RU":"Russia",
           "SA":"Arabia Saudita",
           "RS":"Servia",
           "SG":"Singapure",
           "SK":"Eslovaquia",
           "SI":"Eslovenia",
           "ZA":"Africa do Sul",
           "ES":"Espanha",
           "SE":"Suecia",
           "CH":"Suica",
           "TH":"Tailandia",
           "TR":"Turquia",
           "AE":"Emirados Arabes",
           "GB":"Reino Unido",
           "US":"Estados Unidos da America (U.S.A.)", 
           "XM": "Zona do Euro"}

#BIS Real Effective Exchange Rates Monthly
# WS_EER_M: survey
# M: frequency
# R: Real, EET_TYPE
# B: Broad Basket


def fetch_info(info: Union[str, list]) -> Optional[List[Series]]:
    if isinstance(info, str):
        if info == 'WS_EER_M':
            return [Series(**{'series_id': f"BIS.{info}/M.R.B.{r}", 
                              'description': f"Taxa de Cambio Real Efetiva, {Regions[r]}", 
                              'survey_id': [k for k in surveys if surveys[k] == info][0] ,
                              'frequency': "MENSAL"}) for r in Regions]
    else:
        return reduce(lambda x, y: x + y, [fetch_info(s) for s in source])
        

