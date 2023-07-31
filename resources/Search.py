# import from system
import io, json

# import from packages
import falcon

# import from app
from DBtransactions import search

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
            df = search.query_search(q)
            print(df.head())
            output = io.StringIO()
            if tp == 'json':
                resp.text = json.dumps([{'rank': 1, 
                                         'ticker': df.loc[i, 'tickers'],
                                         'descripcao': df.loc[i, 'descricao']} 
                                        for i in df.index])
            else:
                df.to_csv(output)
                resp.text = output.getvalue()
