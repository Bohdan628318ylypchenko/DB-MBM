FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt /app/
COPY src /app/

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]