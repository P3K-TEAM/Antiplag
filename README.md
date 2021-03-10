# AntiPlag - Backend

# Prerequisites
 - [Docker](https://www.docker.com/)
 
## Installation and configuration

1. Set your environment variables
    
    Create your own `.env` file in root similar to `.env.example`. 
    
    Specify your `ELASTIC_HOST`.
    `DJANGO_SECRET_KEY` can be generated as `base64 /dev/urandom | head -c50`.
    
    Other configuration in `.env.example` is ready for local development.

1. Build and run docker containers

    Run following command in base directory of this project:
    ```
    docker-compose up
    ```
    Docker image for this application will be automatically built. Then, all necessary infrastructure (database, message broker)
    will be run along with web application and Celery worker.

1. Run database migrations
         
    1. Create all necessary tables in database by executing:
        
        ```
        docker-compose exec web pipenv run bash -c "cd antiplag && python manage.py migrate"
        ```

## Usage

1. Run `docker-compose up` in base directory of this project.

## Guides

- To find out how to format code in this repository, please read our [code formatting docs](docs/CODE_FORMATTING.md)
