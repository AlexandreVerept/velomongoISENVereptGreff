import pymongo
import dns # required for connecting with SRV
import time
import api_velo
import json

def launch_worker_Lille():
    """
    This worker add the new records to "lille_velo" with the live data every minute
    """
    while True:
        data = api_velo.send_live()
        db.lille_velo.insert_many(data, ordered=True)
        time.sleep(60)

if __name__ == '__main__':
    with open('client.txt','r') as json_file:
        url = json.load(json_file)
        url = url["url"]
    client = pymongo.MongoClient(url)
    db = client.get_database('Locations')
    launch_worker_Lille()
