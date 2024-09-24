# import from system
from typing import List, Dict

# import from app
from DBtransactions.DBtypes import Series


DATA = [
    #CPIa
    {
    "series_id": "OUKS.d7bt_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), TODOS OS  ITEMS, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""},
    {
    "series_id": "OUKS.dkc6_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR, NÙCLEO POR EXCLUSÃO DE CIGARROS, BEBIDAS ALCOLICAS, ENERGIA E ALIMENTOS, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""},
    {
    "series_id": "OUKS.d7bu_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), ALIMENTOS E BEBIDAS NÃO ALCOOLICAS, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""}, 
    {
    "series_id": "OUKS.d7bv_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), BEBIDAS ALCOOLICAS E CIGARROS, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""}, 
    {
    "series_id": "OUKS.d7bw_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), VESTUARIO, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""}, 
    {
    "series_id": "OUKS.d7bx_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), MORADIA E SERVIÇOS DE MORADIA, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""}, 
    {
    "series_id": "OUKS.d7by_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), ARTIGOS DE RESIDENCIA, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""}, 
    {
    "series_id": "OUKS.d7bz_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), SAUDE, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""}, 
    {
    "series_id": "OUKS.d7c2_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), TRANSPORTE, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""}, 
    {
    "series_id": "OUKS.d7c3_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), COMUNICAÇÃO, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""
    } ,
    {
    "series_id": "OUKS.d7c4_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), RECREACAO E CULTURA, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""
    },
    {
    "series_id": "OUKS.d7c5_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), EDUCAÇAO, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""
    },
    {
    "series_id": "OUKS.d7c6_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), RESTAURANTES E HOTEIS, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""
    },
    {
    "series_id": "OUKS.D7F4_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), TODOS OS BENS, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""
    },
    {
    "series_id": "OUKS.d7f5_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), TODOS OS SERVIÇOS, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""
    },
    {
    "series_id": "OUKS.dk9t_mm23",
    "description": "INDICE DE PREÇOS AO CONSUMIDOR (CPI), ENERGIA, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_CPI",
    "last_update": ""
    },

    # Retail
    {
    "series_id": "OUKS.J5EK_DRSI",
        "description": "VOLUME DE VENDAS TOTAL INCLUSOS AUTOMOVIES A COMBUSTIVEL COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_RSI",
    "last_update": ""
    },
    {
    "series_id": "OUKS.J467_DRSI",
        "description": "VOLUME DE VENDAS TOTAL EXCLUSOS AUTOMOVIES A COMBUSTIVEL COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_RSI",
    "last_update": ""
    },
    {
    "series_id": "OUKS.EAPT_DRSI",
        "description": "VOLUME DE VENDAS PREDOMINANTEMETE ESTABELECIMENTOS DE ALIMENTOS COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_RSI",
    "last_update": ""
    },
    {
    "series_id": "OUKS.EAPV_DRSI",
        "description": "VOLUME DE VENDAS PREDOMINANTEMETE DE ESTABELECIMENTOS DE NAO ALIMENTOS COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_RSI",
    "last_update": ""
    },
    {
    "series_id": "OUKS.EAPU_DRSI",
        "description": "VOLUME DE VENDAS PREDOMINANTEMETE DE ESTABELECIMENTOS NAO ESPECIALIZADOS COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_RSI",
    "last_update": ""
    },
    {
    "series_id": "OUKS.EAPX_DRSI",
        "description": "VOLUME DE VENDAS EM LOJAS DE VESTUARIO COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_RSI",
    "last_update": ""
    },
    {
    "series_id": "OUKS.EAPY_DRSI",
        "description": "VOLUME DE VENDAS EM LOJAS DE ITENS DO LAR COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_RSI",
    "last_update": ""
    },
    {
    "series_id": "OUKS.EAPW_DRSI",
        "description": "VOLUME DE VENDAS EM LOJAS DEMAIS ITEMS COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_RSI",
    "last_update": ""
    },
    {
    "series_id": "OUKS.J5DZ_DRSI",
        "description": "VOLUME DE VENDAS EM ESTABELECIMOS NÃO FÍSICOS COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_RSI",
    "last_update": ""
    },
    # producao industrial
    {
    "series_id": "OUKS.K222_DIOP",
    "description": "VOLUME DA PRODUCAO INDUSTRIAL COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_DIOP",
    "last_update": ""
    },
    {
    "series_id": "OUKS.K224_DIOP",
    "description": "VOLUME DA PRODUCAO DAS INDUSTRIAS DE MINERACAO E EXTRATIVA COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_DIOP",
    "last_update": ""
    },
    {
    "series_id": "OUKS.K22A_DIOP",
    "description": "VOLUME DA PRODUCAO DA INDUSTRIA MANUFATUREIRA COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_DIOP",
    "last_update": ""
    },
    {
    "series_id": "OUKS.K248_DIOP",
    "description": "VOLUME DA PRODUCAO DAS INDUSTRIAS DE ELETRICIDADE, GAS, VAPOR E AR CONDICIONADO COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_DIOP",
    "last_update": ""
    },
    {
    "series_id": "OUKS.K24C_DIOP",
    "description": "VOLUME DA PRODUCAO DA INDUSTRIA DE SANEAMENTO COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_DIOP",
    "last_update": ""
    },
    {
    "series_id": "OUKS.K226_DIOP",
    "description": "VOLUME DA PRODUCAO DAS INDUSTRIA DE PETROLEO E GAS COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_DIOP",
    "last_update": ""
    },
    {
    "series_id": "OUKS.K24Q_DIOP",
    "description": "VOLUME DA PRODUCAO DE BENS DURAVEIS COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_DIOP",
    "last_update": ""
    },
    {
    "series_id": "OUKS.K24R_DIOP",
    "description": "VOLUME DA PRODUCAO DE BENS NAO-DURAVEIS COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_DIOP",
    "last_update": ""
    },
    {
    "series_id": "OUKS.K24S_DIOP",
    "description": "VOLUME DA PRODUCAO DE BENS DE CAPITAL COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_DIOP",
    "last_update": ""
    },
    {
    "series_id": "OUKS.K24O_DIOP",
    "description": "VOLUME DA PRODUCAO DE BENS DE INTERMEDIARIOS COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_DIOP",
    "last_update": ""
    },
    {
    "series_id": "OUKS.K24T_DIOP",
    "description": "VOLUME DA PRODUCAO DE ENERGIA COM AJUSTE SAZONAL, REINO UNIDO",
    "frequency": "MENSAL",
    "survey_id": "OUKS_DIOP",
    "last_update": ""
    },

    # monthly activity GDP
    {
    "series_id": "OUKS.ECY2_MGDP",
    "description": "PIB MENSAL DO REINO UNIDO COM AJUSTE SAZONAL, NÚMERO ÍNDICE",
    "frequency": "MENSAL",
    "survey_id": "OUKS_MGDP",
    "last_update": ""
    },
    {
    "series_id": "OUKS.ECY3_MGDP",
    "description": "PIB MENSAL DO SETOR AGRICOLA DO REINO UNICO COM AJUSTE SAZONAL",
    "frequency": "MENSAL",
    "survey_id": "OUKS_MGDP",
    "last_update": ""
    },
    {
    "series_id": "OUKS.ECY4_MGDP",
    "description": "PIB MENSAL DO SETOR INDUSTRIAL DO REINO UNICO COM AJUSTE SAZONAL",
    "frequency": "MENSAL",
    "survey_id": "OUKS_MGDP",
    "last_update": ""
    },
    {
    "series_id": "OUKS.ECY9_MGDP",
    "description": "PIB MENSAL DO SETOR DE CONSTRUCAO DO REINO UNICO COM AJUSTE SAZONAL",
    "frequency": "MENSAL",
    "survey_id": "OUKS_MGDP",
    "last_update": ""
    },
    {
    "series_id": "OUKS.ECYC_MGDP",
    "description": "PIB MENSAL DO SETOR DE SERVICOS DO REINO UNICO COM AJUSTE SAZONAL",
    "frequency": "MENSAL",
    "survey_id": "OUKS_MGDP",
    "last_update": ""
    }
]


def fetch_info(data:Dict[str, str]):
    return [Series(**d) for d in DATA]
