##################################################
# Helpers para operacionalizar transaoes
# Generaliza-los para escolher entre Sqlite3
# e postgres
# data =  28/03/2022
##################################################

# import from system
import sqlite3
from typing import List, Tuple


# import from packages
import pandas as pd
from dotenv import dotenv_values


config = dotenv_values(f"./.env")
DB = f"{config['DB_sqlite']}"

# import the right sql engine
if config['ENV'] == "DEV":
    import sqlite3 as engine

# character for interpolation to avoid sql injection attack
Q = '?' if config['ENV'] == "DEV" else "%s"



# Helpers
def _parser_to_input(df:pd.DataFrame) -> List[Tuple]:
    """
    Helper to parse a one column datafram to List[Tuple]
    """
    ticker = df.columns[0]
    return [(i.strftime('%Y-%m-%d'), 
             df.loc[i].values[0], 
             ticker) for i in df.index ]


def connect():
    """
    Opens a connects with an specific
    connections
    """
    return engine.connect(DB)


def _cursor(conn:sqlite3.Connection) -> sqlite3.Cursor:
    """
    Helper-factory iniciates a cursor with foregin keys
    automatically activated
    """
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;") # allows for foreign_keys constraing
    cur.execute("PRAGMA journal_model = ON;") # <--
        #
        # allows for concurrent reads and writes. 
        # see https://www.youtube.com/watch?v=86jnwSU1F6Q
        # --
    return cur





