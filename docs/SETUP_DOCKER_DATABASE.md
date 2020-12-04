## Setting up PostgreSQL database with docker

1. Get and install docker from [official docker page](https://docs.docker.com/get-docker/).

1. Copy following and save it into `docker-compose.yml` file.

    ```yaml
    version: "3.8"
       
    services:
      database:
        image: postgres
        environment:
          - POSTGRES_DB=antiplag
          - POSTGRES_USER=root
          - POSTGRES_PASSWORD=root
        ports:
          - "5432:5432"
        volumes:
          - database-data:/var/lib/postgresql/data/ # persist data even if container shuts down
    volumes:
      database-data:
    
    ```

1. Run following command in the directory where your `docker-compose.yml` is:

    ```
    docker-compose -p antiplag-postgres up
    ```

1. Now your postgres database is running and available on port `5432`. 
