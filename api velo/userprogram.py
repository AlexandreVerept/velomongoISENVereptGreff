import pprint
import pymongo
import dns
import json

def location_program(lat,lon,dist=100):
    """
    find all the stations in a certain radius from the user
    """
    # filtre nearby dans global
    found= db.global_velo.find({"Geo": 
                                   {"$near": 
                                    {"$geometry":
                                     {"type": "Point",
                                      "coordinates": [lat, lon]},
                                                     "$maxDistance": dist}}, "Available":"True"})

    if found.count()>0:
        # for each station found, we look for stations in lille by id
        print("Stations found:")
        for f in found:        

            foundLille = db.lille_velo.find({"idstation" : f["_id"]}).sort([("datemaj", -1)]).limit(1)


            for fl in foundLille:
                pprint.pprint(fl)
    else:
        print("No station found")
        
if __name__ == '__main__':
    with open('client.txt','r') as json_file:
        url = json.load(json_file)
        url = url["url"]
    client = pymongo.MongoClient(url)
    db = client.get_database('Locations')
    while True:
        lat = float(input("lat ?"))
        lon = float(input("lon ?"))
        dist = int(input("dist ?"))
        location_program(lat, lon, dist, db)
