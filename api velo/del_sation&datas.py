import pymongo
import dns # required for connecting with SRV
import api_velo

client = pymongo.MongoClient("mongodb+srv://admin:FzM8WTPuY5@cluster0.lgxev.gcp.mongodb.net/test?w=majority")
db = client.get_database('Locations')

def delete_station_datas (_id_station):

    db.global_velo.delete_one( {"_id":_id_station} )

    db.lille_velo.delete_many( {"idstation":_id_station} )
