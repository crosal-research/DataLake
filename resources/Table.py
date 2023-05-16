##################################################
# Definie recurso para Table
# ultima modificação: 09/05/2023
##################################################

# import form system
import io, json, asyncio

# import from packages
import falcon

# import from app
from DBtransactions import table


class Table:
    """
    Classe para gerir recursos relacionados 
    as Tabelas criadas por clientes
    """
    async def on_get(self, req, resp):
        """
        Extrain informações de tables
        """
        q = req.get_param_as_list('table')
        if q[0]:
            try:
                loop = asyncio.get_running_loop()
                df = await loop.run_in_executor(None, table.query_table, q)                
                output = io.StringIO()
                df.to_csv(output)
            except:
                falcon.HTTP_405
        falcon.HTTP_200
        resp.text = output.getvalue()

    async def on_post(self, req, reps):
        """
        Creates new table
        """
        obj = req.get_media()
        if set(obj.keys()).issubset(set(['ticker', 'description', 'tickers'])):
            q = obj.get('ticker')
            d = obj.get('description')
            tickers = obj.get('tickers')

            if q and d:
                loop = asyncio.get_running_loop()
                if len(tickers) > 0:
                    def _aux_add_table():
                        table.add_table(q, d, tickers=tickers)
                    await loop.run_in_executor(None, _aux_add_table)

                else:
                    await loop.run_in_execturo(None, table.add_table, (q, d))
        else:
            resp.status = falcon.HTTP_405
            resp.text = json.dumps({'message': 'request ill formed'})


    async def on_put(self, rep, resp):
        """
        Modifies existing table
        """
        obj = req.get_media()
        if set(obj.keys()).issubset(set(['ticker', 'description', 'tickers'])):
            q = obj.get('ticker')
            d = obj.get('description')
            tickers = obj.get(tickers)
            if q and d:
                if len(tickers) > 0:
                    def _aux_add_table():
                        table.add_table(q, d, tickers=tickers)
                    await loop.run_in_executor(None, _aux_add_table)
                else:
                    await loop.run_in_execturo(None, table.add_table, (q, d))
        else:
            resp.status = falcon.HTTP_405
            resp.text = json.dumps({'message': 'request ill formed'})

    async def on_delete(self, req, resp, ticker):
        """
        Deletes existing table.
        """
        if ticker:
            loop = asyncio.get_running_loop()            
            try:
                loop.run_in_executor(None, table.delete_table, [ticker])
                falcon.HTTP_200
                resp.text = json.dumps({"table": ticker, "deletion": 'ok'})
            except:
                falcon.HTTP_405
                resp.text = json.dumps({"table": ticker, "deletion": 'fail'})
