#!/bin/bash

# echo "siema"
TARGET_DIR=${1}


FILES=$(find katalog -name "*.conf" -type f)

# echo "${FILES}"

rm -rf backup
mkdir  backup

for FILE in ${FILES}; do
    echo "${FILE}"
    cp -v "${FILE}" backup/
done

zip -r katalog_$(date +"%Y-%m-%d").zip backup/

if [[ ${FILE} == *.conf ]]; then
    echo "koncyz sie na .conf"
else
    echo "niet"
fi
