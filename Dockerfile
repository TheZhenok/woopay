FROM python:3.10.6-buster

WORKDIR /app

COPY . .

RUN python3 -m venv /opt/venv
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]