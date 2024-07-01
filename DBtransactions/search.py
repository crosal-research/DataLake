# import from system
import os, re
from typing import List, Tuple, Optional

# inport  form packages
import pandas as pd
from dotenv import dotenv_values
from unidecode import unidecode

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
        c = cur.execute(string_sql)


def query_search(words:str) -> None:
    """
    Pesquisa series a partir de palavras chaves
    see: https://stackoverflow.com/questions/70847617/
                 populate-virtual-sqlite-fts5-full-text-search-table-from-content-table
    - for the use of match keywork see: https://www.sqlite.org/fts5.html
    - for query sintax for sqlite3, see: https://www.sqlite.org/fts5.html#full_text_query_syntax
    """
    string_sql = f"""
    select monthly_tracker.mtracker as tracker, search.ticker, search.description from search 
    join monthly_tracker on search.ticker=monthly_tracker.series_id 
    where search match {Q} order by tracker desc;
    """
    cleansed_words = unidecode(re.sub("[\+ | , | ; ]", " ", words))
    with connect() as conn:
        cur = _cursor(conn)
        try:
            c = cur.execute(string_sql, [cleansed_words])
            ds = pd.DataFrame(c, columns=['popularidade', 'tickers', 'descricao'])
            return ds
        except:
            print('fail')
