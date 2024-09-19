FROM python:3.10

ADD .env .
ADD prepare_device.py .
ADD testing.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "./prepare_device.py"]
CMD ["python", "./testing.py"]