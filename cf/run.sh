#!/bin/sh

echo "------ Setting up database -----"
python registry.py pycsw -c setup_db

echo "------ Starting service -----"
python registry.py runserver 0.0.0.0:$PORT
