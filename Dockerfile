FROM python:latest

COPY . /app/
WORKDIR /app
RUN pip3 install -r requirements.txt

CMD ["python3", "run.py"]
