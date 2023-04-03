##################################################
# Definie recurso para Table
# ultima modificação: 31/03/2023
##################################################


# import form system
import io, json

# import from packages
import falcon

# import from app
from DBtransactions import table


class Table:
    """
    Classe para gerir recursos relacionados 
    as Tabelas criadas por clientes
    """
    def on_get(self, req, resp):
        """
        Extrain informações de tables
        """
        q = req.get_param_as_list('table')
        if q[0]:
            try:
                df = table.query_table(q)
                output = io.StringIO()
                df.to_csv(output)
            except:
                falcon.HTTP_405
        falcon.HTTP_200
        resp.text = output.getvalue()

    def on_post(self, req, reps):
        """
        Creates new table
        """
        q = req.get_param('ticker')
        d = req.get_param('description')
        tickers = req.get_param_as_list(tickers)

        if q and d:
            if len(tickers) > 0:
                table.add_table(q, d, tickers=tickers)
            else:
                table.add_table(q, d)

    def on_put(self, rep, resp):
        """
        Modifies existing table
        """
        q = req.get_param('ticker')
        d = req.get_param('description')
        tickers = req.get_param_as_list(tickers)

        if q and d:
            if len(tickers) > 0:
                table.add_table(q, d, tickers=tickers)
            else:
                table.add_table(q, d)

    def on_delete(self, req, resp, ticker):
        """
        Deletes existing table.
        """
        if ticker:
            try:
                table.delete_table([ticker])
                falcon.HTTP_200
                resp.text = json.dumps({"table": ticker, "deletion": 'ok'})
            except:
                falcon.HTTP_405
                resp.text = json.dumps({"table": ticker, "deletion": 'fail'})
