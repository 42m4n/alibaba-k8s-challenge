FROM python:alpine

COPY requirements.txt ./
RUN pip install -r requirements.txt

WORKDIR /opt
COPY receiver.py ./
COPY sender.py ./

ENV RABBITMQ_HOST rabbitmq
ENV RABBITMQ_QUEUE ticket-queue
