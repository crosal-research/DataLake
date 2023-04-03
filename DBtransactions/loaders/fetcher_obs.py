# import from system
from typing import List


# import from packages
import pandas as pd


# import from app
from DBtransactions.loaders.fred import fred_obs


def fetch(tickers:[List[str]]) -> List[pd.DataFrame]:
    """
    Funcao que agrega of fetchers the todas as fontes.
    Precisa organizar as lista de data frame de acorod
    com a ordem em que são listadas no input
    """
    return fred_obs.fetch(tickers)
