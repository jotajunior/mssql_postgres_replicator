FROM ubuntu

# install all dependencies
RUN apt-get update && apt-get install -y \
	sudo \
	python3 \
	python3-psycopg2 \
	libpq-dev \
	python3-pip \
	python3-dev \
	python3-setuptools \
	unixodbc \
	unixodbc-dev \
	freetds-dev \
	freetds-bin \
	tdsodbc \
	postgresql

# finish setting up driver for MSSQL
COPY . /beblue-replicator
WORKDIR /beblue-replicator

RUN cp odbcinst.ini /etc/odbcinst.ini
RUN cd /beblue-replicator && python3 setup.py develop 
CMD start_replication
