# Antiplag backend
## Configuring your development
### virtualenv
Create your own virtual env that uses Python 3.8

### Requirements
Install all requirements from requirements.txt

```pip install -r antiplag/requirements.txt```

### Enviroment variables
Create your own `.env` file in folder with `manage.py`.
 
Configure `.env` file by following `.env.example`. Don't forget to specify the database connection url.

### Run migrations
To create all necessary tables in database, run:

```python antiplag/manage.py migrate```

### Run local development server
```python antiplag/manage.py runserver```

## Code formatting
Before committing, format code using `black` formater:

```black .```