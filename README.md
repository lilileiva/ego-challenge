# ego-challenge

Submit to EGO challenge consisting in a development of a API using Django

# Table of Contents
1. [Install and run the project](#Install-and-run-the-project)
2. [Run tests](#Run-tests)
3. [Load database data](#Load-database-data)
4. [Admin site](#Admin-site)
5. [Documentation](#Documentation)



## Install-and-run-the-project

### with Docker

Clone de repository

    git clone https://github.com/lilileiva/ego-challenge

Create .env file with env_sample.txt content

    mkdir .env

Build the image

    docker build -t django-ego .

Run the project

    docker run -it -p 8000:8000 django-ego

### with virtual enviroment

Clone de repository

    git clone https://github.com/lilileiva/ego-challenge

Set a virtual enviroment

    cd ego-challenge

    python -m venv venv

    cd venv/Scripts

    activate

    cd ../..

Create .env file with env_sample.txt content

    mkdir .env

Install requirements

    pip install -r requeriments.txt

Migrate

    python manage.py migrate

Run the project

    python manage.py runserver

## #Load-database-data

We have an empty database by default, to load data for testing porpuses use:

    python manage.py loaddata dump.json

## Run tests

Run all tests

    python manage.py test

Run specific test

    python manage.py test -k "<test_name>"

Example:
python manage.py test -k "test_dealerships_list_success"

## Admin-site

Create super user

    python manage.py createsuperuser

Django admin site

    localhost:8000/admin

## Documentation

Swagger documentation

    localhost:8000/swagger
    