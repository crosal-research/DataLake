# import from system
import os
from typing import List, Tuple, Optional

# inport  form packages
import pandas as pd
from dotenv import dotenv_values

# import from app
from DBtransactions.helpers import _cursor, connect
from DBtransactions.helpers import Q


# Clientes
def add_cliente(clientes_info:List[Tuple[str]])-> None:
    """
    Insere/atualiza cliente à  base na base the dados
    list(nome, email, senha, conta_id)
    """
    
    string_sql = f"""
    insert into Cliente(nome, email, senha, conta_id)
    values ({Q}, {Q}, {Q}, {Q}) on conflict (email) do update set
    nome=excluded.nome,
    senha=excluded.senha,
    conta_id=conta_id
    """
    with generate_conn() as conn:
        cur = _cursor(conn)
        cur.executemany(string_sql, clientes_info)


def query_cliente(emails: List[str]) -> pd.DataFrame:
    """
    Insere/atualiza cliente à  base na base the dados
    identificados pela chave primario email
    """
    string_sql = f"""
    select cliente.nome, cliente.email, conta.nome from cliente
    join conta on cliente.conta_id = conta.conta_id
    where email in ({Q});
    """
    with connect() as conn:
        cur = _cursor(conn)
        q = cur.execute(string_sql, emails)
        return pd.DataFrame(data= [{
            'nome': c[0],
            'email': c[1],
            'conta': c[2]} for c in q.fetchall()])
    

def delete_clientes(emails:List[str]):
    """
    remove clientes da base de dados indentificados
    pela chave primaria email
    """
    string_sql = """
    delete from cliente 
    where email in ({seq})
    """.format(seq=','.join([f"{Q}".upper()]*len(emails)))

    with connect() as conn:
        cur = _cursor(conn)
        cur.execute(string_sql, emails)
