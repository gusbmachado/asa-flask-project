# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /asa-flask-project

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=project
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]