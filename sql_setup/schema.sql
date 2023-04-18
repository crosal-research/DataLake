/*
Ativa support para foreign key
ver: https://www.sqlite.org/foreignkeys.html
*/
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;;

/*
Base de Dados para App
de Series de Tempo
*/

/*
Creates table for contas
*/
DROP TABLE IF EXISTS Conta; 
CREATE TABLE IF NOT EXISTS Conta (
       conta_id TEXT NOT NULL PRIMARY KEY,
       nome TEXT NOT NULL
);

/*
Creates table for Clients
*/
DROP TABLE IF EXISTS Cliente; 
CREATE TABLE IF NOT EXISTS Cliente (
       nome TEXT NOT NULL,
       email TEXT NOT NULL PRIMARY KEY,
       senha TEXT NOT NULL,
       conta_id TEXT DEFAULT 'G',
       FOREIGN KEY (conta_id) REFERENCES Conta (conta_id) ON UPDATE CASCADE ON DELETE SET DEFAULT
);


/*
Creates table for sources
*/
DROP TABLE IF EXISTS Source; 
CREATE TABLE IF NOT EXISTS Source (
       source_id TEXT NOT NULL,
       full_name TEXT NOT NULL,
       PRIMARY KEY (source_id)
);


/*
Creates table for sources
*/
DROP TABLE IF EXISTS Source; 
CREATE TABLE IF NOT EXISTS Source (
       source_id TEXT NOT NULL,
       full_name TEXT NOT NULL,
       PRIMARY KEY (source_id)
);


/*
Creates table for surveys
*/
DROP TABLE IF EXISTS Survey;
CREATE TABLE IF NOT EXISTS Survey (
       survey_id TEXT NOT NULL,
       description TEXT NOT NULL,
       source_id TEXT,
       PRIMARY KEY (survey_id)
       FOREIGN KEY (source_id) REFERENCES Source (source_id) ON DELETE CASCADE
);

/*
Creates table for series
*/
DROP TABLE IF EXISTS Series;
CREATE TABLE IF NOT EXISTS Series (
       series_id TEXT NOT NULL,
       description TEXT NOT NULL,
       survey_id TEXT,
       frequency TEXT,
       last_update TEXT,
       PRIMARY KEY (series_id)
       FOREIGN KEY (survey_id) REFERENCES Survey (survey_id) ON DELETE CASCADE
);


/* 
Creates tabel for User tables
Due to a many-to-may relationship
demands a relationship intermediary table
*/
DROP TABLE IF EXISTS Utable;
CREATE TABLE IF NOT EXISTS Utable (
       utable_id TEXT NOT NULL,
       description TEXT,
       proprietario TEXT NOT NULL,
       PRIMARY KEY (utable_id)
       FOREIGN KEY (proprietario) REFERENCES Conta (conta_id) ON DELETE CASCADE
);

--relationship table between utable and series
DROP TABLE IF EXISTS series_utable;
CREATE TABLE IF NOT EXISTS series_utable (
       utable_id TEXT,
       series_id TEXT,
       PRIMARY KEY (utable_id, series_id),
       FOREIGN KEY (utable_id) REFERENCES Utable (utable_id) ON DELETE CASCADE,
       FOREIGN KEY (series_id) REFERENCES Series (series_id) ON DELETE CASCADE
);


/*
Creates table for observations
*/
DROP TABLE IF EXISTS Observation;
CREATE TABLE IF NOT EXISTS Observation (
       dat TEXT NOT NULL,
       valor TEXT NOT NULL,
       series_id TEXT NOT NULL,
       primary key (dat, series_id),
       foreign key (series_id) REFERENCES Series (series_id) ON DELETE CASCADE
);



-- Creates table for series search
-- see: https://sqlite.org/spellfix1.html
-- DROP TABLE IF EXISTS Search;
-- CREATE VIRTUAL TABLE IF NOT EXISTS Search USING fts5(ticker, description);


-- create auxiliar table for the case of using fuzzy search
-- DROP TABLE IF EXISTS Search_aux;
-- CREATE VIRTUAL TABLE IF NOT EXISTS Search_aux USING fts5vocab(Search);



