##################################################
# Definie recurso Series
# ultima modificação: 31/03/2023
##################################################

# import system
import io, json

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
    def on_get(self, req, resp):
        """ Retorna informacoes de series
        """
        q = req.get_param_as_list('series', required=False)
        tp = req.get_param('type', required=False)
        resp.status = falcon.HTTP_200
        if q:
            df = series.query_series(q)
            output = io.StringIO()
            if tp == 'json':
                df.to_json(output)
            else:
                df.to_csv(output)
            resp.text = output.getvalue()

    def on_post(self, req, resp):
        """
        Insere serie na base de dados
        """
        query = req.get_media()
        args = {k:query[k] if k in query else None for 
                k in ('source', 'survey', 'tickers')}

        series.add_series(**args)
        try:
            falcon.HTTP_201
            resp.text = json.dumps({"status": True, "message": "Data upserted in the DB"})
        except:
            falcon.HTTP_405
            resp.text = json.dumps({"status": False, "message": "Data insertion failed"})

    def on_delete(self, req, resp, ticker):
        """
        Remove series da base de dados
        """
        series.delete_series(ticker.split(","))
