FROM postgres:9.5

RUN apt-get update && apt-get install -y \
    sudo \
    vim \
    wget \
    build-essential \
    libffi-dev \
    libssl-dev \
    git

ADD postgresql.conf /etc/postgresql/9.5/main/postgresql.conf
ADD pg_hba.conf /etc/postgresql/9.5/main/pg_hba.conf
RUN chown postgres:postgres /etc/postgresql/9.5/main/*.conf
ADD run.sh /usr/local/bin/run.sh
RUN chmod +x /usr/local/bin/run.sh

EXPOSE 5432
CMD ["/usr/local/bin/run.sh"]