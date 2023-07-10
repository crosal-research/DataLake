# import from system
import json, io, asyncio

# import from packcages
import falcon

# import from app
from DBtransactions import conta


class Conta:
    """
    Classe para gerir recursos relacionados 
    as observacoes das series e tabelas
    """
    async def on_get(self, req, resp):
        """Handles GET requests"""
        q = req.get_param_as_list('account', required=False)
        tp = req.get_param('type', required=False)
        resp.status = falcon.HTTP_200
        loop = asyncio.get_running_loop()
        df = await loop.run_in_executor(None, conta.query_conta, q)
        output = io.StringIO()

        if tp == 'json':
            jdf = [{'conta_id': df.loc[s, 'conta_id'], 
                    'nome': df.loc[s, 'nome']  } for s in df.index]
            resp.text = json.dumps(jdf)
                
        else:
            df.to_csv(output)
            resp.text = output.getvalue()


    async def on_post(self, req, resp):
        """to be implemented"""
        pass

