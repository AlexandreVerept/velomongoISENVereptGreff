import pymongo
import dns # required for connecting with SRV
import json

def search(station, db):
    """
    search for a station by name with only some letters or part of the name
    """
    cur = db.global_velo.find({"Name": {"$regex": station, "$options": "i" }})
    for doc in cur:
        print(doc)

if __name__ == '__name__':
    with open('client.txt','r') as json_file:
        url = json.load(json_file)
        url = url["url"]
    client = pymongo.MongoClient(url)
    db = client.get_database('Locations')
    station = str(input("Search a station"))
    search(station, db)
