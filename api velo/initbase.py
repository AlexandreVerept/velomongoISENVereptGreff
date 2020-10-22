import pymongo
import dns # required for connecting with SRV
import api_velo

def init_base():

    client = pymongo.MongoClient("mongodb+srv://admin:FzM8WTPuY5@cluster0.lgxev.gcp.mongodb.net/test?w=majority")
    db = client.get_database('Locations')

    localisation = db.global_velo

    data = api_velo.send_collection()

    localisation.insert_many(data)

    db.lille_velo.create_index([('Geo','2dsphere')])
    db.global_velo.create_index([('Geo','2dsphere')])

if __name__ == '__main__':
    init_base()
