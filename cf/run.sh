#!/bin/sh

echo "------ Setting up database -----"
python registry.py pycsw -c setup_db

echo "------ Rebuild repository indexes -----"
python registry.py pycsw -c reindex

echo "------ Starting service -----"
python registry.py runserver 0.0.0.0:$PORT
