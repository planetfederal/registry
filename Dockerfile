FROM python:3.5

RUN apt-get update && apt-get install -y \
                libgeos-dev \
                && rm -rf /var/lib/apt/lists/*

RUN mkdir /code

WORKDIR /code

ADD . /code/

RUN pip3 install -r requirements.txt
RUN pip3 install psycopg2