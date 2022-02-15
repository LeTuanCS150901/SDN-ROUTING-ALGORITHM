
import requests
import json
from requests.auth import HTTPBasicAuth

def call_topo_api():
    
    # print("GOI API TAP TOPO")
    response = requests.get('http://localhost:8181/onos/test/localTopology/getTopo',
      auth=HTTPBasicAuth('onos', 'rocks'))

    with open('/home/onos/Downloads/flaskSDN/flaskAPI/topo.json', 'w') as f:
          json.dump(response.content, f)
    # print(response)

def call_host_api():

    response = requests.get('http://localhost:8181/onos/v1/hosts',
      auth=HTTPBasicAuth('onos', 'rocks'))

    with open('/home/onos/Downloads/flaskSDN/flaskAPI/host.json', 'w') as f:
          json.dump(response.content, f)

# hello()
# call_host_api()