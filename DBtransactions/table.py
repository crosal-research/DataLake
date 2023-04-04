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

# import from app
from DBtransactions.helpers import _cursor, connect
from DBtransactions.helpers import Q


# Tables
def add_table(ticker_tbl:str, 
              description:str,
              proprietario:str, 
              tickers_series: Optional[List[str]] = None) -> None:
    """
    Insere/rodifica Table à base de dados
    """
    string_table_sql = f"""
    insert into Utable(utable_id, description, proprietario)
    values ({Q}, {Q}, {Q}) on conflict(utable_id) do update set
    description = excluded.description,
    proprietario = excluded.proprietario
    """
    string_relation_sql = f"""
    insert into series_utable(utable_id, series_id)
    values ({Q}, {Q}) on conflict(utable_id, series_id) do update set
    utable_id = excluded.utable_id,
    series_id = excluded.series_id
    """
    with connect() as conn:
        cur = _cursor(conn)
        try:
            cur.execute(string_table_sql, (ticker_tbl,
                                           description,
                                           proprietario))
        except:
            print("table creation failed")

        if tickers_series:
            inputs = [(ticker_tbl, tck ) for tck in tickers_series]           
            cur.executemany(string_relation_sql, inputs)


def query_table(tickers:List[str]):
    """
    Extrai informaçoes de um lista de Tables
    da base de dados a patir das tickers
    das tables
    """
    string_sql = f"""
    select * from uTable where utable_id = {Q}
    """
    with connect() as conn:
        cur = _cursor(conn)
        cs = []
        for tck in tickers:
            cs.append(cur.execute(string_sql, (tck,)))
            
    return pd.DataFrame(data=[c.fetchone() for c in cs])


def delete_table(tickers:List[str]) -> None:
    """
    Remove lista de tables da base de dados a parit
    dos seus tickers.
    """
    string_sql = f"""
    delete from uTable 
    where utable_id = {Q}
    """
    tickers = [(tck,) for tck in tickers]
    
    with connect() as conn:
        cur = _cursor(conn)
        cur.executemany(string_sql, tickers)
