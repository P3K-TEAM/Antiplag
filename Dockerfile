FROM python:3.8-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /backend
COPY Pipfile /backend/
COPY Pipfile.lock /backend/
COPY nltk_init.py /backend/
RUN pip install pipenv
RUN pipenv install
RUN pipenv run python nltk_init.py
RUN apt-get update
RUN apt-get install -y tesseract-ocr
