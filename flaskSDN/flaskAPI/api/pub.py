import pandas as pd
import requests
import csv
import pika
import sys
import time
import json
# func ket noi rabbitmq
def connectRabbitMQ(data):
    # quan trong nhat
    msg = json.dumps(data)
    #print("msg =", msg)
    #print("type msg", type(msg))

    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='onos')
    channel.basic_publish(
            exchange='',
            routing_key='onos',
            body=msg,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
    #connection.close()

# while(True):
#     # quan trong
#     Links_details = {'src': 1234,'des':3456}
#     # goi ham connect
#     connectRabbitMQ(Links_details)


