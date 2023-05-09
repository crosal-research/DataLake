##################################################
# Define recurso para Observation
# ultima modificação: 31/03/2023
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
        tp = req.get_param('type', required=False)
        resp.status = falcon.HTTP_200
        if tcks:
            utickers = [t.upper() for t in tcks]
            try:
                loop = asyncio.get_running_loop()
                df = await loop.run_in_executor(None, observation.query_obs, utickers)
            except Exception as e:
                print(e)
            output = io.StringIO()
            if tp == 'json':
                df.to_json(output)
            else:
                df.to_csv(output)
            resp.text = output.getvalue()


    async def on_post(self, req, resp):
        obj =  await req.get_media()
        
        if set(obj.keys()).issubset(set(['db', 'source', 'survey', 'tickers'])):
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
