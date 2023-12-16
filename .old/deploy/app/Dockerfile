FROM python:3.10-alpine

RUN apk add --no-cache postgresql-dev build-base

WORKDIR /app
COPY ../../requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir ./input
RUN mkdir ./tx
RUN mkdir ./output

COPY ../../src/* .

CMD [ "python", "main.py" ]
