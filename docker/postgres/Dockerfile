FROM mdillon/postgis:9.5

# Copy init command.
COPY init_db.sh /docker-entrypoint-initdb.d/
COPY pycsw.sql /