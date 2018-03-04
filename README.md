# UI Backend (or Backend for a Frontend/BFAF)
This repository contains a Flask application written in Python that acts as a middleman between the various microservices and the user interface.

## How to set up
In order to set up the backend for running, follow these steps:

  1. Install Python 3.x.
  2. Make a virtual environment - `python3 -m venv venv`.
  3. Activate the virtual environment - `source venv/bin/activate`.
  4. Install dependencies using pip - `pip install -r requirements.txt`.

## How to run
In order to run the backend, follow the set-up steps above and then run `python3 bfaf.py run`.

## How to test
In order to test the backend, follow the set-up steps above and then run `python bfaf.py test`.

## Using Docker container
This repository includes a docker container for deployment in production. You can use it by running `docker-compose up`.
