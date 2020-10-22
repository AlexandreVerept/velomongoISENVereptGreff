import pymongo
import dns # required for connecting with SRV
import api_velo

client = pymongo.MongoClient("mongodb+srv://admin:FzM8WTPuY5@cluster0.lgxev.gcp.mongodb.net/test?w=majority")
db = client.get_database('Locations')

localisation = db.global_velo

def update_station (station):
    datas = api_velo.send_collection()
    data = {}
    _id = {}

    for i in datas:
        if i["Name"] == station:
            data = i
            _id["_id"] = data.pop("_id",None)
    
    try:
        localisation.update_one(_id, {"$set": data}, upsert = True)
        return True
    except:
        return False

if __name__ == '__name__':
    station = str(input("_id station to update"))
    update_station(station)
