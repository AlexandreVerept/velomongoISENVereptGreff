import pymongo
import dns # required for connecting with SRV
import time
import api_velo
import time

client = pymongo.MongoClient("mongodb+srv://admin:FzM8WTPuY5@cluster0.lgxev.gcp.mongodb.net/test?w=majority")
db = client.get_database('Locations')

localisation = db.lille_velo
key = {}

while True:
    data = api_velo.send_live()
    localisation.insert_many(data, ordered=True)
    time.sleep(60)