# import numpy as np
# import pandas as pd
# import sub
# import sys
# sys.path.append('/home/onos/Downloads/flaskSDN/flaskAPI/model')
# import model
# import history_weights

# class updateWeight(object):

#     def __init__(self):
#         # params_data is a data frame object
#         self.params_data = ""
#         self.link_set = set()
#         self.consumer = sub.Sub()
#         self.count = 0

#     def read_params_file(self):
#         self.consumer.receive_queue()
#         #self.params_data = self.consumer.peek_stack()
#         self.params_data = self.consumer.pop_stack()
#         self.count += 1

#         self.update_link()

#     def update_link(self):
#         id_src = str (self.params_data['src'])
#         id_dst = str (self.params_data['dst'])    
#         link = self.has_link(target_src = id_src, target_dst = id_dst)

#         if link == None:
#             link = WeightLink(id_src= id_src, id_dst= id_dst)
#             self.link_set.add(link)
#         else:
#             link.update_weight(params_data= self.params_data)
 
#     def has_link(self, target_src, target_dst):
#         found = None
#         for link in self.link_set:
#             if link.get_id_src() == target_src and link.get_id_dst() == target_dst:
#                 found = True
#                 return link
#         return None

#     def write_update_weights_file(self):
#         print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
#         # xoa het trong so cu o Mongo
#         model.remove_all()
#         print("Write update weight to file ...")
#         # save_params = []
#         print(self.link_set)
#         for link in self.link_set:
#             src = link.get_id_src()
#             dst = link.get_id_dst()
#             #weight = link.get_link_cost()
#             weight = link.peek_weight_stack()
#             #print("KET QUA = ", weight)
#             temp_data = { "src": src, "dst": dst, "weight": weight }
#             # save into mongoDB
#             # model la bang update weight
#             model.insert_data(temp_data)
#             history_weights.insert_data(temp_data)

#             # save_params.append( [src, dst, weight] )
#         # df = pd.DataFrame( save_params )
#         # # convert column "a" to int64 dtype and "b" to complex type
#         # # df.columns = ['src', 'dst', 'cost']
#         # # df = df.astype({"src": int, 'dst':int})
#         # header = ['src', 'dst', 'weight']
#         # df.to_csv("/home/onos/Downloads/flaskSDN/flaskAPI/updateWeight.csv", mode ='a', index = False, header= header)   
#         # print(save_params)
     
#     def get_link_set(self):
#         return self.link_set

#     def get_count(self):
#         return self.count

#     def set_count(self, count):
#         self.count = count

#     def reset_link_set(self):
#         self.link_set = set()
        
# class WeightLink(object):

#         def __init__(self, id_src, id_dst):
#             self.id_src = id_src
#             self.id_dst = id_dst
           
#             # WEIGHT MATRIX INCLUDES [DELAY, LINK_U, PACKET_LOSS] 
#             # self.W = []
#             # self.delay_stack = []
#             # self.link_utilization_stack = []
#             # self.packet_loss_stack = []
#             self.weight_stack = []

#             self.link_cost = 0.0
#             self.delay = 0.0
#             self.link_utilization = 0.0
#             self.packet_loss = 0.0
            
#             self.alpha = 0.2
#             self.beta = 0.4
#             self.gamma = 0.4

#         def get_id_src(self):
#             return self.id_src

#         def get_id_dst(self):
#             return self.id_dst

#         def get_weight(self):
#             return self.weight

#         def update_weight(self, params_data):

#             self.delay += float( params_data['delay'] )
#             self.link_utilization+= float( params_data['linkUtilization'] )
#             self.packet_loss += float( params_data['packetLoss'] )

#             self.weight = (self.alpha * self.delay) + (self.beta * self.link_utilization) + (self.gamma * self.packet_loss)
#             self.push_weight_stack()

#             # test chuan hoa
#             # get data
#             # self.delay = float( params_data['delay'] )
#             # self.link_utilization = float( params_data['linkUtilization'] )
#             # self.packet_loss = float( params_data['packetLoss'] )
            
#             # # day cac tham so vao stack
#             # self.delay_stack.append( self.delay )
#             # self.link_utilization_stack.append( self.link_utilization ) 
#             # self.packet_loss_stack.append( self.packet_loss )


#         def push_weight_stack(self):
#             self.weight_stack.append( self.weight)

#         def peek_weight_stack(self):
#             # return weight average
#             #return self.weight_stack[-1] / len(self.weight_stack)
#             return self.weight_stack.pop()

#         # def normalize_data(self):

#         #     # convert list to vector with float type
#         #     delay_vector            = np.array( self.delay_stack, dtype='f')
#         #     link_utilization_vector = np.array( self.link_utilization_stack, dtype='f')
#         #     packet_loss_vector      = np.array( self.packet_loss_stack, dtype='f')
            
#         #     # stack 3 vector as a feature Matrix
#         #     self.W = np.stack( (delay_vector, link_utilization_vector , packet_loss_vector ), axis=-1)

#         #     # Chuyen vi ma tran de duyet qua tung cot tuong ung voi cac feature thay vi cac hang trong ma tran
#         #     self.W = self.W.T
            
#         #     # DUYET QUA TUNG COT CUA MA TRAN roi chuan hoa theo tung cot
#         #     for feature in range(len(self.W)):

#         #         # normalize each feature with MIN-MAX scaling
#         #         self.W[feature] = ( self.W[feature]-self.W[feature].min() ) / ( self.W[feature].max()-self.W[feature].min() ) 
  
#         # def get_link_cost(self):

#         #     self.link_cost = self.find_link_cost()
#         #     return self.link_cost
        
#         # def find_link_cost(self):
            
#         #     # chuan hoa ma tran trong so W tu truoc den nay
#         #     self.normalize_data()
            
#         #     # tinh vector mean cua tung feature
#         #     mean_W = []
#         #     for num in self.W:
#         #         mean_W.append( num.mean() )

#         #     # Tinh tich vo huong vector mean feature va vector tham so hoc
#         #     mean_W = np.array( mean_W, dtype='f')
#         #     learning_vector = np.array( [ self.alpha, self.beta, self.gamma ], dtype='f')

#         #     return mean_W.dot(learning_vector.T)
                        

# # fake_data = np.array( [ 
# #     ["src0", "dst1", 2, 3, 4, 5, 6, 7], 
# #     ["src1", "dst2", 9, 8, 7, 6, 5, 4],
# #     ["src0", "dst1", 3, 4, 5, 6, 7, 8],
# #     ["src1", "dst2", 2, 3, 4, 5, 6, 10]
# # ])
# # df = pd.DataFrame( fake_data ) 

# # print( df)


        