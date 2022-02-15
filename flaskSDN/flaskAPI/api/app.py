import sys
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/model')
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/handledata/models')
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/core')
import flowRule
import params_model, updateWeight, CusTopo, Graph, Round_robin
from flask import Flask, request
import destQueueRabbit
import pandas as pd
import topo
import requests
import pub
    
# Init app
app = Flask(__name__)

topo.call_topo_api()
topo.call_host_api()

topo_network = CusTopo.Topo()
# add do thi vao topo
graph = Graph.Graph(topo_network)

hosts = topo_network.get_hosts()
servers = topo_network.get_servers()

# print("Doc Queue 1 lan duy nhat")
# print(servers)
# queue_rr = destQueueRabbit.destQueueRabbit()

# for ip in servers:
#   queue_rr.connectRabbitMQ(ip_dest= ip)

# khoi tao bien CAP NHAP LINK COST
update = updateWeight.updateWeight()

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return 'sondzai'

@app.route('/getIpServer', methods=['POST'])
def add():
  if request.method == 'POST':
    host_ip = request.data

    # chuay kieu dijktra
    #object = flowRule.hostServerConnection()
    object = flowRule.hostServerConnection(topo_network, hosts, servers)
    
    # chay kieu Round RR
    # object = Round_robin.hostServerConnectionRR(queue_rr, topo_network, graph, hosts, servers)
    object.set_host_ip(host_ip= str(host_ip))
    dest_ip = object.find_shortest_path()

    # B1: mininet -> host ip >flask
    # B2: app.py co host ip_address
    # B3: dua host ip cho file flow rule
    # B4: flow rule tra ve flask dest ip

  return str(dest_ip)

@app.route('/',  methods=['GET', 'POST'] )
def write_data():

   # cong mac dinh la GET
  if request.method == 'GET':
    app.logger.info('Da nhan duoc GET')
    return "Da nhan duoc GET"

  if request.method == 'POST':
    #app.logger.info("Da nhan dc POST")

    # get data from API
    content = request.data
    dicdata={}
    datas=content.split("&")

    # processing data
    for data in datas:
      d=data.split(":")

      if len(d) == 3:
        temp = [ d[1], d[2] ]
        dicdata[ d[0] ] = ":".join(temp)
      else:
        dicdata[ d[0] ] = d[1] 

    #  Xoa data <= 556
    if float(dicdata['byteSent']) > 556:
      #print("ket qua", dicdata['byteSent'] )
      
      # them du lieu vao rabbit de lay ra lien tuc
      pub.connectRabbitMQ( data = dicdata )
      # them du lieu vao MONGO de theo doi ve sau
      params_model.insert_data(dicdata)

      # doc data tu rabbit
      update.read_params_file()

      # khi nao doc duoc 500 du lieu tu rabbit
      if update.get_count() == 100: 
          
        # # khoi tao do thi
        #   topo_object = CusTopo.Topo()
        # # graph se them du lieu do thi vao topo 
        #   graph_object = Graph.Graph(topo_object)
          app.logger.info("Da nhan dc 100 du lieu tu rabbit")
          # viet trong so moi ra Mongo
          update.write_update_weights_file()
          # reset bien doc du lieu
          update.set_count(count = 0)

          #update = updateWeight.updateWeight()
          # reset lai tap canh chua trong so cu
          #update.reset_link_set()
    
          # topo doc du lieu tu Mongo va cap nhap topo
          # topo_object.read_update_weight()
       
      
      # # write data to csv
      # array = []````````````````````````
      # array.append(dicdata)

     
      #columns = [ 'src', 'dst', 'delay', 'linkUtilization', 'byteSent', 'byteReceived', 'time', 'packetLoss' ]
      # df = pd.DataFrame(array, columns= columns )````````````````````
      # df.to_csv("/home/onos/Downloads/flaskSDN/flaskAPI/params.csv", mode='a', index = False, header=False)
    
      #app.logger.info('Da tao dc file csv')  
  return content

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
  
    

   

   