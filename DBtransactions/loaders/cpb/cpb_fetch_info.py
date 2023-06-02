############################################################
# Ingestiong of series from the cpl database
# url: https://www.cpb.nl/en/worldtrademonitor
#############################################################

# import from system
from typing import List, Tuple

# imports from app
from DBtransactions.DBtypes import Series

INFO: List[Tuple] = [
    ("CPB.IPZ_W1_QNMI_SP", 
         "Producao industrial mundial com ajuste sazonal, normalizada pela peso da producao dos blocos economicos", 
         "CPB_PROD", "Mensal"),
    ("CPB.TGZ_W1_QNMI_SN", "Fluxo de comercio da economia mundial com a ajuste sazonal", "CPB_TRADE", "Mensal"),
    ("CPB.MGZ_W1_QNMI_SN", "Importacao pela economia mundial com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.MGZ_I1_QNMI_SN", "Importacao pelas Economia Avancadas com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.MGZ_E6_QNMI_SN", "Importacao pelos paises da regiao do Euro com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.MGZ_US_QNMI_SN", "Importacao pelos os Estados Unidos com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.MGZ_GB_QNMI_SN", "Importacao pelo o Reunio Unidos com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.MGZ_JP_QNMI_SN", "Importacao pelo o Japao com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.MGZ_A3_QNMI_SN", "Importacao pelo Economias avancadas da asis (ex-japao) com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.MGZ_R2_QNMI_SN", "Importacao por outras economias avancadas (ex- E.U.A, E.U., Japao e Asia) com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.MGZ_D1_QNMI_SN", "Importacao pelas economias emergentes com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.MGZ_CN_QNMI_SN", "Importacao pela China com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.MGZ_A5_QNMI_SN", "Importacao pelos paises asiáticos (ex-China) com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.MGZ_T1_QNMI_SN", "Importacao pelos o paises do leste europeu com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.MGZ_F3_QNMI_SN", "Importacao pelos paises da america latina com ajuste sazonal","CPB_TRADE", "Mensal"),

    ("CPB.XGZ_W1_QNMI_SN", "Exportacao pela economia mundial com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.XGZ_I1_QNMI_SN", "Exportacao pelas Economia Avancadas com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.XGZ_E6_QNMI_SN", "Exportacao pelos paises da regiao do Euro com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.XGZ_US_QNMI_SN", "Exportacao pelos os Estados Unidos com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.XGZ_GB_QNMI_SN", "Exportacao pelo o Reunio Unidos com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.XGZ_JP_QNMI_SN", "Exportacao pelo o Japao com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.XGZ_A3_QNMI_SN", "Exportacao pelo Economias avancadas da asis (ex-japao) com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.XGZ_R2_QNMI_SN", "Exportacao por outras economias avancadas (ex- E.U.A, E.U., Japao e Asia) com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.XGZ_D1_QNMI_SN", "Exportacao pelas economias emergentes com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.XGZ_CN_QNMI_SN", "Exportacao pela China com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.XGZ_A5_QNMI_SN", "Exportacao pelos paises asiáticos (ex-China) com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.XGZ_T1_QNMI_SN", "Exportacao pelos o paises do leste europeu com ajuste sazonal","CPB_TRADE", "Mensal"),
    ("CPB.XGZ_F3_QNMI_SN", "Exportacao pelos paises da america latina com ajuste sazonal","CPB_TRADE", "Mensal")]


def fetch_info(info: List[Tuple]) -> List[Series]:
    return [Series(**{
        'series_id': srs[0]  ,
        'description': srs[1],
        'survey_id': srs[2],
        'frequency': srs[3]
    }) for srs in info]
