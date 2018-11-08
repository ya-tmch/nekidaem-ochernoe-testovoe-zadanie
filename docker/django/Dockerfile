FROM python:3.7-stretch

LABEL Description="Django container"

RUN pip3 install django psycopg2-binary

COPY ./watch.sh /watch.sh

RUN chmod +x /watch.sh