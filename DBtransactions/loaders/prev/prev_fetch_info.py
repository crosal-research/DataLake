# import from system
from typing import List, Dict

# import from app
from DBtransactions.DBtypes import Series



__all__ = ['SERIES', 'fetch_info']

DATA = [
    {'series_id': "PREV.CONCE_TOTALQ",
     'description': "QUANTIDADE DE CONCESSOES BENEFICIOS, TOTAL"},
    {'series_id': "PREV.CONCE_URBQ",
     'description': "QUANTIDADE DE CONCESSOES BENEFICIOS, BENEFICIARIOS URBANOS"},
    {'series_id': "PREV.CONCE_RURALQ",
     'description': "QUANTIDADE DE CONCESSOES BENEFICIOS, BENEFICIARIOS RURAIS"},
    {'series_id': "PREV.CONCE_RGPSQ",
     'description': "QUANTIDADE DE CONCESSOES BENEFICIOS, BENEFICIOS DO RGPS"},
    {'series_id': "PREV.CONCE_ASSISTQ", 
     'description': "QUANTIDADE DE CONCESSOES BENEFICIOS, BENEFICIOS ASSISTENCIAS"},
    {'series_id': "PREV.CONCE_BLEQ", 
     'description': "QUANTIDADE DE CONCESSOES BENEFICIOS, BENEFICIOS DE LEGISLACAO ESPECIFICA"},
    {'series_id': "PREV.EST_TOTALQ", 
     'description': "ESTOQUE CONCESSOES BENEFICIOS, TOTAL"},
    {'series_id': "PREV.EST_URBQ", 
     'description': "ESTOQUE CONCESSOES BENEFICIOS, BENEFICIARIOS URBANOS"},
    {'series_id': "PREV.EST_RURALQ", 
     'description': "ESTOQUE CONCESSOES BENEFICIOS, BENEFICIARIOS RURAIS"},
    {'series_id': "PREV.EST_RGPSQ", 
     'description': "ESTOQUE CONCESSOES BENEFICIOS, BENEFICIOS DO RGPS"},
    {'series_id': "PREV.EST_ASSISTQ", 
     'description': "ESTOQUE CONCESSOES BENEFICIOS, BENEFICIOS DO ASSISTENCIAIS"},
    {'series_id': "PREV.EST_BLEQ",
     'description': "ESTOQUE CONCESSOES BENEFICIOS, BENEFICIOS DE LEGISLACAO ESPECIFICA"},


    {'series_id': "PREV.CONCE_TOTALV",
     'description': "VALOR DAS CONCESSOES BENEFICIOS, TOTAL"},
    {'series_id': "PREV.CONCE_URBV",
     'description': "VALOR DAS CONCESSOES BENEFICIOS, BENEFICIARIOS URBANOS"},
    {'series_id': "PREV.CONCE_RURALV",
     'description': "VALOR DAS CONCESSOES BENEFICIOS, BENEFICIARIOS RURAIS"},
    {'series_id': "PREV.CONCE_RGPSV",
     'description': "VALOR DAS CONCESSOES BENEFICIOS, BENEFICIOS DO RGPS"},
    {'series_id': "PREV.CONCE_ASSISTV", 
     'description': "VALOR DAS CONCESSOES BENEFICIOS, BENEFICIOS ASSISTENCIAS"},
    {'series_id': "PREV.CONCE_BLEV", 
     'description': "VALOR DAS CONCESSOES BENEFICIOS, BENEFICIOS DE LEGISLACAO ESPECIFICA"},
    {'series_id': "PREV.EST_TOTALV", 
     'description': "VALOR DOS ESTOQUE DAS CONCESSOES BENEFICIOS, TOTAL"},
    {'series_id': "PREV.EST_URBV", 
     'description': "VALOR DOS ESTOQUE DAS CONCESSOES BENEFICIOS, BENEFICIARIOS URBANOS"},
    {'series_id': "PREV.EST_RURALV", 
     'description': "VALOR DOS ESTOQUE DAS CONCESSOES BENEFICIOS, BENEFICIARIOS RURAIS"},
    {'series_id': "PREV.EST_RGPSV", 
     'description': "VALOR DOS ESTOQUE DAS CONCESSOES BENEFICIOS, BENEFICIOS DO RGPS"},
    {'series_id': "PREV.EST_ASSISTV", 
     'description': "VALOR DOS ESTOQUE DAS CONCESSOES BENEFICIOS, BENEFICIOS DO ASSISTENCIAIS"},
    {'series_id': "PREV.EST_BLEV",
     'description': "VALOR DOS ESTOQUE DAS CONCESSOES BENEFICIOS, BENEFICIOS DE LEGISLACAO ESPECIFICA"}]

    
def fetch_info(series: List[Dict[str, str]]):
    for s in series:
        s['frequency'] = 'MENSAL'
        s['last_update'] = ''
        s['survey_id'] = 'PREV_EST'
    return [Series(**s) for s in series]
