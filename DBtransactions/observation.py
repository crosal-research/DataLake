# import from system
import os
from typing import List, Tuple, Optional

# inport  form packages
import pandas as pd
from dotenv import dotenv_values
import pendulum
import aiosqlite
import uvloop

# import from app
from DBtransactions.helpers import _cursor, connect, _parser_to_input
from DBtransactions.helpers import Q
from DBtransactions.loaders.fetcher_obs import fetch
from DBtransactions.DBtypes import Observation


LDATE="1800-01-01" #limite inferior para datas na base de dados


def query_obs(tickers:List[str] = None, 
              table:Optional[str]=None,
              limit:Optional[str]=None) -> pd.DataFrame:
    """
    Extrai observations de um lista de séries indentificadas
    pela a lista de seus respectivos tickers, a parti de uma 
    data limite inferior
    """
    if table:
        string_sql_aux=f"""
        select series_id from series_utable
        where utable_id = {Q}
        """
        with connect() as conn:
            cur = _cursor(conn)
            q = cur.execute(string_sql_aux, (table,))
            tickers = [srs[0] for srs in q.fetchall()]
    
    string_sql="""
    select dat, valor, series_id from observation
    where series_id in ({seq}) and dat >= {limit}
    order by dat asc
    """.format(seq=','.join([f"{Q}".upper()]*len(tickers)), limit=Q)
    ticks = (*tickers, limit if limit else LDATE)
    
    with connect() as conn:
        dt = pendulum.now().format("YYYY-MM-DD HH:mm:ss") 
        inp = [(tck, dt) for tck in tickers]
        exp = f"insert into tracker(series_id, timeA) values({Q}, {Q})"
        cur = _cursor(conn)
        cur.executemany(exp, inp)
        q = cur.execute(string_sql, ticks)
    
    df = pd.DataFrame(data=q.fetchall(), 
                      columns=["data", "valor", "tickers"])
    
    df_new = df.pivot(index='data', columns=['tickers'], values='valor').fillna(value="")

    return df_new.loc[:, tickers]
    

def add_obs(tickers:Optional[List[str]]=None,
            table: Optional[str]=None,
            survey:Optional[str]=None, 
            source:Optional[str]=None, 
            db:Optional[str]=None, 
            limit:Optional[int] | Optional[str]=None) -> None:
    """
    Insere/substitui dados para list the series,
    series de um, survey, de uma fonte ou de toda
    a base de dados
    """
    string_sql = f"""
    insert into observation(dat, valor, series_id)
    values ({Q}, {Q}, {Q}) 
    on conflict (dat, series_id) do update set
    valor = excluded.valor
    """
    if tickers:
        string_sql_aux = ""
        tcks = [tickers] if isinstance(tickers, str) else tickers
    elif table:
        string_sql_aux = f"""
        select series_id from series_utable
        where utable_id = {Q}
        """
    elif survey:
        string_sql_aux = f"""
        select series_id from series where survey_id = {Q}
        """
    elif source:
        string_sql_aux = f"""
        select series.series_id from source
        join survey on survey.source_id = source.source_id
        join series on series.survey_id = survey.survey_id
        where source.source_id = {Q}
        """
    else: # all series from the database
        string_sql_aux = f"""
        select series_id from series
        """
    with connect() as conn:
        cur = _cursor(conn)
        if string_sql_aux:
            if survey:
                c = cur.execute(string_sql_aux, (survey,))
            elif table:
                c = cur.execute(string_sql_aux, (table.upper(),))
            elif source:
                c = cur.execute(string_sql_aux, (source,))
            else:
                c = cur.execute(string_sql_aux)
            tcks = [tck[0] for tck in c.fetchall()]
        try:
            llobs = fetch(tcks, limit=limit)
        except Exception as e:
            print(f"File observation: {e}")
    
        for lobs in llobs:
            if len(lobs) > 0:
                mobs = [tuple(obs.model_dump().values()) 
                        for obs in lobs]
                try:
                    cur.executemany(string_sql, mobs)
                except Exception as e:
                    print(e)
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
