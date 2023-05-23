/*
* Insert tables
*/

-- Principais indicadores de atividades mensal
BEGIN TRANSACTION;
INSERT INTO Utable (utable_id, description, proprietario)
    VALUES ('TBL.ATIVIDADE_BRM', 
            'PRINCIPAIS INDICADORES MENSAIS DE ATIVIDADES BRSILEIRA COM AJUSTE SAZONAL', 
            'TI');

INSERT INTO series_utable (utable_id, series_id)
    VALUES 
    ('TBL.ATIVIDADE_BRM', 'BCB.24364'), --IBC-BR
    ('TBL.ATIVIDADE_BRM', 'IBGE.8881/V/7170/C11046/56736'), -- varejo ampliado
    ('TBL.ATIVIDADE_BRM', 'IBGE.8888/V/12607/C544/129314'), -- PIM
    ('TBL.ATIVIDADE_BRM', 'IBGE.8688/V/7168/C11046/56726/C12355/107071'); -- serviços
COMMIT;

-- Indicadores de produção industrial
BEGIN TRANSACTION;
INSERT INTO Utable (utable_id, description, proprietario)
    VALUES ('TBL.PIMCE_SA', 
            'PRODUCAO INDUSTRIAL POR GRANDES CATEGORIAS ECONOMIAS COM AJUSTE SAZONAL', 
            'TI');

INSERT INTO series_utable (utable_id, series_id)
    VALUES 
    ('TBL.PIMCE_SA', 'IBGE.8888/V/12607/C544/129314'), -- PIM Total
    ('TBL.PIMCE_SA', 'IBGE.8887/V/12607/C543/129278'), -- PIM Capital
    ('TBL.PIMCE_SA', 'IBGE.8887/V/12607/C543/129283'), -- PIM Intermediarios
    ('TBL.PIMCE_SA', 'IBGE.8887/V/12607/C543/129300'), -- PIM Consumo
    ('TBL.PIMCE_SA', 'IBGE.8887/V/12607/C543/129301'), -- PIM Consumo duravies
    ('TBL.PIMCE_SA', 'IBGE.8887/V/12607/C543/129305'); -- PIM Não duravies
COMMIT;


-- Indicadores de varejo ampliado
BEGIN TRANSACTION;
INSERT INTO Utable (utable_id, description, proprietario)
    VALUES ('TBL.PMC_SA', 
            'PESQUISA DE VAREJO AMPLIADO POR COMPONENTES COM AJUSTE SAZONAL', 
            'TI');

INSERT INTO series_utable (utable_id, series_id)
    VALUES 
    ('TBL.PMC_SA', 'IBGE.8881/V/7170/C11046/56736'), -- PMC Total
    ('TBL.PMC_SA', 'IBGE.8883/V/7170/C11046/56736/C85/90671'), -- PMC combustiveis
    ('TBL.PMC_SA', 'IBGE.8883/V/7170/C11046/56736/C85/90672'), -- PMC supermerdados & alimientos
    ('TBL.PMC_SA', 'IBGE.8883/V/7170/C11046/56736/C85/103154'), -- PMC supermerdados
    ('TBL.PMC_SA', 'IBGE.8883/V/7170/C11046/56736/C85/90673'), -- PMC vestuarios
    ('TBL.PMC_SA', 'IBGE.8883/V/7170/C11046/56736/C85/2759'), -- PMC Moveis & eletrodomesticos
    ('TBL.PMC_SA', 'IBGE.8883/V/7170/C11046/56736/C85/31555'), -- PMC Moveis
    ('TBL.PMC_SA', 'IBGE.8883/V/7170/C11046/56736/C85/31556'), -- PMC eletrodomesticos
    ('TBL.PMC_SA', 'IBGE.8883/V/7170/C11046/56736/C85/103155'), -- PMC Farmaceuticos
    ('TBL.PMC_SA', 'IBGE.8883/V/7170/C11046/56736/C85/103156'), -- PMC Papelaria
    ('TBL.PMC_SA', 'IBGE.8883/V/7170/C11046/56736/C85/103157'), -- PMC Equicapmentos & escritorio
    ('TBL.PMC_SA', 'IBGE.8883/V/7170/C11046/56736/C85/103158'), -- PMC Uso pessoal
    ('TBL.PMC_SA', 'IBGE.8883/V/7170/C11046/56736/C85/103159'), -- PMC Motociclecas e peças
    ('TBL.PMC_SA', 'IBGE.8884/V/7170/C11046/56738'); -- PMC Motociclecas e peças
COMMIT;

-- 
