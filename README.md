# BFAF (Backend for a Frontend)

The BFAF handles communication between the React.js client and the microservices, acting as a gateway layer to the backend.

## Set up

Install python 3.6 -> make a virtual environment valled 'venv' `virtualenv venv`

Activate the venv ->  `source venv/bin/activate`

`pip install -r requirements.txt`


## Run local dev server

`python bfaf.py run`

## Tests

`python bfaf.py test`


## Docker

The Docker container is used for deploying in production.

`docker-compose up` should allow you to build and run it.
