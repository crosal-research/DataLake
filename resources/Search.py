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
        """
        retrieves series related to a search string
        issued by user. Words is the string and type 
        is the return's format: either csv or json
        """
        q = req.get_param('words', required=False)
        tp = req.get_param('type', required=False)
        resp.status = falcon.HTTP_200
        if q:
            df = search.query_search(q)
            try:
                if tp == 'json':
                    result = [{'popularidade': int(df.loc[i, 'popularidade']), 
                               'ticker': df.loc[i, 'tickers'],
                               'descricao': df.loc[i, 'descricao']} 
                              for i in df.index]
                    resp.media = result
                else:
                    output = io.StringIO()
                    df.to_csv(output, sep=";")
                    resp.text = output.getvalue()
                    resp.status = falcon.HTTP_200
            except _ as e:
                print(e)
                resp.status = falco.HTTP_500
