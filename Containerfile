FROM fedora

EXPOSE 5000/tcp

USER root

RUN mkdir /app

WORKDIR /app

RUN dnf install -y git python3.11 python3-pip python3-PyMySQL.noarch mariadb  mariadb-connector-c-devel gcc python3-devel

RUN  git clone https://github.com/Siname22/TFG-booksGallery-Back.git

WORKDIR TFG-booksGallery-Back/

ENV MARIADB_CONFIG=/usr/bin/mariadb_config

RUN pip3 install mariadb

RUN  pip3 install --user -r requirements.txt

ENTRYPOINT python3 manage.py
