import pymongo
import dns # required for connecting with SRV
import api_velo
import json

def init_base(db):
    """
    Initialise the data base
    """

    localisation = db.global_velo

    data = api_velo.send_collection()

    localisation.insert_many(data)

    db.lille_velo.create_index([('Geo','2dsphere')])
    db.global_velo.create_index([('Geo','2dsphere')])

if __name__ == '__main__':
    with open('client.txt','r') as json_file:
        url = json.load(json_file)
        url = url["url"]
    client = pymongo.MongoClient(url)
    db = client.get_database('Locations')
    init_base()
