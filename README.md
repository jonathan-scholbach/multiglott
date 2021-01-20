__multiglott__ is a web application for a community driven vocabulary trainer. 

In order to install your own __multiglott__ application, rename the `.env-example` to `.env`:

    mv .env-example .env

fill in the appropriate settings and run the server with `docker-compose`.


The application consists of three docker containers, one for the REST API in the backend, built with Python's FastAPI, one for the client code, built using Vue.js, and one for the PostgreSQL database.


In order to run the database migrations, run `alembic` inside the docker container:

    docker-compose run api alembic upgrade head


In order to autogenerate migrations with `alembic`, run

    docker-compose run api alembic revision --autogenerate