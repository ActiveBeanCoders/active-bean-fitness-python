#!/bin/bash

files=(
    data_db_project/manage.py
    data_es_project/manage.py
)

cwd="$(pwd)"
for file in ${files[@]}; do
    printf '%s\n' "######################################################"
    printf '%s\n' "#### ${file%/*}"
    printf '%s\n' "######################################################"
    cd "${file%/*}"
    python manage.py test
    cd "${cwd}"
done

