FROM python:3.9

WORKDIR /app
COPY . .

RUN pip install flask requests mysql-connector-python

CMD ["python", "app.py"]