# import from system
import os, json
from typing import List, Dict

# import from app
from DBtransactions.DBtypes import Series


__all__ = ["DATA", 'fetch_info']


DATA = [
    {'series_id': 'ABCR.BZLEVES',
     'description': 'Fluxo por pracas pedagiadas de veiculos leves, Brasil',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id': "ABCR_FLUXO"
     },
    {'series_id': 'ABCR.BZPESADOS',
     'description': 'Fluxo por pracas pedagiadas de veiculos pesados, Brasil',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
    },
    {'series_id': 'ABCR.BZTOTAL',
     'description': 'Fluxo total de veiculos por pracas pedagiadas, Brasil',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
    },
    {'series_id': 'ABCR.SPLEVES',
     'description': 'Fluxo por pracas pedagiadas de veiculos leves, Sao Paulo',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
     },
    {'series_id': 'ABCR.SPPESADOS',
     'description': 'Fluxo por pracas pedagiadas de veiculos pesados, Sao Paulo',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
    },
    {'series_id': 'ABCR.SPTOTAL',
     'description': 'Fluxo total de veiculos por pracas pedagiadas, Sao Paulo',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
    },
    {'series_id': 'ABCR.RJLEVES',
     'description': 'Fluxo por pracas pedagiadas de veiculos leves, Rio de Janeiro',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
     },
    {'series_id': 'ABCR.RJPESADOS',
     'description': 'Fluxo por pracas pedagiadas de veiculos pesados, Rio de Janeiro',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
    },
    {'series_id': 'ABCR.RJTOTAL',
     'description': 'Fluxo total de veiculos por pracas pedagiadas total, Rio de Janeiro',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
     },

    {'series_id': 'ABCR.BZLEVES_ADJS',
     'description': 'Fluxo por pracas pedagiadas de veiculos leves com ajuste sazonal, Brasil',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
     },
    {'series_id': 'ABCR.BZPESADOS_ADJS',
     'description': 'Fluxo por pracas pedagiadas de veiculos pesados com ajuste sazonal, Brasil',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
    },
    {'series_id': 'ABCR.BZTOTAL_ADJS',
     'description': 'Fluxo total de veiculos por pracas pedagiadas  com ajuste sazonal, Brasil',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
    },
    {'series_id': 'ABCR.SPLEVES_ADJS',
     'description': 'Fluxo por pracas pedagiadas de veiculos leves com ajuste sazonal, Sao Paulo',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
     },
    {'series_id': 'ABCR.SPPESADOS_ADJS',
     'description': 'Fluxo por pracas pedagiadas de veiculos pesados com ajuste sazonal, Sao Paulo',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
    },
    {'series_id': 'ABCR.SPTOTAL_ADJS',
     'description': 'Fluxo total de veiculos por pracas pedagiadas total com ajuste sazonal, Sao Paulo',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
    },
    {'series_id': 'ABCR.RJLEVES_ADJS',
     'description': 'Fluxo por pracas pedagiadas de veiculos leves com ajuste sazonal, Rio de Janeiro',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
     },
    {'series_id': 'ABCR.RJPESADOS_ADJS',
     'description': 'Fluxo por pracas pedagiadas de veiculos pesados com ajuste sazonal, Rio de Janeiro',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
    },
    {'series_id': 'ABCR.RJTOTAL_ADJS',
     'description': 'Fluxo total de veiculos por pracas pedagiadas  com ajuste sazonal, Rio de Janeiro',
     'last_update': '',
     'frequency': "MENSAL", 
     'survey_id':"ABCR_FLUXO"
    }
]


def fetch_info(data: List[Dict[str, str]]) -> List[Series]:
    """
    Adds into the Database que information pertaining to each series of
    the ABCR survey
    """
    return [Series(**d) for d in data]
