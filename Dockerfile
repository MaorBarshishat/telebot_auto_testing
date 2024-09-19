FROM python:3.10

ADD .env .
ADD testing.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "./testing.py"]