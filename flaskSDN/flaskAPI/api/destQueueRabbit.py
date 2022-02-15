import pandas as pd
import requests
import csv
import pika
import sys
import time
import json
# func ket noi rabbitmq


class destQueueRabbit(object):

    def __init__(self):
        self.dest_ip = ""

        # # khoi tao topo 
        # self.topo = CusTopo.Topo()
        # # add do thi vao topo
        # self.graph = Graph.Graph(self.topo)

        # # khoi tao queue moi xong moi lan cap nhap mang
        # self.server_to_queue()
        # # moi lan khoi tao xong thi cap nhap luon topo tu Mongo
        # self.update_topo()

        # # host dictionary and server list creation 
        # self.hosts = self.topo.get_hosts()
        # self.servers = self.topo.get_servers()

    def connectRabbitMQ(self, ip_dest):
            # quan trong nhat
            msg = str(ip_dest)
            #print("msg =", msg)
            #print("type msg", type(msg))
            # print("DAY VAO QUEUE", msg)
            connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()

            channel.queue_declare(queue='dest')
            channel.basic_publish(
                    exchange='',
                    routing_key='dest',
                    body=msg,
                    properties=pika.BasicProperties(
                        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                    ))

    # lay rabbit
    def receive_queue(self):

                connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
                channel = connection.channel()
                channel.queue_declare(queue='dest')
                #print('Waitting for data send')

                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(queue='dest', on_message_callback= self.callback )
                
                #channel.open()
                channel.start_consuming()

    def callback(self, ch, method, properties, body):
                  

                    self.dest_ip = body
                    ch.basic_ack(delivery_tag=method.delivery_tag)

                    # do call back duoc goi lien tuc nen sau 1 lan goi ta stop lai
                    ch.close()
           
    def get_dest_ip(self):
        return self.dest_ip

    #connection.close()

# while(True):
#     # quan trong
#     Links_details = {'src': 1234,'des':3456}
#     # goi ham connect
#     connectRabbitMQ(Links_details)


