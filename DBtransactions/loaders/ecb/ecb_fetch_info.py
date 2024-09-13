# import from system
from typing import List, Dict, Optional

# import from app
from DBtransactions.DBtypes import Series


series:Dict[str, List[str]] = {
                         "ECB.USD/MXN": ["ECB_EXR", "Taxa de Cambio: Pesos mexicanos por dólares do Estadunidenses"],
                         "ECB.USD/BRL": ["ECB_EXR", "Taxa de Cambio: Reais brasileiros por dólares do Estadunidenses"],
                         # "ECB.USD/CLP": ["ECB_EXR", "Pesos Chilenos por dólares do Estadunidenses"],
                         "ECB.USD/ZAR": ["ECB_EXR", "Taxa de Cambio: Rand da Africa do sul por dólares do Estadunidenses"],
                         "ECB.USD/TRY": ["ECB_EXR", "Taxa de Cambio: Liras turcas por dólares do Estadunidenses"],
                         "ECB.USD/JPY": ["ECB_EXR", "Taxa de Cambio: Iens japoneses por dólares do Estadunidenses"],
                         "ECB.USD/CHF": ["ECB_EXR", "Taxa de Cambio: Francos suíçoo por dólares do Estadunidenses"],
                         "ECB.USD/CAD": ["ECB_EXR", "Taxa de Cambio: Dólares Canadenses por dólares do Estadunidenses"],
                         "ECB.NZD/USD": ["ECB_EXR", "Taxa de Cambio: Dólares Estadunidenses por dólares da Neozelandês"],
                         "ECB.EUR/USD": ["ECB_EXR", "Taxa de Cambio: Dólares Estadunidenses por Euros"],
                         "ECB.GBP/USD": ["ECB_EXR", "Taxa de Cambio: Dólares Estadunidenses por Libras Esterlinas"],
                         "ECB.USD/CNY": ["ECB_EXR", "Taxa de Cambio: Rembini chinês por dólares do Estadunidenses"],
                         "ECB.USD/INR": ["ECB_EXR", "Taxa de Cambio: Rubis indianos por dólares do Estadunidenses"],
                         "ECB.AUD/USD": ["ECB_EXR", "Taxa de Cambio: Dólares Estadunidenses por dólares do Australianos"],
                         "ECB.USD/KRW": ["ECB_EXR", "Taxa de Cambio: Won Sul-Coreano por dólares do Estadunidenses"],
                         "ECB.USD/NOK": ["ECB_EXR", "Taxa de Cambio: Coroa Norueguesas por dólares do Estadunidenses"], 
                         "ECB.USD/HKD": ["ECB_EXR", "Taxa de Cambio: Dolares de Hong Kong por dólares do Estadunidenses"], 
                         "ECB.MRR_FR": ["ECB_FM", "TAXA REPO DE POLITICA MONETARIA DO ECB (MAIN REFINANCING OPERATIONS)"], 
                         "ECB.DFR": ["ECB_FM", "TAXA DE DEPOSITO DE POLITICA MONETARIA DO ECB (DEPOSIT FACILITY)"], 
                         "ECB.MLFR": ["ECB_FM", "TAXA DE EMPRESTIMO DE POLITICA MONETARIA DO ECB (MAIN LENDING FACILITY)"]}



DATA:List[Series] = [{'series_id': tck,
                      'description': (f'{series[tck][1]}') if "USD" else f'{series[tck][1]}',
                      'survey_id': series[tck][0],
                      'last_update': None,
                      'frequency': 'DIARIA'} for tck in series]


def _fetch_dataflow(ticker):
    """
    returns a dataflow, according to the ECB classification, from a
    ticker of the database
    """
    return [d['survey_id'] for d in DATA if d['series_id'] == ticker][0].split("_")[1]


def fetch_info(survey:Optional[str]=None) -> List[Series]:
    """
    takes a list of dictionries with information a particular series
    and return 
    """
    if survey:
        return [Series(**s) for s in DATA if s['survey_id'] == survey]
    return [Series(**s) for s in DATA]
