/*
Ativo support para foreign key
ver: https://www.sqlite.org/foreignkeys.html
*/

PRAGMA foreign_keys = ON;
PRAGMA jornal_mode = WAL;

/*
Inserts de dados
*/

--Insert Conta
BEGIN TRANSACTION;
INSERT INTO Conta (conta_id, nome) 
       VALUES ('TI', 'TERRA INVESTIMENTOS');
INSERT INTO Conta (conta_id, nome) 
       VALUES ('GUEST', 'GUEST');       
COMMIT;

--Insert Cliente
INSERT INTO Cliente (roleType, email, conta_id, senha)
       VALUES ('ADMIN', 'JOAO.ROSAL@TERRAINVESTIMENTOS.COM.BR', 'TI', '123');

--Insert Sources
BEGIN TRANSACTION;
INSERT INTO Source (source_id, full_name)
       VALUES ('BCB', 'BANCO CENTRAL DO BRASIL');
INSERT INTO Source (source_id, full_name)
       VALUES ('BCB_EXP', 'EXPECTATIVAS DO BANCO CENTRAL DO BRASIL');       
INSERT INTO Source (source_id, full_name)
       VALUES ('IBGE', 'INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATISTICA');	
INSERT INTO Source (source_id, full_name)
       VALUES ('FRED', 'Federal Reserve of Saint Louis');
INSERT INTO Source (source_id, full_name)
       VALUES ('BLS', 'BUREAU OF LABOR STATISTICS');       
INSERT INTO Source (source_id, full_name)
       VALUES ('IPEA', 'INSTITUTO DE PESQUISA ECONOMICA APLICADA');
INSERT INTO Source (source_id, full_name)
       VALUES ('IMF', 'FUNDO MONETARIO INTERNACIONAL');
INSERT INTO Source (source_id, full_name)
       VALUES ('BIS', 'BANCO INTERNACIONAL DE COMPENSACOES');
INSERT INTO Source (source_id, full_name)
       VALUES ('ONS', 'OPERADOR NACIONAL DO SISTEMA ELETRICO');                     
INSERT INTO Source (source_id, full_name)
       VALUES ('BEA', 'BUREAU OF ECONOMICS ANALYSIS');
INSERT INTO Source (source_id, full_name)
       VALUES ('CEPEA', 'CENTRO DE ESTUDOS AVANCADOS EM ECONOMIA APLICADA');
INSERT INTO Source (source_id, full_name)
       VALUES ('CPB', 'INSTITUTO DE ESTATISTICA DA HOLANDA');
INSERT INTO Source (source_id, full_name) VALUES ('NBSC', 'NATIONAL BUREAU OF STATISTICS OF CHINA');
COMMIT;	      


--Insert Surveys
BEGIN TRANSACTION;

-- IBGE 
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('IBGE_PIM', 'PESQUISA INDUSTRIAL MENSAL, Brasil', 'IBGE');
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('IBGE_PMC', 'PESQUISA MENSAL DE COMERCIO, BRASIL', 'IBGE');
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('IBGE_PMS', 'PESQUISA MENSAL DE SERVICO, BRASIL', 'IBGE');      
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('IBGE_CN', 'CONTAS NACIONAIS TRIMESTRAIS, BRASIL', 'IBGE');
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('IBGE_IPCA', 'Indice de Preco ao Consumidor amplo, Brasil', 'IBGE');
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('IBGE_IPCA15', 'Indice de Preco ao Consumidor amplo-15', 'IBGE');
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('IBGE_PNAD', 'Pesquisa Nacional de Amostra Domiliar Continuada, Brasil', 'IBGE');                              

-- FRED ---
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('FRED_ECON', 'DADOS ECONÔMICOS DISPONIBILIZADOS PELO FRED', 'FRED');
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('FRED_FIN', 'DADOS FINANCEIROS DISPONIBILIZADOS PELO FRED', 'FRED');

-- IPEA --
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('IPEA', 'DADOS GENERICOS DISPONIBILIZADOS PELO IPEA', 'IPEA');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('IPEA_ECON', 'DADOS ECONOMICOS DISPONIBILIZADOS PELO IPEA', 'IPEA');   
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('IPEA_FIN', 'DADOS FINANCEIROS DISPONIBILIZADOS PELO IPEA', 'IPEA');

-- BLS --
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BLS_CPI', 'DADOS DE INFLACAO AO CONSUMIDOR DOS E.U.A.', 'BLS');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BLS_LN', 'DADOS DE FORCA DE TRABALHO DOS E.U.A. DO CURRENT POLUTAION SURVEY (SIC)', 'BLS');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BLS_CE', 'DADOS DE EMPREGO, HORAS TRABALHADAS E GANHOS DO E.U.A. DO CURRENT POPULATION SURVEY', 'BLS');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('IMF_PCPS', 'PRECO DE COMMODITIES PRIMARIAS', 'IMF');

--BIS --
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BIS_WS_EER_M', 'TAXAS DE CAMBIOS REAL EFETIVOS', 'BIS');

-- BCB --
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BCB_ECON', 'SERIES ECONOMICAS DO BANCO CENTRAL DO BRASIL', 'BCB');                                                INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BCB_MERCADO-ABERTO', 'SERIES FINANCEIRAS DISPONIBILIZADAS PELO BANCO CENTRAL DO BRASIL', 'BCB');                 INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BCB_CREDITO', 'SERIES DO MERCADO DE CREDITO E POLITICA MONETARIA DISPONIBILIZADAS PELO BANCO CENTRAL DO BRASIL', 'BCB');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BCB_ESTAB', 'SERIES DE ESTABILIDADE FINANCEIRA DISPONIBILIZADAS PELO BANCO CENTRAL DO BRASIL', 'BCB');           INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BCB_FISCAL', 'SERIES DE POLITICA FISCAL DISPONIBILIZADAS PELO BANCO CENTRAL DO BRASIL', 'BCB');                  INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BCB_SE', 'SERIES DO SETOR EXTERNO DISPONIBILIZADAS PELO BANCO CENTRAL DO BRASIL', 'BCB');                        
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BCB_EXP_12M', 'SERIES DE EXPECTATIVAS 12 MESES A FRENTE DISPONIBILIZADAS PELO BANCO CENTRAL DO BRASIL', 'BCB');  INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BCB_EXP_ANUAL', 'SERIES DE EXPECTATIVAS DE FINAL DE ANO DISPONIBILIZADAS PELO BANCO CENTRAL DO BRASIL', 'BCB');

INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('ONS_ENA', 'INFORMACOES SOBRE UTILIZAÇAO DO ENERGIA NATURAL AFLUENTE TO BRASIL', 'ONS');         

-- BEA --
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BEA_GDP', 'DADOS RELACIONADOS AO PIB DOS E.U.A.', 'BEA');         
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BEA_CONSUMER', 'DADOS RELACIONADOS A PESQUINA DE CONSUMO E RENDA DOS E.U.A.', 'BEA');
--CEPEA --
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('CEPEA_PRECO', 'COTACOES DE PRECOS DE ITENS AGRICOLAS NO BRASIL', 'CEPEA');

-- CPB
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('CPB_TRADE', 'ESTATISTICAS DE PRODUCAO MUNDIAL PRODUZIDAS PELO CPB', 'CPB');

--NBSC--
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('NBSC_PIBY', 'DADOS ANUALIZADOS DO PIB E SEUS COMPONENTES', 'NBSC');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('NBSC_PIBQ', 'DADOS TRIMESTRAIS DO PIB E SEUS COMPONENTES COM AJUSTE SAZONAL', 'NBSC');                       
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('NBSC_CPI', 'INDICE DE PREÇO AO CONSUMIDOR E SEUS PRINCIPAIS COMPONENTES', 'NBSC');                       
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('NBSC_PPI', 'INDICE DE PREÇO AO PRODUTOR E SEUS PRINCIPAIS COMPONENTES', 'NBSC');                       
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('NBSC_TRADE', 'DADOS DA BALANÇA COMERCIAL, CHINA', 'NBSC');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('NBSC_PMI', 'PMI OFICIAL DA CHINA E SEUS COMPONENTES', 'NBSC');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('NBSC_IND', 'PRODUCAO INDUSTRIAL, CHINA', 'NBSC');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('NBSC_RETAIL', 'VAREJO CHINA E SEUS COMPONENTES', 'NBSC');                            
COMMIT;
