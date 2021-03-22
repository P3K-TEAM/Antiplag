FROM python:3.8-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /backend

# Install pipenv dependencies
COPY Pipfile /backend/
COPY Pipfile.lock /backend/
RUN pip install pipenv
RUN pipenv install

# Initialize nltk
COPY nltk_init.py /backend/
RUN pipenv run python nltk_init.py

# Install tesseract-ocr
RUN apt-get update
RUN apt-get install -y tesseract-ocr
RUN apt-get -y install gcc mono-mcs
