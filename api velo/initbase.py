import pymongo
import dns # required for connecting with SRV
import api_velo

client = pymongo.MongoClient("mongodb+srv://putyourid:mdphere.yoururl")
db = client.get_database('Locations')

localisation = db.location_velo

data = api_velo.send_collection()

localisation.insert_many(data)
