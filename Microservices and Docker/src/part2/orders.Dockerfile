FROM python:3.9-alpine

WORKDIR /app

COPY /back-end/orders_service.py /back-end/orders_DB.csv /back-end/Read_Write_Lock.py /app/

ENTRYPOINT ["python3", "orders_service.py"]