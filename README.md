# DataLake

Base de Dados de series econômicas extraídas de várias fontes. O
usuário interagem com as śerias através de um api. Desenvolvimento de
interfaces gráficas com camada adicional pode facilitar esse
interação.

Os principais canais de interação são:

  * Pesquisa por séries, que são representadas por tickers.
  * Descrição das séries (ou de seus tickers) através de uma função
    específica.
  * Consumo de séries em através de suas observações data/valor.


# Infrastrutura

- Linux 22.04
- python 3.11 >=
- sqlite3 3.42 >=
- ngnix 1.26.0


## Séries ##

As series são definidas pelas seguintes entradas:
  * series_id: o ticker da série.
  * description: descrição da seŕies.
  * frequency: frequencia da seŕies.
  * last_update: última vez que a seŕies foi atualizada.
  * first: primeiro observação temporal disponível da séire.
  * last: última observação da disponível da série disponível.


# Principais funções

Para o usuário final, as principais funções são, através do verbo _get_, as seguintes:
  * __Baixar série__: raiz_url/observations?series=_ticker_&...&series=titcker_&ini=_DD/MM/YYYY__&type=json
  * __Baixar metadado de série__: raiz_url/series?series=_ticker_&....&series&_ticker_&type=json
  * __Procura__: raiz_url/search?words=_palavras_&type=json
  
O formato dos resultados se dão em _json_ ou em _csv_ (default). No
caso das funções de procura e metadados (descrição), o formato _csv_ é
separado por ";", pois os textos contém ",".
	
