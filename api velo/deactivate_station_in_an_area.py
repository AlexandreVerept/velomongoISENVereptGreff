import pymongo
import dns

client = pymongo.MongoClient("mongodb+srv://admin:FzM8WTPuY5@cluster0.lgxev.gcp.mongodb.net/test?w=majority")
db = client.get_database('Locations')


def deactivate_zone(lat,lon,dist):
    """
    deactivate all stations in a select area
    """
    # filtre nearby dans global
    found= db.global_velo.find({"Geo": 
                                   {"$near": 
                                    {"$geometry":
                                     {"type": "Point",
                                      "coordinates": [lat, lon]},
                                                     "$maxDistance": dist}}, "Available":"True"})
    for i in found:
        db.global_velo.update_one(i["_id"], {"$set": {"Available": "False"}}, upsert = True)


if __name__ == '__main__':
    while True:
        lat = float(input("lat for zone to desactivate ?"))
        lon = float(input("lon for zone to desactivate ?"))
        dist = int(input("dist for zone to desactivate ?"))
        deactivate_zone(lat,lon,dist)
