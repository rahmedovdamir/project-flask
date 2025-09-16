FROM python:3.11

WORKDIR /app

ADD . /app

RUN apt install gcc -y

RUN pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]

