FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY alembic.ini /app/
COPY alembic /app/alembic/
COPY main.py /app/

ENTRYPOINT ["python", "main.py"]