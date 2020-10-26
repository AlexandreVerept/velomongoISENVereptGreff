import pymongo
import dns # required for connecting with SRV

client = pymongo.MongoClient("mongodb+srv://admin:FzM8WTPuY5@cluster0.lgxev.gcp.mongodb.net/test?w=majority")
db = client.get_database('Locations')
db.global_velo.create_index([('Name','text')])

def search(station):
    """
    search for a station by name with only some letters or part of the name
    """
    cur = db.global_velo.find({"Name": {"$regex": station, "$options": "i" }})
    for doc in cur:
        print(doc)

if __name__ == '__name__':
    station = str(input("Search a station"))
    search(station)
