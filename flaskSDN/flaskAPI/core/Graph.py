import sys
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/handledata/models')
import CusHost, CusLink, CusDevice, CusTopo
import json
import ast

class Graph(object):
    """
    Graph object adds topology network from file to Custopo object 
    """
    def __init__(self, topo):
       """
       topo: Custopo object
       topo_file: holds json data file
       """
       self.topo = topo
       self.topo_file = ""
       self.host_file = ""
       self.load_topo()

    def load_topo(self):
        """
        Read topo json and save it to topo_file
        """
        with open('/home/onos/Downloads/flaskSDN/flaskAPI/topo.json') as handle:
            self.topo_file = json.loads(handle.read())
            self.topo_file=  ast.literal_eval(self.topo_file)
        
        self.create_topo()
        
    def create_topo(self):
        """  Adds data from topo_file to our topo object """
        self.add_devices()
        self.add_links()
        self.add_hosts()

    def add_links(self):
        for link in self.topo_file['links']:
            # extract data from dictionary
            src = link['src']
            dst = link['dst']
            id_src = src['id']
            id_dst = dst['id']
            port_out = src['port']
            port_in = dst['port']
            
            # get device src and dst objects
            d_src = self.find_device(id_src)
            d_dst = self.find_device(id_dst)

            # add edge between src and dst devices
            edge1 = CusLink.DeviceEdge(d_src, d_dst, 1, port_in, port_out)
            edge2 = CusLink.DeviceEdge(d_dst, d_src, 1, port_out, port_in)

            # add edges to topo
            self.topo.add_edge(edge1)
            self.topo.add_edge(edge2)

    def add_devices(self):
        for device in self.topo_file['devices']:
            id = device['id']
            # create device object
            device = CusDevice.Device(id)
            # add device object to topo object
            self.topo.add_node(device)

    def add_hosts(self):
        #print("1111111111111111111111111111")

        with open('/home/onos/Downloads/flaskSDN/flaskAPI/host.json') as handle:
            self.host_file = json.loads(handle.read())
            self.host_file = "\'" + self.host_file + "\'"
            self.host_file=  ast.literal_eval(self.host_file)
            self.host_file = json.loads(self.host_file)


        hosts = dict()
        servers = dict()

        #print(self.host_file)
        for host in self.host_file['hosts']:
            #print("123")
            host_mac = str(host['mac'])
            host_ip = str(host['ipAddresses'][0])
                 
            locations = host['locations']
            location = locations[0]
            port = int(location['port'])
            device_id = str(location['elementId'])
            
            device = self.find_device(device_id)
            host = CusHost.Host( id = host_mac, device = device, port = port, ip= host_ip)

            number = int(host_ip[-1])
            if number <=4:
                hosts[host_ip] = host
                
            else:
                servers[host_ip] = host
               
            #print("server hien tai", servers)
            self.topo.set_hosts(hosts= hosts)
            self.topo.set_servers(servers= servers)
            self.topo.add_node(host)
 
            edge1 = CusLink.HostEdge(host, device, 1 , port)
            edge2 = CusLink.HostEdge(device, host, 1 , port)
            
            self.topo.add_edge(edge1)
            self.topo.add_edge(edge2)

        # for host in self.topo_file['hosts']:
        #     # extract data from dictionary
        #     host_id = host['id']
        #     device_id = host['deviceId']
        #     port = host['port']

        #     device = self.find_device(device_id)
        #     # create host object connect with device object
        #     host = CusHost.Host( id = host_id, device = device, port = port)
        #     # add host object to topo object
        #     self.topo.add_node(host)
 
        #     edge1 = CusLink.HostEdge(host, device, 1 , port)
        #     edge2 = CusLink.HostEdge(device, host, 1 , port)
            
        #     self.topo.add_edge(edge1)
        #     self.topo.add_edge(edge2)
        
    def find_device(self, target):
        nodes = self.topo.get_nodes()
        for device in nodes:
            if device.get_id() == target:
                return device


    

# d1 = CusDevice.Device( id = "id_d1")
# d2 = CusDevice.Device( id = "id_d2")

# h1 = CusHost.Host( id="id_h1", device = d1)
# h2 = CusHost.Host( id="id_h2", device = d2)

# l1 = CusLink.Edge(h1, d1, 10000)
# l2 = CusLink.Edge(d1, h2, 50000)
# l3 = CusLink.Edge(d2, h2, 30000)

# topo.add_node(d1)
# topo.add_node(d2)
# topo.add_node(h1)
# topo.add_node(h2)

# topo.add_edge(l1)
# topo.add_edge(l2)
# topo.add_edge(l3)

# topo = CusTopo.Topo()
# graph = Graph(topo = topo)
# print(topo)