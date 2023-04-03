##################################################
# Definie recurso Series
# ultima modificação: 31/03/2023
##################################################

# import system
import io

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
        q = req.get_media()
        info_series = [[s['series_id'], 
                        s['description'], 
                        s['survey_id']] for s in q['series']]
    
        try:
            series.add_series(info_series)
            falcon.HTTP_201
        except:
            falcon.HTTP_405

    def on_delete(self, req, resp, ticker):
        """
        Remove series da base de dados
        """
        series.delete_series(ticker.split(","))
