FROM python:3.6-slim

COPY . /usr/app/

WORKDIR /usr/app/

## internal port
EXPOSE 5000

RUN pip install -r requirements.txt

## startup app when build container
#CMD python flask_app.py

