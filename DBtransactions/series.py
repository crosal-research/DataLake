##################################################
# Define transacoes do recurso Series com a 
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
from DBtransactions.loaders.fetcher_info import fetch_infos
from DBtransactions.DBtypes import Series

def add_series(source:Optional[str]=None,
               survey: Optional[str]=None,
               tickers:List[Optional[str]]=None) -> None:
    """
    Insert/Update a list of series in the
    database
    """
    string_sql = f"""
        insert into series(series_id, description, survey_id, frequency, last_update)
           values({Q}, {Q}, {Q}, {Q}, {Q})
           on conflict(series_id) do update set
        	  description=excluded.description,
        	  survey_id=excluded.survey_id,
        	  frequency=excluded.frequency;
        """
    def _input(linfo: List[Series]) -> Tuple[str]:
        """
        Helper function to raise letters to upper case
        """
        return [tuple(map(lambda x: x.upper() if x is not  None else None, l.model_dump().values()))
                for l in linfo]

    if source is not  None:
        linfo = fetch_infos(source=source)
    elif survey is not  None:
        linfo = fetch_infos(survey=survey)
    else:
        linfo = fetch_infos(tickers=tickers)
    with connect() as conn:
        cur = _cursor(conn)
        try:
            cur.executemany(string_sql, _input(linfo))
        except Exception as e:
            print(f"Failed to insert series: {e}")

def query_tickers(survey:Optional[str]=None,
                  source:Optional[str]= None):
    """
    recupera os tickers de series relacionados a um survey
    ou source
    """
    if survey:
        string_sql = f"""
        select series.series_id from series
        join survey on series.survey_id = survey.survey_id
        where survey.survey_id = {Q};
        """
        query_var = survey
    else:
        string_sql = f"""
        select series.series_id from series
        join survey on series.survey_id = survey.survey_id
        join source on survey.source_id = source.source_id
        where source.source_id = {Q};
        """
        query_var = source

    with connect() as conn:
        cur = _cursor(conn)
        c = cur.execute(string_sql, (query_var,))
        return [d[0] for d in c.fetchall()]


def query_series(series_tickers:List[str]=[], survey:str='', source:str='') -> List[Tuple[str]]:
    """
    extrai informações de series determinadas pela
    1) list do seus respectivos tickers
    2) o survey a qual pertencem
    3) fonte a qual pertencem
    4) totas as series
    """
    string_sql = """
    select Series.series_id, Series.description, Series.last_update, Source.full_name from Series
    join Survey on Series.survey_id = Survey.survey_id
    join Source on Survey.source_id = Source.source_id
    where series_id in ({sep})
    """.format(sep=','.join([f"{Q}".upper()]*len(series_tickers)))

    with connect() as conn:
        cur = _cursor(conn)
        q =  cur.execute(string_sql, series_tickers)
    df = pd.DataFrame(data=q.fetchall(), 
                      columns=['Ticker', "Descricao", "last_update", "Fonte"])
    return df.set_index(['Ticker'])


def delete_series(tickers=List[str]):
    """
    remove da base de dados uma lista de séries determinadas
    por uma lista do seus respectivos tickers
    """
    string_sql="""
    delete from series where series_id in ({seq})
    """.format(seq=','.join([f"{Q}".upper()]*len(tickers)))

    with connect() as conn:
        cur = _cursor(conn)
        for tck in tickers:
            cur.execute(string_sql,(tck,))
