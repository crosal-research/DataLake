# import from system
from typing import Dict


# import from app
from DBtransactions.DBtypes import Series
from  DBtransactions.loaders.nucleos_ipca.core_definitions import cores

c = cores
stats_cores = {"P55":  "Nucleo Percentil 55",
               "SUAVIDADO": "Nucleo de medias aparadas suavizadas",
               "MÉDIAS_APARADAS": "Nucleo de medias aparadas"}
indexes = ["IPCA", "IPCA15"]

SERIES = []

for i in indexes:
    for c in cores:
        SERIES.append({'series_id': f"{i}.{c}", 
                       'description': f"Nucleo de bens {c}, {i}",
                       'frequency': "MENSAL",
                       'last_update': None,
                       'survey_id': f"CORE_{i}"})

for i in indexes:
    for c in stats_cores:
        SERIES.append({'series_id': f"{i}.{c}", 
                       'description': f"{stats_cores[c].upper()}, {i}",
                       'frequency': "MENSAL",
                       'last_update': None,
                       'survey_id': f"CORE_{i}"})

def fetch_info(series: Dict) -> Series:
    return [Series(**s) for s in series]
