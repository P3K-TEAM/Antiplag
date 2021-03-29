# AntiPlag - Backend

## Prerequisites

- [Docker](https://www.docker.com/)

## Installation and configuration

1. Set your environment variables by creating your own `.env` file in root similar to `.env.example`.

    - Specify your `ELASTIC_HOST`.
    - Specify `DJANGO_SECRET_KEY`. It can be generated as `base64 /dev/urandom | head -c50`.
    
   All Other configuration in `.env.example` is ready for local development.

1. Build and run docker containers

   Run following command in base directory of this project:

    ```
    docker-compose up --build --d
    ```

   Docker image for this application will be automatically built. Then, all necessary infrastructure (database, message
   broker)
   will be run along with web application and Celery worker.

1. Run database migrations

   Create all necessary tables in database by executing:

    ```
    docker-compose exec web pipenv run migrate"
    ```

## Usage

Run `docker-compose up` in base directory of this project.

### Code formatting

Before committing, format code using `black` formater:

```
docker-compose exec web pipenv run lint
```

### Unit tests

Run unit tests using following command:

```
docker-compose exec web pipenv run test
```

