import pymongo
import dns # required for connecting with SRV
import time
import api_velo

client = pymongo.MongoClient("mongodb+srv://admin:FzM8WTPuY5@cluster0.lgxev.gcp.mongodb.net/test?w=majority")
db = client.get_database('Locations')
db.global_velo.create_index([('Name','text')])

def search(station):

    cur = db.global_velo.find({"Name": {"$regex": station, "$options": "i" }})
    print(cur)
    for doc in cur:
        print(doc)


search("St")
