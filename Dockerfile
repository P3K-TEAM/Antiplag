FROM python:3.8-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /backend/antiplag

# Install platform dependencies
RUN \
apt-get update && \
apt-get install -y python-dev gettext libgettextpo-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig gcc mono-mcs

# Install pipenv dependencies
COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv
RUN pipenv install --pre --clear

# Initialize nltk
COPY nltk_init.py .
RUN pipenv run python nltk_init.py
