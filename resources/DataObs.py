##################################################
# Definie recurso para Table
# ultima modificação: 09/05/2023
##################################################

# import form system
import io, json, asyncio

# import from packages
import falcon
import pandas as pd
import pendulum

# import from app
from DBtransactions.data import add_data_obs
from DBtransactions.DBtypes import Observation


class DataObs:
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
            df.columns = [c.replace(" ", "") for c in df.columns]
            df.set_index(['data'], inplace=True)
            df.index = [pendulum.from_format(d, "DD/MM/YYYY").to_date_string() for d in df.index]
            lx = []
            for c in df.columns:
                lx.append([Observation(**{'dat': dat, 
                            'valor': df.loc[dat, c], 
                            'series_id': c}) for dat in df.index])
            await add_data_obs(lx)
            resp.status = falcon.HTTP_200
        except Exception as e:
            print(e)
            resp.status = falcon.HTTP_405
        
