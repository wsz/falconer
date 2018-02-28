#!/usr/bin/env bash

function safely_unset {
    backup_var=${1}_BACKUP
    if [[ -n ${!backup_var} ]]
    then
        export "${1}"=${!backup_var}
        unset ${backup_var}
    else
        unset ${1}
    fi
}

safely_unset PYTHONPATH
safely_unset DB_DRIVER_NAME
safely_unset DB_NAME
