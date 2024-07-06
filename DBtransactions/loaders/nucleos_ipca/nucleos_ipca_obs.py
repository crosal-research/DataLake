# import from system
import os
from typing import List, Tuple, Optional

# inport  form packages
import pandas as pd
from dotenv import dotenv_values

# import from app
from DBtransactions.helpers import _cursor, connect, _parser_to_input, Q
from DBtransactions.DBtypes import Observation


def load_var(dat, cpi):
    """
    fetches from DB ipca's (ipca15) changes
    from date 'dat' forward
    """
    inflation = 7060 if cpi == 'IPCA' else 7062
    tbl = 63 if cpi == 'IPCA' else 355

    sql = f"""
    SELECT dat, series_id, valor from observation
    where series_id like 'IBGE.{inflation}/V/{tbl}/%'
    and dat >= ?
    """
    with connect() as conn:
        cur = _cursor(conn)
        q = cur.execute(sql, [dat])
        df = pd.DataFrame(data=q.fetchall(), 
                          columns=['dat', 'ticker', 'weigth']).set_index(['dat'])
        
    return df


def load_weight(dat, cpi):
    """
    fetches from DB ipca's (ipca15) weights
    from date 'dat' forward
    """
    inflation = 7060 if cpi == 'IPCA' else 7062
    tbl = 66 if cpi == 'IPCA' else 357

    sql = f"""
    SELECT dat, series_id, valor from observation
    where series_id like 'IBGE.{inflation}/V/{tbl}/%'
    and dat >= ?
    """
    with connect() as conn:
        cur = _cursor(conn)
        q = cur.execute(sql, [dat])
        df = pd.DataFrame(data=q.fetchall(), 
                          columns=['dat', 'ticker', 'weigth']).set_index(['dat'])
    return df
    
