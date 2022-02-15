import sys
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/core')
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/handledata/models')
import Dijkstra, Graph
import CusDevice, CusHost, CusLink, CusTopo, Flow, Flows, Instruction, Selector, Treatment, Criteria
import json
import requests
from requests.auth import HTTPBasicAuth


class flowRule(object):
    """
    flowRule object generates json file which adds flow
    """
    def __init__(self, topo, shortest_path, src, dst):
        """
        topo: Custopo network object
        shortest_path: list of edge resuts in path
        src: starting node
        dst: ending node
        """
        self.topo = topo
        self.shortest_path = shortest_path
        self.src = src
        self.dst = dst
        self.json_rule = dict() 
        self.jsonRulePath = ""
        self.priority = 200

    def get_json_rule(self):
        return self.json_rule

    def get_src(self):
        return self.src.get_id()

    def get_dst(self):
        return self.dst.get_id()

    def get_shortest_path(self):
        return self.shortest_path

    def create_flow_rule(self, flows):  
        """
        Generates flow rule framework
        """
        for link in range ( len (self.shortest_path) ):
                    from_node = self.shortest_path[link].get_src()
                    to_node   = self.shortest_path[link].get_dest()
                    # abandon first edge 
                    if isinstance( from_node, CusHost.Host ):
                        continue                                         
                    elif isinstance( to_node, CusHost.Host):

                        device = from_node  
                        port_out =  self.shortest_path[link].get_port()

                        previous_link = self.shortest_path[ link -1 ]
                        from_node = previous_link.get_src()

                        if isinstance( from_node, CusHost.Host ):
                            port_in = previous_link.get_port()
                        else:
                            port_in = previous_link.get_port_in()                                 
                    else:            
                        port_out = self.shortest_path[link].get_port_out()
                        device = from_node
            
                        previous_link = self.shortest_path[ link - 1 ]
                        from_node = previous_link.get_src()

                        # trung gian dau tien bi vuong host
                        if isinstance( from_node, CusHost.Host ):
                            port_in = previous_link.get_port()
                        else: # cac trung gian con lai
                            port_in = self.shortest_path[link-1].get_port_in()

                    self.priority +=1
                    flow = Flow.Flow(priority = self.priority, timeout = 0, isPermanent = True, deviceId = device.get_id()  )
                    treatment = Treatment.Treatment()
                    selector = Selector.Selector()

                    # add instruction to treatment
                    instruction = Instruction.Instruction(type = "OUTPUT", port = port_out)
                    # set port out
                    treatment.set_instructions( instruction_object = instruction )

                    # set criteria oobject
                    criteria = Criteria.Criteria(type = "IN_PORT")
                    criteria_src = Criteria.Criteria(type = "ETH_SRC")
                    criteria_dst = Criteria.Criteria(type = "ETH_DST")
                        
                    # set port in
                    criteria.set_port(port_in)

                    criteria_src.set_port(0) 
                    criteria_dst.set_port(0)

                    criteria_src.set_mac( self.src.get_id() )
                    criteria_dst.set_mac( self.dst.get_id() )
                    # add criteria to selector
                    selector.set_criterias(criteria_object = criteria)
                    selector.set_criterias(criteria_object = criteria_src)
                    selector.set_criterias(criteria_object = criteria_dst)

                    # add treat ment and selector to flow object
                    flow.set_treatment( treatment_object = treatment)
                    flow.set_selector( selector_object = selector)
                    # add each flow to flows object
                    flows.set_flows(flow_object = flow)

    def add_flow_rule(self):
        """
        set attributes of flow rule
        """
        flows = Flows.Flows()
        self.create_flow_rule(flows)

        json_flows = []
        self.json_rule['flows'] = json_flows

        # add flow rule value
        for f in flows.get_flows():
            json_flow = dict()
            json_flows.append( json_flow )
            json_flow['priority'] = f.get_priority()
            json_flow['timeout'] = f.get_timeout()
            json_flow['isPermanent'] = f.get_isPermanent()
            json_flow['deviceId'] = f.get_deviceId()

            # treatment dictionary
            json_treatment = dict()
            json_instructions = []
            json_treatment['instructions'] = json_instructions

            for instruct in f.get_treatment().get_instructions():
                json_instruction = dict() 
                json_instructions.append( json_instruction )  
                json_instruction['port'] = instruct.get_port()
                json_instruction['type'] = instruct.get_type()
              
            # add treatment dictionary to each flow
            json_flow['treatment'] = json_treatment

            # selector dictionary
            json_selector = dict()
            # add selector dictionary to each flow
            json_flow['selector'] = json_selector

            json_criterias = []
            json_selector['criteria'] = json_criterias

            count = 1
            for crite in f.get_selector().get_criterias():
                json_criteria = dict()
                json_criterias.append ( json_criteria )          
                json_criteria['port'] = crite.get_port()
                json_criteria['type'] = crite.get_type()

                # using count to avoid 'mac' key in the first instruction object
                if count != 1:
                    json_criteria['mac'] = crite.get_mac()
                else:
                    count += 1
              
        #self.write_json_rule_to_file(self.json_rule)        
        # with open('/home/onos/Downloads/flaskSDN/flaskAPI/jsonRuleXuoi.json', 'w') as json_file:
        #      json.dump(self.json_rule, json_file)

    def write_json_rule_to_file(self, json_rule_path, json_rule_reversing_path):

        flows_reversing_path = json_rule_reversing_path['flows']
        flows_path = json_rule_path['flows']
        #print(flows_path)
     
        for elem in range ( len (flows_reversing_path) ):     
            temp =  flows_reversing_path[elem]
            flows_path.append( temp )

        #print( len (flows_path))
        self.jsonRulePath = json_rule_path
        #self.call_routing_api()
        
        with open('/home/onos/Downloads/flaskSDN/flaskAPI/jsonRulePath.json', 'w') as json_file:
            json.dump( json_rule_path, json_file)

        self.call_routing_api()

    def call_routing_api(self):
        """
        Automatically POST rulePath to API
        return 200 if successul routing
        """
        with open("/home/onos/Downloads/flaskSDN/flaskAPI/jsonRulePath.json") as json_file:
                data = json.load(json_file)

        headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": "Basic a2FyYWY6a2FyYWY="
                    }
        data=json.dumps(data)
        query = {'appID': "1233"}
        
        response = requests.post('http://localhost:8181/onos/v1/flows?appId=onos.onosproject.routing', 
        params=query,auth=HTTPBasicAuth('onos', 'rocks'), data = data, headers=  headers )
        # print(response)
        # print("Da add flow thanh cong")
    

class hostServerConnection(object):

    def __init__(self, topo_network, hosts, servers):

        # khoi tao topo 
        # self.topo = CusTopo.Topo()
        # # add do thi vao topo
        # self.graph = Graph.Graph(self.topo)

        # # moi lan khoi tao xong thi cap nhap luon topo tu Mongo
        # self.update_topo()

        # # host dictionary and server list creation 
        # self.hosts = self.topo.get_hosts()
        # self.servers = self.topo.get_servers()
        self.topo = topo_network
        self.hosts = hosts
        self.servers = servers

        # khoi tao thuat toan tim duong
        self.sol = ""
        self.reverse_sol = ""
        
        # add flow
        self.flow = ""
        self.reverse_flow = ""

        # host ip
        self.host_ip = ""
        self.dest_ip = ""

    def update_topo(self):
        self.topo.read_update_weight()

    def set_host_ip(self, host_ip):
        self.host_ip = host_ip
    
    def find_src(self):
        host_object = self.hosts[self.host_ip]     
        return host_object

    def find_shortest_path(self):
        
        min_cost = 0
        host_object = self.find_src()
        dest_object = ""
        path = ""
        # di chieu xuoi
        for server in self.servers:       
            # chay thuat toan
            self.sol = Dijkstra.Dijkstra( topo=self.topo, start= host_object, end= self.servers[server])
            self.sol.routing()

            current_cost = self.sol.get_minimum_cost()
           
            if min_cost == 0:
                min_cost = current_cost

            if min_cost >= current_cost:
                min_cost = current_cost
                dest_object = self.servers[server]
                path = self.sol.get_result()

        
        # bat dau goi flow rule 
        # quan trong phai tim duoc path
        self.add_flow(host_object, dest_object, path)
      
        return dest_object.get_ip()
      
    def add_flow(self, host_object, dest_object, path):

        # di chieu nguoc
        self.reverse_sol = Dijkstra.Dijkstra( topo=self.topo, start= dest_object, end= host_object)
        self.reverse_sol.routing()
        reverse_path = self.reverse_sol.get_result()

        # add flow chieu thuan
            
        #print("\n\nadd flow JSon")
        flow = flowRule(topo = self.topo, shortest_path = path, src = host_object, dst = dest_object)
        flow.add_flow_rule()
        flow_rule = flow.get_json_rule()


        #print("\n\nadd reverse flow JSon")
        reverse_flow = flowRule(topo = self.topo, shortest_path = reverse_path, src = dest_object, dst = host_object)
        reverse_flow.add_flow_rule()
        reverse_flow_rule = reverse_flow.get_json_rule()
        
        flow.write_json_rule_to_file(json_rule_path = flow_rule, 
                                 json_rule_reversing_path= reverse_flow_rule)

    

# object = hostServerConnection()
# object.set_host_ip(host_ip= "10.0.0.1")
# a = object.find_shortest_path()
# print(a)
# # khoi tao topo 
# topo = CusTopo.Topo()
# # add do thi vao topo
# graph = Graph.Graph(topo)

# src = topo.get_nodes()[11]
# dst = topo.get_nodes()[12]

# chay thuat toan tim duong chieu xuoi
#sol =  Dijkstra.Dijkstra(topo = topo, start = src, end = dst)
# sol.routing()
# path = sol.get_result()
# print(sol)


# # chay thuat toan tim duong chieu nguoc
# reverse_sol =  Dijkstra.Dijkstra(topo = topo, start = dst, end = src)
# reverse_sol.routing()
# reverse_path = reverse_sol.get_result()
# print(reverse_sol)


# print("\n\nadd flow JSon")
# flow = flowRule(topo = topo, shortest_path = path, src = src, dst = dst)
# flow.add_flow_rule()
# flow_rule = flow.get_json_rule()



# print("\n\nadd reverse flow JSon")
# reverse_flow = flowRule(topo = topo, shortest_path = reverse_path, src = dst, dst = src)
# reverse_flow.add_flow_rule()
# reverse_flow_rule = reverse_flow.get_json_rule()

# # viet ra file flow cuoi cung va day api
# flow.write_json_rule_to_file(json_rule_path = flow_rule, 
#                                  json_rule_reversing_path= reverse_flow_rule)




