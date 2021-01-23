# deprecated to avoid creation of new image

FROM postgres:9.6

ENV PG_MODE=primary
ENV DATABASE_HOST=0.0.0.0
ENV POSTGRES_USER=root
ENV POSTGRES_PASSWORD=root
ENV POSTGRES_DB=root  

ADD postgres_init_flask_db.sql /docker-entrypoint-initdb.d/