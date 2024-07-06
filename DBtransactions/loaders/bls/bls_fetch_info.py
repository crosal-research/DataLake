# import from system
from typing import List, Tuple
import os, json

# import from packages
import pandas as pd
import requests
from dotenv import dotenv_values

# import from app
from DBtransactions.DBtypes import Series

config = dotenv_values("./.env")
_key_bls=config["BLS_KEY"]

# path_to_file = os.path.dirname(os.path.abspath(__file__)) + "/datasource.xlsx"


INFO = [{'survey': "BLS_CU", 'description': "Consumer Price Index - All Urban Consumer", 
         'source': "BLS", "Frequency": "MENSAL", 'series': 'all'},
        {'survey': "BLS_ND", 'description': "Producer Price Index Industry Data", 
         'source': "BLS", "Frequency": "MENSAL"},
        {'survey': "BLS_LN", 'description': "Labor Force Statistics from the Current Population Survey (SIC)", 
         'source': "BLS", 'Frequency': 'MENSAL',
         'tickers': ["LNS14000000", "LNS11300000", "LNS12000000", "LNS14000006"]}, # Mensal
        {'survey': "BLS_CE", 'description': "Employment, Hours, and Earnings from the Current Employment Statistics survey (National)", 'source': "BLS", 'frequency': 'MENSAL', 
         'tickers': ["CES0000000001", "CES0500000003", "CES0500000001", "CES3000000001", "CES0500000002"] } # Mensal
        ]


def build_url(survey):
    """
    Build url for searching the main series of a particular survey. Usefull for the 
    case of investigating these tickers
    """
    return f"https://api.bls.gov/publicAPI/v2/timeseries/popular?survey={survey.split('_')[1]}"

def fetch_info(survey: str) -> List[Series]: 
    """
    Takes a string - path for the file - and returns
    a list of list, where the inner list is three dimnension
    with information about series
    """
    if survey['survey'] == "BLS_CU":
        ds = pd.read_excel(path_to_file, sheet_name="Pub level",
                           usecols=[0, 1], skiprows=[0], skipfooter=3)
        return  [Series(**{'series_id': "BLS.CUSR0000" + i[0], 
                           'description': f"{i[1]}, U.S.A. Consumer Price Index (CPI)", 'last_update': None,
                           'survey_id': "BLS_CPI", 'frequency': "MENSAL"}) for i in ds.values if i[0] not in ["AAO", "AAOR"]]
    else:
        url = f"https://api.bls.gov/publicAPI/v2/timeseries/data/?"
        headers = {'Content-type': 'application/json'}
        resp = requests.post(url, data=json.dumps({'seriesid': [i['tickers'] for i in INFO if i['survey'] == survey][0],
                                                   'registrationkey': _key_bls,
                                                   'catalog': True, 
                                                   'startyear': "2023", 
                                                   'endyear': "2023"}), headers=headers)
        if resp.ok:
            srs = [Series(**{
                'series_id': f"BLS.{s['catalog']['series_id']}",
                'description': s['catalog']['series_title'],
                'frequency': 'MENSAL' if f"BLS_{s['catalog']['survey_abbreviation']}" in ["BLS_LN", "BLS_CE", "BLS_ND"] else None,
                'survey_id': f"BLS_{s['catalog']['survey_abbreviation']}"}) 
                   for s in resp.json()["Results"]['series']]
            return srs
        print(f"Failed to build series for survey {suvey}")
