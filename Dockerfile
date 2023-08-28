FROM python:3.11.5-bookworm

WORKDIR /code

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD uvicorn --host 0.0.0.0 --port 5000 app:app