FROM python:3.11.5-slim-bullseye
WORKDIR /app
COPY . /app
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "app.py"]