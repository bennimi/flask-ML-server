FROM python:3.6-slim

RUN apt-get update
RUN apt-get install -y build-essential


COPY . /usr/app/

WORKDIR /usr/app/

## internal port
#EXPOSE 5000

RUN pip install -r requirements.txt

## startup app when build container
#CMD python flask_app.py
CMD ["uwsgi", "app.ini"]