# import from packages
import requests
from typing import List

# import from app
from DBtransactions.DBtypes import Series

# Final
# years for which add series for year-end estimates
anos = [2023, 2024, 2025, 2026, 2027]

def fetch_info() -> List[Series]:
    """
    returns series of BCB's expectations API
    """
    series_list  = [[(f"bcb.ipcaexp_{ano}final".upper(), f" Expectativa Mediana de Mercado: IPCA (yoy%), final de {ano}, Brasil", "BCB_EXP_ANUAL"),
                     (f"bcb.pibexp_{ano}final".upper(), f"Expectativa Mediana de Mercado: PIB (yoy%), final de {ano}, Brasil", "BCB_EXP_ANUAL"),
                     (f"bcb.selicexp_{ano}final".upper(), f"Expectativa Mediana de Mercado: Meta Over-Selic (%), final de {ano}, Brasil", "BCB_EXP_ANUAL"),
                     (f"bcb.cambioexp_{ano}final".upper(), f"Expectativa Mediana de Mercado: Taxa de Câmbio (R$/USD), final de {ano}, Brasil", "BCB_EXP_ANUAL"),
                     (f"bcb.primarioexp_{ano}final".upper(), f"Expectativa Mediana de Mercado: Resultado Primario (% PIB) , final de {ano}, Brasil", "BCB_EXP_ANUAL")

] 
                    for ano in anos]

    series = [{"series_id":item[0], 
               "description":item[1],
               "frequency": "DIARiA",
               "last_update": None,
               "survey_id":item[2] }
              for sublist in series_list for item in sublist]

    # 12 meses
    series.append({"series_id": "BCB.IPCAEXP_12M", 
                   "description": 'Expectativa mediana do IPCA 12 meses a frente, Brasil', "frequency": "DAILY", 
                   "last_update": None, "survey_id": 'BCB_EXP_12M'})

    return [Series(**s) for s in series]
