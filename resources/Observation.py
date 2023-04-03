##################################################
# Definie recurso para Observation
# ultima modificação: 31/03/2023
##################################################


# import from system
import json, io

# import from packcages
import falcon

# import from app
from DBtransactions import observation


class Observations:
    """
    Classe para gerir recursos relacionados 
    as observacoes das series e tabelas
    """
    def on_get(self, req, resp):
        """Handles GET requests"""
        tcks = req.get_param_as_list('ticker', required=False)
        tp = req.get_param('type', required=False)
        resp.status = falcon.HTTP_200
        if tcks:
            df = observation.query_obs([t.upper() for t in tcks])
            output = io.StringIO()
            if tp == 'json':
                df.to_json(output)
            else:
                df.to_csv(output)
            resp.text = output.getvalue()


    def on_post(self, req, resp):
        tcks= req.media.get('tickers')
        tickers = tcks if isinstance(tcks, list) else [tcks]
        survey = req.media.get('survey')
        source = req.media.get('source')
        table = req.media.get('table')
        db = req.media.get('db')
        
        if tickers[0]:
            d = {'tickers': tickers}
        elif survey:
            d = {'survey': survey}
        elif source:
            d = {'source': source}
        elif table:
            d = {'table': table}
        elif db:
            d = {'db': db}
        else:
            resp.status = falcon.HTTP_405
            resp.text = json.dumps({'message': 'request ill formed'})    
            return None

        try:
            observation.add_observations(**d)
            resp.status = falcon.HTTP_201
            d['upsert'] = 'ok'
            resp.text = json.dumps(d)
        except:
            resp.status = falcon.HTTP_405
            d['upsert'] = 'Fail'
            resp.text = json.dumps(d)    


