# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ARG directory=./frontend-flask

COPY $directory/requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip3 install -r requirements.txt
COPY $directory /app

EXPOSE 5002

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
