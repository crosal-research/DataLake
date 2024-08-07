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
       conta_id TEXT NOT NULL,
       nome TEXT NOT NULL,
       PRIMARY KEY (conta_id)
);

/*
Creates table for Clients
*/
DROP TABLE IF EXISTS Cliente; 
CREATE TABLE IF NOT EXISTS Cliente (
       roleType TEXT DEFAULT 'CLIENT',   -- CLIENT, ADMIN
       email TEXT NOT NULL PRIMARY KEY,
       senha TEXT NOT NULL,
       conta_id TEXT DEFAULT 'GUEST',
       api_key TEXT,
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
       last_update TEXT,
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
       first_observation TEXT,
       last_observation TEXT,
       PRIMARY KEY (series_id)
       FOREIGN KEY (survey_id) REFERENCES Survey (survey_id) ON DELETE CASCADE
);


/*
Creates table Tracker
that keep track of whenever a series'
observations is selected
*/
CREATE TABLE IF NOT EXISTS Tracker (
       series_id TEXT NOT NULL,
       timeA TEXT NOT NULL,
       PRIMARY KEY (series_id, timeA)
       FOREIGN KEY (series_id) REFERENCES Series (series_id) ON DELETE CASCADE
);


/*
View to retrived the weekly requests of each
Series by users
*/
DROP VIEW IF EXISTS Weekly_Tracker;
CREATE VIEW Weekly_Tracker AS
Select series_id, count(*) as wtracker from Tracker
where timeA >= datetime('now', 'localtime', '-14 days') and timeA <= datetime('now', 'localtime')
group by series_id order by wtracker desc;


/*
View to retrived the monthly requests of each
Series by users
*/
DROP VIEW IF EXISTS Monthly_Tracker;
CREATE VIEW Monthly_Tracker AS
Select series_id, count(*) as mtracker from Tracker
where timeA >= datetime('now', 'localtime', '-30 days') and timeA <= datetime('now', 'localtime')
group by series_id order by mtracker desc;


/* 
Creates tabble for User tables
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
DROP TABLE IF EXISTS Search;
CREATE VIRTUAL TABLE IF NOT EXISTS Search USING fts5(ticker, description, 
       tokenize = "unicode61");

-- Used in case of batch insertiong into search table
-- INSERT INTO search (ticker, description) SELECT series_id, description FROM series;

-- see: https://stackoverflow.com/questions/70847617/populate-virtual-sqlite-fts5-full-text-search-table-from-content-table
-- https://kimsereylam.com/sqlite/2020/03/06/full-text-search-with-sqlite.html


CREATE TRIGGER search_ai AFTER INSERT ON series
    BEGIN
        INSERT INTO search (ticker, description)
        VALUES (new.series_id, new.description);
    END;


CREATE TRIGGER search_del AFTER DELETE ON series
    BEGIN
        INSERT INTO search (ticker, description)
	VALUES ('delete', old.series_id, old.description)
    END;


CREATE TRIGGER search_au AFTER UPDATE ON series
    FOR EACH ROW
    WHEN (new.description != old.description)
    BEGIN
	UPDATE search SET description = old.description
    END;


