import numpy as np

# import requests

# r = requests.post("http://127.0.0.1:5000/getIpServer", data="2")
# print( type(str(r.text)) )


a = [1,2,3,4]
b=  [4,5,6,7]
c = [7,8,9,10]

a1 = np.array(a)
b1 = np.array(b)
c1 = np.array(c)

a1.reshape( (len(a), 1) )
print(a1.shape)
print(a1)
