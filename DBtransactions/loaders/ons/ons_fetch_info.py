from DBtransactions.DBtypes import Series

regions = {"N": 'NORTE', 
           "NE": 'NORDESTE', 
           "S": "SUL", 
           "SE": "SUDESTE"}

def fetch_info():
    info = []
    for sistema in ['N', 'NE', 'S', 'SE']:
        info.append(Series(**{'series_id': f"ONS.ENAPERC_{sistema}", 
                              'description': f"Percentual da Energia Natural Afluente utilizada na região {regions[sistema]}", 
                              'frequency': "MENSAL", 
                              'survey_id': "ONS_ENA"}))
    return info
