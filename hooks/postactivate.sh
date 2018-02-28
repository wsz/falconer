#!/usr/bin/env bash

function safely_set {
    if [[ -n ${!1} ]]
    then
        export "${1}_BACKUP"=${!1}
    fi
    export "${1}"=${2}
}

safely_set PYTHONPATH '.'
safely_set DB_DRIVER_NAME sqlite
safely_set DB_NAME db.sqlite3
