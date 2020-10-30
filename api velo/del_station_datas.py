import pymongo
import dns # required for connecting with SRV
import json

def delete_station_datas (_id_station, db):
    """
    delete a station by "_id" in "global_velo" and all the corresponding records in 'lille_velo'
    """

    db.global_velo.delete_one( {"_id":_id_station} )

    db.lille_velo.delete_many( {"idstation":_id_station} )

if __name__ == '__main__':
    with open('client.txt','r') as json_file:
        url = json.load(json_file)
        url = url["url"]
    client = pymongo.MongoClient(url)
    db = client.get_database('Locations')
    _id_station = str(input("Choose the id station you want to remove"))
    delete_station_datas (_id_station, db)
