FROM python:3.9-alpine

WORKDIR /app

COPY /front-end/server.py .

ENTRYPOINT ["python3", "server.py"]