FROM postgres:13-alpine

COPY dbschema.sh /docker-entrypoint-initdb.d/
COPY schemafifadb.sql /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/dbschema.sh

