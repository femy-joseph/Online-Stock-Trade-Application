FROM python:3.9-alpine

WORKDIR /app

COPY /back-end/catalog_service.py /back-end/stocks_DB.csv /back-end/Read_Write_Lock.py /app/

ENTRYPOINT ["python3", "catalog_service.py"]
