FROM python:3.10-bullseye

RUN apt-get update -y
RUN apt-get install -y sqlite3

# COPY --chown=www-data:www-data src/pip /var/app/pip
COPY --chown=www-data:www-data src/. var/app/
# COPY --chown=www-data:www-data docker_compose/docker/scripts/* /
# ADD --chown=www-data:www-data src/* /var/app/
RUN cd /var/app/
RUN pip install -r pip/requirements.txt

VOLUME /var/app/
WORKDIR /var/app/

ENTRYPOINT [ "sh", "/docker-entrypoint.sh" ]
CMD [ "python", "main.py" ]