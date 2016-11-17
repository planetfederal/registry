#!/bin/sh

echo "------ Setting up database -----"
python registry.py pycsw -c setup_db

echo "------ Running server instance -----"
python registry.py runserver 0.0.0.0:$PORT
