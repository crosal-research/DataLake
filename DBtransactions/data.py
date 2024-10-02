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
import aiosqlite # does not commit automatically

from DBtransactions.DBtypes import Observation, Series
from DBtransactions.helpers import Q

async def add_data_obs(llobs: List[List[Observation]]) -> None:
    """
    Insert observation in the database
    """
    async with aiosqlite.connect(DB) as db:
        async with db.cursor() as cur:
            await cur.execute("PRAGMA foreign_keys = ON;") # allows for foreign_keys constraing
            await cur.execute("PRAGMA journal_model = ON;") # <--
            string_sql = f"""
            insert into observation(dat, valor, series_id)
            values ({Q}, {Q}, {Q}) 
            on conflict (dat, series_id) do update set
            valor = excluded.valor
            """
            for lobs in llobs:
                if len(lobs) > 0:
                    mobs = [tuple(obs.model_dump().values()) 
                            for obs in lobs]
                    try:
                        c = await cur.executemany(string_sql, mobs)
                    except Exception as e:
                        await db.rollback()
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
                        await cur.execute(exp, (mobs[0][2], dt, mobs[0][2]))
                        await db.commit()
                    except Exception as e:
                        await db.rollback()
                        print(e)
        


# To be implemented
async def add_data_series(lseries: List[Series]) -> None:
    """
    Insert observation in the database
    """
    async with aiosqlite.connect(DB) as db:
        async with db.cursor() as cur:
            await cur.execute("PRAGMA foreign_keys = ON;") # allows for foreign_keys constraing
            await cur.execute("PRAGMA journal_model = ON;") # <--

            string_sql = f"""
            insert into series(series_id, description, survey_id, frequency, last_update)
            values({Q}, {Q}, {Q}, {Q}, {Q})
            on conflict(series_id) do update set
            description=excluded.description,
            survey_id=excluded.survey_id,
            frequency=excluded.frequency;
            """
            def _input(linfo: List[Series]) -> List[Tuple[str]]:
                """
                Helper function to raise letters to upper case
                """
                return [tuple(map(lambda x: x.upper() if x is not  None else None, l.model_dump().values()))
                        for l in linfo]

            try:
                ls = _input(lseries) 
                print(ls)
                await cur.executemany(string_sql, ls)
            except Exception as e:
                print(e)
                print("Failed to insert series")

            await db.commit()
            
            

