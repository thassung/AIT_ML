FROM python:3.9-bookworm

# WORKDIR /code

# COPY requirements.txt .
RUN pip3 install pandas
RUN pip3 install ipykernel
RUN pip3 install dash

# COPY . .

# EXPOSE 5000

CMD tail -f /dev/null