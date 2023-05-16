#!/bin/bash

############################################################
# script para montar base de dados
# e carrega-la com dados básicos.
# Funciona apenas para sqlite3
# Ultima atualização: 18/04/2023
############################################################

dir_name="$(dirname $realpath $0)"
cd "$dir_name"


function build_db(){
    if [[ -e ./DB/database.db ]]; then 
	rm ./DB/database.db
    fi
    touch ./DB/database.db
    echo ".bail on"
    echo ".open ./DB/database.db"
    echo ".read ./sql_setup/schema.sql"
    exit 0
}


function load_db(){
    if ! [[ -e ./DB/database.db ]]; then 
	echo "DB not set up"
	exit 1
    else
	echo ".bail on"
	echo ".open ./DB/database.db"
	echo ".read ./sql_setup/input.sql"
	echo ".mode csv"
	echo ".import ./DB/series.csv series"
	echo ".read ./sql_setup/tables.sql"
    fi
    exit 0
}

case $1 in

    "build") build_db | sqlite3 --batch
	     ;;
    "load") load_db | sqlite3 --batch
	    ;;
    "run")  uvicorn app:app --reload --loop asyncio
	    ;;
    "backup") sqlite3 ./DB/database.db -csv -header 'select series_id, description,  survey_id from series' > ./DB/series.csv
	      ;;
    "help") echo "Type either build, load, run or backup "
	    ;;
    *) echo "Type help"
       ;;
esac

exit 0
