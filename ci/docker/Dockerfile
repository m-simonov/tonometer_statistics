FROM python:3.10-bullseye

RUN apt-get update -y
RUN apt-get install -y sqlite3

COPY src/. var/app/
# COPY --chown=www-data:www-data ci/docker/scripts/* /
RUN cd /var/app/ && pip install -r pip/requirements.txt

VOLUME /var/app/
WORKDIR /var/app/

# ENTRYPOINT [ "sh", "/docker-entrypoint.sh" ]
CMD [ "python", "main.py" ]