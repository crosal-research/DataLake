##################################################
# Define recurso para Observation
# ultima modificação: 25/05/2023
##################################################

# import from system
import json, io, asyncio

# import from packcages
import falcon

# import from app
from DBtransactions import observation


class Observations:
    """
    Classe para gerir recursos relacionados 
    as observacoes das series e tabelas
    """
    async def on_get(self, req, resp):
        """Handles GET requests"""
        tcks = req.get_param_as_list('ticker', required=False)
        tbl = req.get_param('table', required=False)
        limit = req.get_param('limit', required=False)
        tp = req.get_param('type', required=False)
        resp.status = falcon.HTTP_200
        loop = asyncio.get_running_loop()
        
        if tcks:
            utickers = [t.upper() for t in tcks]
        else:
            table = tbl.upper()
        def _aux_query_obs():
            return observation.query_obs(tickers= utickers if tcks else None, 
                                         table= table if tbl else None,
                                         limit= limit if limit else None)
                                         
        try:
            df = await loop.run_in_executor(None, _aux_query_obs)
        except Exception as e:
            print(e)
        if tp == 'json':
            index = df.index
            result = [{'ticker': c,
                       'observations': [{'date': i, 'value': df.loc[i, c]} for i in index]} for c in df.columns]
            resp.text = json.dumps(result)
        else:
            output = io.StringIO()
            df.to_csv(output)
            resp.text = output.getvalue()


    async def on_post(self, req, resp):
        obj =  await req.get_media()
        if set(obj.keys()).issubset(set(['db', 'source', 'survey', 'tickers', 'table'])):
            loop = asyncio.get_running_loop()
            
            def _aux_add_obs():
                """
                Help function to add observation
                using run_in_executor function
                """
                observation.add_obs(**obj)

            df = await loop.run_in_executor(None, _aux_add_obs)
            resp.status = falcon.HTTP_201
            obj['upsert'] = 'ok'
            resp.text = json.dumps(obj)
        else:
            resp.status = falcon.HTTP_405
            resp.text = json.dumps({'message': 'request ill formed'})    
            return None
