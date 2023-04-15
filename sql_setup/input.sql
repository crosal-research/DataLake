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
       VALUES ('BIS_WS_EER_M', 'TAXAS DE CAMBIOS REAL EFETIVOs', 'BIS');                                                         
COMMIT;


--Isert Series
BEGIN TRANSACTION;
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.UNRATE', 'TAXA DE DESEMPREGO DOS E.U.A.', 'FRED_ECON');
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.CFNAI', 'INDICE DE ATIVIDADE NACIONAL E.U.A. DO FED DE CHICAGO', 'FRED_ECON');
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.USRECD', 'INDICADOR DE RECESSAO DOS E.U.A. PUBLICADO PELA NBER', 'FRED_ECON');
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.PCEPI', 'INDICE DE PRECOS PCE', 'FRED_ECON');
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.PCEPILFE', 'NUCLEO DO PCE POR EXCLUSAO DE ALIMENTOS E ENERGIA', 'FRED_ECON');
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.T10YIE', 'INFLACAO IMPLICITA de 10 ANOS EXTRAIDA DOS TITULO SOBERANDO E.U.A.', 'FRED_FIN');
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.VIXCLS', 'VOLATILIDADE IMPLICITA DO S&P500', 'FRED_FIN');
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.CIVPART', 'TAXA DE PARTICIPAÇAO DA MAO-DE-OBRA DOS E.U.A.', 'FRED_ECON');
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.UMCSENT', 'SENTIMENTO DO CONSUMIDOR DOS E.U.A. DA UNIVERSIDADE DE MICHIGAN', 'FRED_ECON');
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.CPILFESL', 'NUCLEO DO INDICE DE PREÇOS AO CONSUMIDOR DOS E.U.A (CPI) POR EXCLUSAO DE ALIMENTOS E ENERGIA', 'FRED_ECON');
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.CPIAUCSL', 'INDICE DE PREÇOS AO CONSUMIDOR DOS E.U.A (CPI)', 'FRED_ECON');
INSERT INTO Series (series_id, description, survey_id)n
      VALUES ('FRED.PAYEMS', 'TOTAL DE EMPREGOS CRIADOS NOS E.U.A. EXCLUIDO O SETOR AGRĨCOLA (NONFARM PAYROLL)', 'FRED_ECON');
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.INDPRO', 'PRODUCAO INDUSTRIAL DOS E.U.A. COM AJUSTE SAZONAL', 'FRED_ECON');
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.ICSA', 'PEDIDOS INICIAIS DE SEGURO DESEMPREGO', 'FRED_ECON');
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.DGS10', 'TAXA DE JUROS DA TAXA DE 10 ANOS DO TÍTULO DO GOVERNO DOS E.U.A (TREASURY)', 'FRED_FIN');
INSERT INTO Series (series_id, description, survey_id)
      VALUES ('FRED.EFFR', 'TAXA FED FUNDS EFETIVA', 'FRED_FIN');
INSERT INTO Series (series_id, description, survey_id)      
      VALUES ('FRED.VXEWZCLS', 'VOLATILIDADE IMPLICITA DO ETF EWZ DE ACÕES BRAZILEIRAS', 'FRED_FIN');                        
COMMIT;
