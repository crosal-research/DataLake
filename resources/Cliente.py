##################################################
# Definie recurso Clientes
# ultima modificação: 09/05/2023
##################################################

# import from system
import json, io, asyncio

# import from packcages
import falcon

# import from app
from DBtransactions import cliente


class Cliente:
    """
    Classe para gerir recursos relacionados 
    as observacoes das series e tabelas
    """
    async def on_get(self, req, resp):
        """Extrai informacoes 
        the clientes contidos na base de dados
        """
        e = req.get_param_as_list('email')
        tp = req.get_param('type')

        if e:
            try:
                loop = asyncio.get_running_loop()
                df = await loop.run_in_executor(None,cliente.query_cliente, e)
                falcon.HTTP_2000
            except:
                falcon.HTTP_405
            output = io.StringIO()
            if tp == 'json':
                jdf = [{'nome': df.loc[s, 'nome'],
                        'email': df.loc[s, 'email'], 
                        'password': df.loc[s, 'password'], 
                        'conta': df.loc[s, 'conta']  } for s in df.index]
                resp.text = json.dumps(jdf)
            else:
                df.to_csv(output)
                resp.text = output.getvalue()

    async def on_post(self, req, resp):
        """
        Insere um novo cliente na base de dados.
        Request captura json com:
        {nome:nome, email:email, 
        senha: senha, conta_id: conta_id}
        """
        obj = await req.get_media()
        clientes = [(d['nome'], 
                     d['email'], 
                     d['senha'], 
                     d['conta_id'])]
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, cliente.add_cliente, clientes)
        falcon.HTTP_200


    async def on_delete(self, rep, resp, email):
        """
        Remove clientes da base de dados indentificado
        pela chave primária email
        """
        clientes = email
        if clientes:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, cliente.delete_clientes, [clientes])

            
