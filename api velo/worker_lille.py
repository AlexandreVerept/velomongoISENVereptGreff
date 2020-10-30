import pymongo
import dns # required for connecting with SRV
import time
import api_velo
import json

def launch_worker_Lille(db):
    """
    This worker add the new records to "lille_velo" with the live data every minute
    """
    while True:
        datas = api_velo.send_live()
        for data in datas:
            # test if a station is delete
            if db.global_velo.find({"_id":data["idstation"]}).limit(1).count(True) == 1:
                db.lille_velo.insert_one(data)
        time.sleep(50)

if __name__ == '__main__':
    with open('client.txt','r') as json_file:
        url = json.load(json_file)
        url = url["url"]
    client = pymongo.MongoClient(url)
    db = client.get_database('Locations')
    launch_worker_Lille(db)
