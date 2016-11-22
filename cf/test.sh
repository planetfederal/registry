#!/bin/sh

cd /app
. .profile.d/python.sh
/app/.heroku/python/bin/pip -r cf/test-requirements.txt
.heroku/python/bin/python setup.py test
exit
