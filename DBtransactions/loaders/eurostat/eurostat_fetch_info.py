############################################################
# Module to build series informations for data extract
# form eurostat
############################################################


countries = {'DE': "Alemanha", 'FR': "FRANÇCA", 'ES': "ESPANHA", 'IT': "ITAlIA", 'EA20': "REGIÃO DO EURO"}

# RELEVANT OF THE NAMQ_GDP SURVEY #

# url = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/NAMQ_10_GDP/1.0/Q.CLV_I10.SCA.B1GQ.DE?format=csvdata&compress=false'

# B1GQ = GDP
# P3 = final expediture
# P3_S3 = final consumption expediture of general government
# P31_S14_S15 = final consumption of HH and NPISH (non-profit) 
# P516 = Gross fixed capital investiment
# P52_P53 = Changes in inventories and acquision less disposable of valuables
# P6 = exports of goos and services
# P7 = imports of goos and services

indicators = {"B1GQ": "PRODUTO INTERNO BRUTO", 
              "P3": "GASTO PRIVADO TOTAL",
              "P3_S13": "CONSUMO PUBLICO TOTAL ", 
              "P31_S14_S15": "CONSUMO DAS FAMILIAS E DE ONGS",
              "P51G": "INVESTIMENTO EM CAPITAL FIXO", 
#              "P52": "VARIACOES DE ESTOQUES", # vazia
              "P6": "EXPORTAÇÕES DE BENS E SERVIÇOS", 
              "P7": "IMPORTAÇÕES DE BENS E SERVIÇOS"}

DATA_GDP = []
for k in countries:
    for i in indicators:
        DATA_GDP.append({ "series_id": f"EUROSTAT.Q.CLV_I10.SCA.{i}.{k}", 
                          'description': f"{indicators[i]}, PIB - {countries[k]}, 2010=100",
                          'last_update': None,
                          'frequency': "TRIMESTRAL",
                          'survey_id': 'NAMQ_10_GDP'})


# RELEVANT FOR THE STS_INPR_M SURVEY

# 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/STS_INPR_M/1.0/M.PRD.B.SCA.I15.DE?format=csvdata&compress=false'

# B: manufaturing
# D: Electricity, gas, steam and air conditioning supply
# D-C

indicators = {"B": "Setor de Manufatura", 
              "D": "Setores eletrico, gas e oferta de ar condicionado", 
              "B-D": "Setores de Manufatura, eletrico, gas e oferta de ar condicionado"}

DATA_IPROD = []
for k in countries:
    for i in indicators:
        DATA_IPROD.append({"series_id": f"EUROSTAT.M.PRD.{i}.SCA.I15.{k}", 
                           'description': f"{indicators[i]} , Producao Industrial- {countries[k]}, 2010=100",
                           'last_update': None,
                           'frequency': "MENSAL",
                           'survey_id': 'STS_INPR_M'})



# RELEVANT FOR THE PRC_HICP_MIDX SURVEY

# 'HTTPS://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/PRC_HICP_MIDX/1.0/M.I05.CP00.DE?format=csvdata&compress=false'

# CP00: headline
# CP00: Food and non-alcoholic beverages
# TOT_X_NRG_FOOD: Overall index excluding energy, food, alcohol and tobacco
# SERV: services
# NRG: Energy


indicators = {'CP00': "Headline",
              'TOT_X_NRG_FOOD': "Alimentos e bebindas não-alcoolicas",
              'SERV': "serviços",
              'NRG': 'energia'}

DATA_INF = []

for k in countries:
    for i in indicators:
        DATA_INF.append({"series_id": f"EUROSTAT.M.I05.{i}.{k}", 
                         'description': f"Inflação ao Consumidor, {indicators[i]} - {countries[k]}, 2010=100",
                         'last_update': None,
                         'frequency': "MENSAL",
                         'survey_id': 'PRC_HICP_MIDX'})



# RELEVANT FOR THE STS_TRTU_M SURVEY #
# url = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/STS_TRTU_M/1.0/M.VOL_SLS.G.SCA.I21.DE?format=csvdata&compress=false'

# G = Wholesale and retail trade; repair of motor vehicles and motorcycles
# G45 = Wholesale and retail trade and repair of motor vehicles and motorcycles
# G47 = Retail trade, except of motor vehicles and motorcycles


indicators = {"G": "Vendas totais", 
              "G45": "Atacado e varejo de e vendar modorisads",
              "G47": "Varejo, exceto veiculos motorisados"}


DATA_RETAIL = []

for k in countries:
    for i in indicators:
        DATA_RETAIL.append({"series_id": f"EUROSTAT.M.VOL_SLS.{i}.SCA.I21.{k}", 
                            'description': f"Vendas, {indicators[i]} - {countries[k]}, 2010=100",
                            'last_update': None,
                            'frequency': "MENSAL",
                            'survey_id': 'STS_TRTU_M'})

# RELEVANT FOR THE  SURVEY #
# url = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/UNE_RT_M/1.0/M.NSA.TOTAL.PC_ACT.T.DE?format=csvdata&compress=false'

# imports from app
from DBtransactions.DBtypes import Series

indicators = {"PC_ACT": "Taxa de Desemprego"}
DATA_LABOR = []

for k in countries:
    for i in indicators:
        DATA_LABOR.append({"series_id": f"EUROSTAT.M.NSA.TOTAL.{i}.T.{k}", 
                           'description': f"{indicators[i]} - {countries[k]}, 2010=100",
                           'last_update': None,
                           'frequency': "MENSAL",
                           'survey_id': 'UNE_RT_M'}) 

DATA = [Series(**d) for d in DATA_GDP + DATA_IPROD + DATA_INF + DATA_RETAIL + DATA_LABOR]


def fetch_info():
    """
    Return list of series of the eurostat data source
    """
    return DATA


def _form_full_ticker(ticker):
    du = {'NAMQ_10_GDP': "NAMQ_10_GDP/1.0",
          'STS_INPR_M': "STS_INPR_M/1.0",
          'PRC_HICP_MIDX': "PRC_HICP_MIDX/1.0",
          'STS_TRTU_M': "STS_TRTU_M/1.0",
          'UNE_RT_M': "UNE_RT_M/1.0"}

    info = [d.survey_id for d in DATA if d.series_id == ticker]
    return f"EUROSTAT.{info[0]}/1.0/{ticker.split('EUROSTAT.')[1]}" 
