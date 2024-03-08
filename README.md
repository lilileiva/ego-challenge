# ego-challenge

Submit to EGO challenge consisting in a development of a API using Django

# Table of Contents
1. [Install and run the project](#Install-and-run-the-project)
2. [Run tests](#Run-tests)
3. [Documentation](#Documentation)



## Install-and-run-the-project

Clone de repository

    git clone https://github.com/lilileiva/ego-challenge

Set a virtual enviroment

    cd ego-challenge

    python -m venv venv

    cd venv/Scripts

    activate

    cd ../../..

Install requirements

    pip install -r requeriments.txt

Run the project

    python manage.py runserver

## Run tests

    python manage.py test <test path>

Example:
python manage.py test 'ego.cars.tests.test_dealership.DealershipTestCase'

## Documentation

Swagger documentation

    localhost:8000/swagger
    