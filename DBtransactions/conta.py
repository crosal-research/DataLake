##################################################
# define funcão/transacoes de recurso Conta
# conta a base de dados
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
def add_conta(contas_info:List[Tuple[str]])-> None:
    """
    Insere/atualiza conta na base na base the dados.
    input: list(conta_id, nome))
    """
    string_sql = f"""
    insert into Conta(conta_id, nome)
    values ({Q}, {Q}) on conflict (conta_id) do update set
    nome=excluded.nome;
    """
    with connect() as conn:
        cur = _cursor(conn)
        try:
            cur.executemany(string_sql, contas_info)
        except:
            print('fail')


def query_conta(contas:Optional[List[str]]=None) -> List[Tuple]:
    """
    Extrai informações de contas a partir
    dos identificadores das contas
    """
    with connect() as conn:
        cur = _cursor(conn)
        if contas:
            string_sql = """
            select * from conta 
            where conta_id in ({sep})
            """.format(sep=','.join([f"{Q}".upper()]*len(contas)))
            c = cur.execute(string_sql, contas)
        else:
            string_sql = """
            select * from conta;
            """
            c = cur.execute(string_sql) 
    return pd.DataFrame(data=c.fetchall(), 
                        columns=['conta_id', 'nome'])


def delete_conta(contas:List[str]) -> None:
    """
    Remove contas a partir
    dos identificadores das contas
    """
    string_sql = """
    delete from conta 
    where conta_id in ({seq})
    """.format(seq=','.join([f"{Q}".upper()]*len(contas)))
    with connect() as conn:
        cur = _cursor(conn)
        c = cur.execute(string_sql, contas)
