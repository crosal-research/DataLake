###############################################################################
# fetches data from cepea database
################################################################################

# import form the system
from concurrent.futures import ThreadPoolExecutor as executor
from typing import List, Tuple
from datetime import datetime as dt
from typing import Optional

# import from packages
import requests
import pandas as pd
import xlrd

#app imports
from DBtransactions.DBtypes import Series, Observation


__all__ = ['INFO', 'fetch']

# series to be included
INFO = [
    ("CEPEA.77", "Preco do milho ESALQ/BM&FBOVESPA ", "DIARIA", "CEPEA_PRECO", 'milho'), 
    ("CEPEA.23", "Preco do Café Arábia CEPEA/ESALQ", "DIARIA", "CEPEA_PRECO", 'cafe'), 
    ("CEPEA.24", "Preco do Café Robusta CEPEA/ESALQ", "DIARIA", "CEPEA_PRECO", 'cafe'), 
    ("CEPEA.53", "Preco do acucar cristal branco cepea/esalq - Sao Paulo", "DIARIA", "CEPEA_PRECO", 'acucar'), 
    ("CEPEA.92", "Preco da soja ESALQ/BM&FBOVESPA - Paranagua", "DIARIA", "CEPEA_PRECO", 'soja'), 
    ("CEPEA.2", "Cotacao do boi-Gordo CEPEA/B3", "DIARIA", "CEPEA_PRECO", 'boi-gordo'),
    ("CEPEA.103", "Cotacao do Etanol Hidratado combustível CEPEA/ESALQ", "DIARIA", "CEPEA_PRECO", 'etanol'),
    ("CEPEA.104", "Cotacao do Etanol Anidro CEPEA/ESALQ", "DIARIA", "CEPEA_PRECO", 'etanol'),
    ("CEPEA.178", "Cotacao do Trigo CEPEA/ESALQ - Parana", "DIARIA", "CEPEA_PRECO", 'trigo'),
    ("CEPEA.54", "Cotacao do Algodao em pluma CEPEA/ESALQ a vista", "DIARIA", "CEPEA_PRECO", 'algodao-a-vista'), 
    ("CEPEA.91", "Cotacao do Arroz em casca CEPEA/IRGA - RS", "DIARIA", "CEPEA_PRECO",'arroz')]


def fetch_info(info: List[Tuple]):
    return [Series(**{'series_id': srs[0], 
                      'description': srs[1], 
                      'frequency': srs[2], 
                      'survey_id': srs[3]}) for srs in info]
