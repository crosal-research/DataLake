##################################################
# define funcão/transacoes de recurso Survey
# sruvey: base de dados
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


# Conta
def add_survey(contas_info:List[Tuple[str]])-> None:
    """
    Insere/atualiza survey na base na base the dados.
    input: list(survey_id, description, source_id))
    """
    string_sql = f"""
    insert into Conta(survey_id, description, source_id)
    values ({Q}, {Q}, {Q}) on conflict (survey_id) do update set
    description=excluded.description,
    source_id=excluded.source_id;
    """
    with connect() as conn:
        cur = _cursor(conn)
        try:
            cur.executemany(string_sql, survey_info)
        except:
            print('fail')


def query_survey(surveys:Optional[List[str]]=None) -> List[Tuple]:
    """
    Extrai informações de surveys a partir
    dos identificadores dos surveys
    """
    with connect() as conn:
        cur = _cursor(conn)
        if surveys is not None:
            string_sql = """
            select * from survey
            where survey_id in ({sep})
            """.format(sep=','.join([f"{Q}".upper()]*len(surveys)))
            c = cur.execute(string_sql, surveys)
        else:
            string_sql = """
            select * from survey;
            """
            c = cur.execute(string_sql) 
    return pd.DataFrame(data=c.fetchall(), 
                        columns=['survey_id', 'description', 'source_id'])


def delete_survey(surveys:List[str]) -> None:
    """
    Remove surveys a partir
    dos seus identificadores das 
    """
    string_sql = """
    delete from survey
    where survey_id in ({seq})
    """.format(seq=','.join([f"{Q}".upper()]*len(surveys)))
    with connect() as conn:
        cur = _cursor(conn)
        c = cur.execute(string_sql, surveys)
