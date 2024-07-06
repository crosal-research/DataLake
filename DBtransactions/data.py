##################################################
# Define transacoes do recurso Table com a 
# base de dados
##################################################

# import from system
import os
from typing import List, Tuple, Optional

# inport  form packages
import pandas as pd
from dotenv import dotenv_values
import pendulum

# import from app
from DBtransactions.DBtypes import Observation
from DBtransactions.helpers import _cursor, connect
from DBtransactions.helpers import Q

# Data
def add_data(llobs: List[List[Observation]]) -> None:
    """
    Insert observation in the database
    """
    string_sql = f"""
    insert into observation(dat, valor, series_id)
    values ({Q}, {Q}, {Q}) 
    on conflict (dat, series_id) do update set
    valor = excluded.valor
    """
    with connect() as conn:
        cur = _cursor(conn)
        for lobs in llobs:
            if len(lobs) > 0:
                mobs = [tuple(obs.model_dump().values()) 
                        for obs in lobs]
                cur.executemany(string_sql, mobs)
                dt = pendulum.now().format("YYYY-MM-DD HH:mm:ss")
                exp = f"""
                with cte_mm as
                (select min(dat) as min, max(dat) as max from observation where series_id = {Q})
                update series
                set last_update={Q}, first_observation = cte_mm.min, last_observation = cte_mm.max 
                from cte_mm
                where series_id = {Q};
                """
                try:
                    cur.execute(exp, (mobs[0][2], dt, mobs[0][2])) 
                except Exception as e:
                    print(e)
