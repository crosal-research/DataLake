# import from system
import os
from typing import List, Tuple, Optional

# inport  form packages
import pandas as pd
from dotenv import dotenv_values

# import from app
from DBtransactions.helpers import _cursor, connect, _parser_to_input
from DBtransactions.helpers import Q
from DBtransactions.loaders.fetcher_obs import fetch


LDATE="1800" #limite inferior para datas na base de dados


def query_obs(tickers:List[str], limit:Optional[str]=LDATE):
    string_sql="""
    select dat, valor, series_id from observation
    where series_id in ({seq}) and dat >= {limit}
    order by dat asc
    
    """.format(seq=','.join([f"{Q}".upper()]*len(tickers)), limit=Q)
    ticks =(*tickers, limit)


    with connect() as conn:
        cur = _cursor(conn)
        q = cur.execute(string_sql, ticks)

    df = pd.DataFrame(data=q.fetchall(), 
                      columns=["data", "valor", "tickers"])
    df_new = df.pivot(index='data', columns=['tickers'], values='valor')
    return df_new.loc[:, tickers]
    

def add_obs(tickers:Optional[List[str]]=None, 
            survey:Optional[str]=None, 
            source:Optional[str]=None, 
            db:Optional[str]=None):
    """
    Insere/substituin dados para list the series,
    series de um survey, de uma fonta ou de toda
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
        tcks = tickers
    elif survey:
        string_sql_aux = f"""
        select series.series_id from survey
        join series on series.survey_id = survey.survey_id
        where survey.survey_id = {Q}
        """
    elif source:
        string_sql_aux = f"""
        select series.series_id from source
        join survey on survey.source_id = source.source_id
        join series on series.survey_id = survey.survey_id
        where source.source_id = {Q}
        """
    else:
        string_sql_aux = f"""
        select series_id from series
        """

    with connect() as conn:
        cur = _cursor(conn)
        if string_sql_aux:
            if survey:
                c = cur.execute(string_sql_aux, (survey,))
            elif source:
                c = cur.execute(string_sql_aux, (source,))
            else:
                c = cur.execute(string_sql_aux)
            tcks = [tck[0] for tck in c.fetchall()]
        dfs = fetch(tcks)
        for df in dfs:
            cur.executemany(string_sql, _parser_to_input(df))
