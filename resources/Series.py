##################################################
# Define recurso Series
# ultima modificação: 08/06/2024
##################################################

# import system
import io, json, asyncio

# import from packages
import falcon

# import from app
from DBtransactions import series

# Sereis
class Series:
    """
    Classe para gerir recursos relacionados 
    a pesquisa de series na base de dados
    """
    async def on_get(self, req, resp):
        """ Retorna informacoes de series
        """
        q = req.get_param_as_list('tickers', required=False)
        tp = req.get_param('type', required=False)
        resp.status = falcon.HTTP_200
        if q:
            loop = asyncio.get_running_loop()
            df = await loop.run_in_executor(None, series.query_series,q)
            if tp == 'json':
                resp.media = [{'ticker': i, 
                                         'descricao': df.loc[i, 'Descricao'], 
                                         'last_update': str(df.loc[i, 'last_update']), 
                                         'fonte': df.loc[i, 'Fonte']}
                                        for i in df.index ]
            else:
                output = io.StringIO()
                df.loc[q].to_csv(output, sep=";")
                resp.text = output.getvalue()

    async def on_post(self, req, resp):
        """
        Insere serie na base de dados
        """
        query = await req.get_media()
        args = {k:query[k] if k in query else None for 
                k in ('source', 'survey', 'tickers')}
        loop = asyncio.get_running_loop()

        def _aux_add_series():
            """
            Helper function to run add_series
            within the event loop
            """
            series.add_series(**args)

        try:
            await loop.run_in_executor(None, _aux_add_series)
            resp.text = json.dumps({"status": True, "message": "Data upserted in the DB"})
            falcon.HTTP_201
        except:
            falcon.HTTP_405
            resp.text = json.dumps({"status": False, "message": "Data insertion failed"})

    async def on_delete(self, req, resp, ticker):
        """
        Remove series da base de dados
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None,series.delete_series,ticker.split(","))
