FROM python:3.7.3

RUN apt-get update -y

RUN apt-get install -y graphviz

COPY _resources/app /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD python app.py
