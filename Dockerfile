FROM python:3.5

RUN apt-get update && apt-get install -y \
                gcc \
                gettext \
                postgresql-client libpq-dev \
                sqlite3 \
                python-gdal python-psycopg2 \
                python-imaging python-lxml \
                python-dev libgdal-dev \
        --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/

EXPOSE 8000

CMD ["python", "registry.py", "runserver", "0.0.0.0:8000"]
