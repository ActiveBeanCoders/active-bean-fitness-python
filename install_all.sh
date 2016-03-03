#!/bin/bash

function die {
    printf '%s\n' "ERROR. goodbye."
    exit 1
}

projects=(
    "data_all_api/"
    "data_db_api/"
    "data_es_api/"
    "fitness_common/"
    "security-api/"
)
printf '%s\n' "Installing: ${projects[*]}"

for proj in ${projects[@]}; do
    cd ${proj} || die
    printf '%s\n' "Installing ${proj} (develop)"
    python setup.py develop
    cd ..
done

