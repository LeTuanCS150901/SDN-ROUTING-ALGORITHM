from pymongo import MongoClient

# mongo_uri = "mongodb://username:" + urllib.quote("p@ssword") + "@127.0.0.1:27001/"
mongo_uri = "mongodb://127.0.0.1:27017"
connection = MongoClient(mongo_uri)

# CREATE DATABASE
database = connection['SDN_data']
# database = connection['roundRobinParams']
# CREATE COLLECTION
collection = database['params']
# print("Database connected")

def insert_data(data):
    """
    Insert new data or document in collection
    :param data:
    :return:
    """
    collection.insert(data)
    return


def get_multiple_data():
    """
    get document data by document ID
    :return:
    """
    data = collection.find()
    return list(data)


# CLOSE DATABASE
connection.close()










# weights = Model.find({})
# for w in weights:
#     print(w)
# insert one
# data = {  "src": "Son dzai src", "dst": "Son dzai dst", "weight": "281" }

# insert many
# data = [ {  "src": "Son dzai src", "dst": "Son dzai dst", "weight": "281" } ,
#         {  "src": "Son dzai src", "dst": "Son dzai dst", "weight": "281" }]
# weight_collection.insert(data)

# update one
# weight_collection.update({"dieukien", {"$set": {"gia tri sua"}}})
# weight_collection.update({"weight": "281"}, {"$set": {"src": "Son van dzai src"}})


# update many
# weight_collection.update_many({"weight": "281"}, {"$set": {"src": "Son van dzai src"}})

# delete
# weight_collection.delete_one({"Dieu kien"})
# weight_collection.delete_many({"Dieu kien"})
