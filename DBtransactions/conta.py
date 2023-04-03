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
    Insere/atualiza conta na base na base the dados
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


def query_conta(contas:List[str]):
    """
    Extrai informações de contas a partir
    dos identificadores das contas
    """
    pass


def delete_conta(contas:List[str]):
    """
    Remove contas a partir
    dos identificadores das contas
    """
    pass
