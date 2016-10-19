registry

[![Build Status](https://travis-ci.org/boundlessgeo/registry.svg?branch=master)](https://travis-ci.org/boundlessgeo/registry)
[![Coverage Status](https://coveralls.io/repos/github/boundlessgeo/registry/badge.svg?branch=master)](https://coveralls.io/github/boundlessgeo/registry?branch=master)

Usage
=====

Step 1. Initialize the database.

    python registry.py pycsw -c setup_db

Step 2. Run the server.

    python registry.py runserver

Step 3. Access it via http://localhost:8000/


Features
========

 - [ ] CSW-T support via pycsw
 - [ ] Mirror information to Elasticsearch for faster searches
 - [ ] OpenSearch based API to enable the use of facets on different fields (extending CSW standard).
