FROM python:3.12-alpine

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /app/

EXPOSE 8082

ENTRYPOINT ["python", "main.py"]

