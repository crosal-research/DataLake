##################################################
# Definie recurso para Table
# ultima modificação: 10/08/2024
##################################################

# import form system
import io, json, asyncio

# import from packages
import falcon
import pandas as pd
import pendulum

# import from app
from DBtransactions.data import add_data_series
from DBtransactions.DBtypes import Series


class DataSeries:
    """
    Classe para gerir recursos relacionados 
    às observações de series enviadas pelos
    administradores
    """
    async def on_post(self, req, resp):
        """
        Insere dados na base de dados a partir dos dados
        enviados no formato csv (separador ";")
        check: https://www.geeksforgeeks.org/python-falcon-get-post-data/
        """
        csv = await req.bounded_stream.read()
        try:
            df = pd.read_csv(io.BytesIO(csv), sep=";", decimal=",").dropna(axis=1, how='all')
            df.set_index(['series_id'], inplace=True)

            lx = [Series(**{'series_id': s, 
                                     'description': df.loc[s, 'description'],
                                     'last_update': None, 
                                     'survey_id': df.loc[s, 'survey_id'], 
                                     'frequency': df.loc[s, 'frequency']}) for s in df.index]
            await add_data_series(lx)
        except Exception as e:
            print(e)

        
