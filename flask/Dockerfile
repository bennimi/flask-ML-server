FROM python:3.6-slim

RUN apt-get update
RUN apt-get install -y build-essential
RUN python -m pip install --upgrade pip

COPY . /usr/app/

WORKDIR /usr/app/

## internal port
#EXPOSE 5000

RUN pip install -r requirements.txt

## startup app when build container

#CMD ["uwsgi", "app.ini"] # called in docker-compose to wait startup db-server