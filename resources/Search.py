# import from packages
import falcon

# import from app
from DBtransactions import table

class Search:
    """
    Classe para gerir recursos relacionados 
    a pesquisa de series na base de dados
    """
    async def on_get(self, req, resp):
        """Handles GET requests"""
        q = req.get_param('words', required=False)
        tp = req.get_param('type', required=False)
        resp.status = falcon.HTTP_200
        if q:
            df = table.query_search(q)
            output = io.StringIO()
            if tp == 'json':
                df.to_json(output)
            else:
                df.to_csv(output)
            resp.text = output.getvalue()
