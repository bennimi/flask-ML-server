## Docker containerization to deploy ML models

Docker-compose.yml to set up the following services:

* Flask as backend server
	* server-side input validation on server
	* client-side input validation using JS
	* client-side input validation utilizing fetch-api
* uWSGI as application server (combined with flask)
	* handles flask app
	* routes traffic from flask to nginx
* nginx as HTTP webserver

* postgres as backend db

* pgAdmin as GUI for postgres 
	* to connect to server:
		* host name: postgres
		* port: 5432
		* username/pw: root
___________________________________________________________________________________________________

Future work:
* setup bottlenecks on kubernetes

