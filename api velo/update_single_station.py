import pymongo
import dns # required for connecting with SRV
import api_velo
import json

def update_station (station, db):
    datas = api_velo.send_collection()
    data = {}
    _id = {}

    for i in datas:
        if i["Name"] == station:
            data = i
            _id["_id"] = data.pop("_id",None)
    
    try:
        db.global_velo.update_one(_id, {"$set": data}, upsert = True)
        return True
    except:
        return False

if __name__ == '__name__':
    with open('client.txt','r') as json_file:
        url = json.load(json_file)
        url = url["url"]
    client = pymongo.MongoClient(url)
    db = client.get_database('Locations')
    station = str(input("_id station to update"))
    update_station(station, db)
