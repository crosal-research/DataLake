# import from system
import json, io, asyncio

# import from packcages
import falcon

# import from app
from DBtransactions import survey


class Survey:
    """
    Classe para gerir recursos relacionados 
    as observacoes das series e tabelas
    """
    async def on_get(self, req, resp):
        """Handles GET requests"""
        q = req.get_param_as_list('survey', required=False)
        tp = req.get_param('type', required=False)
        resp.status = falcon.HTTP_200
        loop = asyncio.get_running_loop()
        df = await loop.run_in_executor(None, survey.query_survey, q)
        output = io.StringIO()

        if tp == 'json':
            jdf = [{'survey_id': df.loc[s, 'survey_id'], 
                    'description': df.loc[s, 'description'], 
                    'source': df.loc[s, 'source_id'] } for s in df.index]
            resp.text = json.dumps(jdf)
                
        else:
            df.to_csv(output)
            resp.text = output.getvalue()


    async def on_post(self, req, resp):
        """
        Still in need to be implemented
        Insere survey na base de dados
        """
        query = await req.get_media()
        args = {k:query[k] if k in query else None for 
                k in ('source', 'survey', 'tickers')}

        loop = asyncio.get_running_loop()

        def _aux_add_series():
            """
            Helper function to run add_surveys
            within the event loop
            """
            series.add_series(**query)

        try:
            falcon.HTTP_201
            await loop.run_in_executor(None, _aux_add_series)
            resp.text = json.dumps({"status": True, "message": "Data upserted in the DB"})
        except:
            falcon.HTTP_405
            resp.text = json.dumps({"status": False, "message": "Data insertion failed"})


    async def on_delete(self, req, resp, ticker):
        """
        Remove series da base de dados
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None,series.delete_series,ticker.split(","))
