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
       VALUES ('G', 'GUEST');       
COMMIT;

--Insert Cliente
INSERT INTO Cliente (nome, email, conta_id, senha)
       VALUES ('ADMIN', 'joao.rosal@terrainvestimentos.com.br', 'TI', '123');

--Insert Sources
BEGIN TRANSACTION;
INSERT INTO Source (source_id, full_name)
       VALUES ('BCB', 'BANCO CENTRAL DO BRASIL');
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
COMMIT;	      


--Insert Surveys
BEGIN TRANSACTION;

INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('IBGE_PIM', 'PESQUISA INDUSTRIAL MENSAL, Brasil', 'IBGE');
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('IBGE_PMC', 'PESQUISA MENSAL DE COMERCIO, BRASIL', 'IBGE');
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('IBGE_PMS', 'PESQUISA MENSAL DE SERVICO, BRASIL', 'IBGE');      
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('IBGE_CN', 'CONTAS NACIONAIS TRIMESTRAIS, BRASIL', 'IBGE');
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('IBGE_PNAD', 'Pesquisa Nacional de Amostra Domiliar Continuada, Brasil', 'IBGE');                        
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('FRED_ECON', 'DADOS ECONÔMICOS DISPONIBILIZADOS PELO FRED', 'FRED');
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('FRED_FIN', 'DADOS FINANCEIROS DISPONIBILIZADOS PELO FRED', 'FRED');
INSERT INTO Survey (survey_id, description, source_id)
      VALUES ('IPEA', 'DADOS GENERICOS DISPONIBILIZADOS PELO IPEA', 'IPEA');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('IPEA_ECON', 'DADOS ECONOMICOS DISPONIBILIZADOS PELO IPEA', 'IPEA');   
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('IPEA_FIN', 'DADOS FINANCEIROS DISPONIBILIZADOS PELO IPEA', 'IPEA');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BLS_CPI', 'DADOS DE INFLACAO AO CONSUMIDOR DOS E.U.A.', 'BLS');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('IMF_PCPS', 'PRECO DE COMMODITIES PRIMARIAS', 'IMF');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BIS_WS_EER_M', 'TAXAS DE CAMBIOS REAL EFETIVOS', 'BIS');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BCB_ECON', 'SERIES ECONOMICAS DO BANCO CENTRAL DO BRASIL', 'BCB');                                                INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BCB_MERCADO-ABERTO', 'SERIES FINANCEIRAS DISPONIBILIZADAS PELO BANCO CENTRAL DO BRASIL', 'BCB');                  
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BCB_CREDITO', 'SERIES DO MERCADO DE CREDITO E POLITICA MONETARIA DISPONIBILIZADAS PELO BANCO CENTRAL DO BRASIL', 'BCB');
INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BCB_ESTAB', 'SERIES DE ESTABILIDADE FINANCEIRA DISPONIBILIZADAS PELO BANCO CENTRAL DO BRASIL', 'BCB');           INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BCB_FISCAL', 'SERIES DE POLITICA FISCAL DISPONIBILIZADAS PELO BANCO CENTRAL DO BRASIL', 'BCB');                   INSERT INTO Survey (survey_id, description, source_id) 
       VALUES ('BCB_SE', 'SERIES DO SETOR EXTERNO DISPONIBILIZADAS PELO BANCO CENTRAL DO BRASIL', 'BCB');                        COMMIT;
