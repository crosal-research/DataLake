# import from system
import os
from typing import List, Tuple, Optional

# inport  form packages
import pandas as pd
from dotenv import dotenv_values

# import from app
from DBtransactions.helpers import _cursor, connect
from DBtransactions.helpers import Q



# Search
def build_search() -> None:
    """
    Insere palavras a serem utilizadas
    na table 'search' para pesquisa de series
    """
    string_sql = """
    insert into search (ticker, description) 
    select series_id, description from series
    """
    with connect() as conn:
        cur = _cursor(conn)
        c = cur.execute(string_slq)


def query_search(words:str) -> None:
    """
    Pesquisa series a partir de palavras chaves
    see: https://stackoverflow.com/questions/70847617/
                 populate-virtual-sqlite-fts5-full-text-search-table-from-content-table
    """
    string_sql = f"""select ticker, description from search 
    where search match {Q};
    """

    with sqlite3.connect() as conn:
        cur = _cursor(conn)
        try:
            c = cur.execute(string_sql, [words])        
            return pd.DataFrame(data=c, columns=['tickers', 'descricao'])
        except:
            print('fail')
