import Graph
import CusTopo
import heapq
import CusHost

import sys
sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/api')
import updateWeight

class Dijkstra(object):
    """Dijktra shortest path algorithm"""
    def __init__(self, topo, start, end):
       """
       topo: Custopo object hold network
       start: starting node object
       end: ending node object
       nodes: list of node object
       edges: dictionary of edge object
       """
       self.topo = topo
       self.nodes = topo.get_nodes()
       self.edges = topo.get_edges()
       self.start = start
       self.end = end

       self.distance = dict()  # minimum distance from start each node in shortest path
       self.path = dict()   # parent of each node in shortest path
       self.minimum_cost = 0
       self.result = []
       self.heap = []

       self.routing_preparation()

    def routing_preparation(self):

       # neu tap ket qua luu duong di truoc di thi reset lai de routing duong moi
       if self.result:
            self.reset_route()

       for node in self.nodes:
            self.distance[node] = (0 if node == self.start else float('inf') )
            self.path[node] = None

    def reset_route(self):
       self.distance = dict()  
       self.path = dict()  
       self.minimum_cost = 0
       self.result = []
       self.heap = []

    def routing(self):  

        self.routing_preparation()
        #print("heap hien tai", len(self.heap) )

        self.heap = [ (0, self.start) ]  # cost from start node
        visited = set()

        while self.heap:
            (current_cost, u) = heapq.heappop(self.heap)
            #print(current_cost, u)

            if u in visited:
                continue
            visited.add(u)

            if u.get_id() == self.end.get_id():
                self.minimum_cost = current_cost
                # backtrack to save shortest path
                self.set_result()
                return 
                
            for v, c, edge_address in self.edges[u]:
                #print("vertex", v, "cost", v)
                if v not in visited and current_cost + c < self.distance[v]:
                    next = current_cost + c
                    self.path[v] = u  # parent of v is u
                    self.distance[v] = next # update new distance
                    heapq.heappush(self.heap, (next, v))
        return -1

    def get_distance(self):
        return self.distance

    def get_path(self):
        return self.path
        
    def set_result(self):
        current = self.end
        
        while current != self.start:
            parent = self.path[current]
            edge_object = self.topo.find_edge(src= parent, dest = current)

            weight = edge_object[1] # access weight in list
            self.result.append( edge_object[2] ) # access edge address in list
            current = parent

        # reverse result
        self.result = self.result[::-1]
        #print(self.result)
        # print("hello")

    def get_minimum_cost(self):
        return self.minimum_cost

    def __str__(self):
        for e in self.result:
            print("from", e.get_src().get_id(), "->", e.get_dest().get_id(), 
                    " = ", e.get_weight() )
        return "OK"

    def set_start(self, start):
         self.start = start

    def set_end(self, end):
        self.end = end

    def get_result(self):
        return self.result

# # khoi tao do thi
# topo = CusTopo.Topo()
# # graph se them du lieu do thi vao topo 
# graph = Graph.Graph(topo)
# hien thi do thi
#print(topo)

# print( topo.get_servers() )
# print("hosts = ")
# print( topo.get_hosts() )
# for node in topo.get_nodes():
#     if isinstance( node, CusHost.Host):
#         print(node.get_ip())


# src = topo.get_nodes()[11]
# dst = topo.get_nodes()[9]

# # # for node in topo.get_nodes():
# # #     print(node.get_id())

# # # # chay thuat toan tim duong chieu xuoi
# sol =  Dijkstra(topo = topo, start = src, end = dst)
# sol.routing()
# print(sol)

# #### chay file update

#  update = updateWeight.updateWeight()


# while(True):
#     # doc du lieu tu rabbit
#     object.read_params_file()
#     #print(object.get_count())
#     #print(object.get_count())
#     # khi nao doc duoc 500 du lieu tu rabbit
#     if object.get_count() == 500:
#         # viet trong so moi ra DB
#         object.write_params_file()
#         # reset bien doc du lieu
#         object.set_count(count = 0)
#         # print("after", object.get_count())
#         #print("Done")
#         # topo doc du lieu tu DB
#         topo.read_update_weight()
#         # routing l
#         sol.routing()
#         print(sol)
        #print(topo)

# # # # sau khi update trong so 
# # topo.read_update_weight()


# # print("Chay lai thuat toan tim duong TRONG SO MOI")
# #print(topo)
# # #sol.routing_preparation()
# # sol.routing()
# # print(sol)

# # print(topo)

# # # truy xuat ket qua duong di vua tim
# # solution.get_path()
# # # hien thi toan bo ket qua duong di
# # print( solution )

# # #print( solution.get_path[-1] )




# # #NHiem vu: Dao duoc duong di

# # a = solution.get_path()# # a = [1,2,3,4]
# # # b = list(reversed(a))
# # # c = a[::-1]
# # b = sorted(a, reverse=True)
# # print(a)
# # print(b)
# # print(c)
# # print(a[0].get_src().get_id())
# # print(b[0].get_src().get_id())



