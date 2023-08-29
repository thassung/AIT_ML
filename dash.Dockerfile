FROM python:3.9-bookworm

WORKDIR /root

COPY ./ /root/
RUN pip3 install -r requirements.txt

# EXPOSE 5000

CMD tail -f /dev/null