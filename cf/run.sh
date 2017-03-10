#!/bin/sh

#if [[ "$REGISTRY_DATABASE_URL" == "postgres"* ]]; then
#    echo "------ Installing psycopg2 -----";
#    pip install psycopg2 --upgrade;
#else
#    echo "----- PostgreSQL Database is not being used -----";
#fi
#
echo "------ Setting up database -----"
python registry.py pycsw -c setup_db

echo "------ Starting service -----"
python registry.py runserver 0.0.0.0:$PORT
