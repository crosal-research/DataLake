# import system
from typing import List, Dict


# import from app
from DBtransactions.DBtypes import Series


# Series with information for NCAGED
DATA = [
        {"series_id": "CAGED.ADM_ADJS", 
         'description': "ADMISSOES DE EMPREGADOS FORMAIS, COM AJUSTE",
         'last_update': None,
         'frequency': "MENSAL",
         'survey_id': 'NCAGED'},
        {"series_id": "CAGED.DESLIG_ADJS", 
         'description': "DESLIGAMENTO DE EMPREGADOS NO SETOR FORMAL, COM AJUSTE",
         'last_update': None,
         'frequency': "MENSAL",
         'survey_id': 'NCAGED'},
        {"series_id": "CAGED.EST_ADJS", 
         'description': "ESTOQUE DE TRABALHADORES FORMAIS, COM AJUSTE",
         'last_update': None,
         'frequency': "MENSAL",
         'survey_id': 'NCAGED'},
        {"series_id": "CAGED.SALDO_ADJS", 
         'description': "CONTRATACAO LÍQUIDA DE TRABALHADORES FORMAIS, COM AJUSTE",
         'last_update': None,
         'frequency': "MENSAL",
         'survey_id': 'NCAGED'},
        {"series_id": "CAGED.SMADM", 
         'description': "SALARIO MEDIO REAL DOS TRABALHADORES ADMITIDOS",
         'last_update': None,
         'frequency': "MENSAL",
         'survey_id': 'NCAGED'},
        {"series_id": "CAGED.SMDESLIG", 
         'description': "SALARIO MEDIO REAL DOS TRABALHADORES DESLIGADOS",
         'last_update': None,
         'frequency': "MENSAL",
         'survey_id': 'NCAGED'}
]


def fetch_info(data: List[Dict[str, str]]) -> List[Series]:
    """
    Adds into the Database que information pertaining to each series of
    the NCAGED survey
    """
    return [Series(**d) for d in data]
