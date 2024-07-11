# import from system
import os, json
from typing import List, Dict

# import from app
from DBtransactions.DBtypes import Series


with open(os.getcwd() + "/DBtransactions/loaders/stn/data.json", "r") as f:
    dat = json.loads(f.read())
    DATA = []
    for d in dat:
        if d['series_id'] != 'STN.431512':
            DATA.append(dict((k, (lambda i: None if (i=="") else i)(d[k])) for k in d))

    
def fetch_info(data: List[Dict[str, str]]) -> List[Series]:
    """
    Adds into the Database que information pertaining to each series of
    the NCAGED survey
    """
    return [Series(**d) for d in data]
