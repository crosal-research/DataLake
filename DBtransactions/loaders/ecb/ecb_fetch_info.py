# import from system
from typing import List, Dict, Optional

# import from app
from DBtransactions.DBtypes import Series


series:Dict[str, List[str]] = {
                         "ECB.USD/MXN": ["ECB_EXR", "Pesos mexicanos por dólares do Estadunidenses"],
                         "ECB.USD/BRL": ["ECB_EXR", "Reais brasileiros por dólares do Estadunidenses"],
                         # "ECB.USD/CLP": ["ECB_EXR", "Pesos Chilenos por dólares do Estadunidenses"],
                         # "ECB.USD/COP": ["ECB_EXR", "Pesos Colombianos por dólares do Estadunidenses"], not available at ECB
                         "ECB.USD/ZAR": ["ECB_EXR", "Rand da Africa do sul por dólares do Estadunidenses"],
                         "ECB.USD/TRY": ["ECB_EXR", "Liras turcas por dólares do Estadunidenses"],
                         "ECB.USD/JPY": ["ECB_EXR", "Iens japoneses por dólares do Estadunidenses"],
                         "ECB.USD/CHF": ["ECB_EXR", "Francos suíçoo por dólares do Estadunidenses"],
                         "ECB.USD/CAD": ["ECB_EXR", "Dólares Canadenses por dólares do Estadunidenses"],
                         "ECB.NZD/USD": ["ECB_EXR", "Dólares Estadunidenses por dólares da Neozelandês"],
                         "ECB.EUR/USD": ["ECB_EXR", "Dólares Estadunidenses por Euros"],
                         "ECB.GBP/USD": ["ECB_EXR", "Dólares Estadunidenses por Libras Esterlinas"],
                         "ECB.USD/CNY": ["ECB_EXR", "Rembini chinês por dólares do Estadunidenses"],
                         "ECB.USD/INR": ["ECB_EXR", "Rubis indianos por dólares do Estadunidenses"],
                         "ECB.AUD/USD": ["ECB_EXR", "Dólares Estadunidenses por dólares do Australianos"],
                         "ECB.USD/KRW": ["ECB_EXR", "Won Sul-Coreano por dólares do Estadunidenses"],
                         "ECB.USD/NOK": ["ECB_EXR", "Coroa Norueguesas por dólares do Estadunidenses"], 
                         "ECB.USD/HKD": ["ECB_EXR", "Dolares de Hong Kong por dólares do Estadunidenses"]}

DATA:List[Series] = [{'series_id': tck,
                      'description': f'Taxa de Cambio: {series[tck][1]}',
                      'survey_id': series[tck][0],
                      'last_update': None,
                      'frequency': 'DIARIA'} for tck in series]


def fetch_info(series: List[Dict[str, str]]) -> List[Series]:
    """
    takes a list of dictionries with information a particular series
    and return 
    """
    return [Series(**s) for s in DATA]
