# AntiPlag - Backend

# Prerequisites
 - [Python ^3.0](https://www.python.org/downloads/) 
 - [Pip](https://pypi.org/project/pip/) 
 - [Pipenv](https://pypi.org/project/pipenv/)

## Installation

1. Install all dependencies using

    ```
    pipenv install
    ```
 
## Configuration

1. Activate virtual environment

   ```
   pipenv shell
   ```

1. Set your environment variables
    
    Create your own `.env` file in root similar to `.env.example`

1. Run database migrations
    
    1. Have your database server running first
    1. Setup database credentials in environment variables 
    1. To create all necessary tables in database, run
        
        ```
        python manage.py migrate
        ```

## Usage

1. Activate virtual environment

   ```
   pipenv shell
   ```

1. Run local development server 
    ```
    python manage.py runserver
    ```

## Guides

To find out how to format code in this repository, please read our [code formatting docs](docs/CODE_FORMATTING.md)
