CREATE USER flask;
CREATE DATABASE flask_db
    WITH 
    OWNER = flask
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

\connect flask_db

CREATE TABLE public.tweets_data(
    id SERIAL PRIMARY KEY,
    timestamp_col TIMESTAMP,
    tweets_org  character varying(500),
    predictions smallint NOT NULL
    );
    
