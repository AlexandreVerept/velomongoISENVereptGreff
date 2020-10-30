from datetime import datetime
from datetime import timedelta
import pprint
import pymongo
import dns
import json

def get_stations_under20(db, jours=7,hourStart = 15,hourEnd = 16):
    """
    Print the _id of each stations that have a bike/total_stand ratio smaller than 20% in the last x days (excluding the week-ends)
    
    parameters:
        jour : (int) number of days we want to consider
    
    You can find the complete process behind our long querry in our tests made with Jupyter Notebook
    """

    #get the day x day before
    start = datetime.now()
    end = (start - timedelta(days=jours)).replace(hour=0, minute=59,second=59)
    
    found = db.lille_velo.aggregate([
        {"$project":
         
         {"hour":
          {"$hour":"$datemaj"
          },
          
          "datemaj":"$datemaj",
          
          "idstation":"$idstation",
          
          "weekDay":{"$dayOfWeek":"$datemaj"
          },
          
          "ratio": 
          {"$cond":
        [
            {'$gt':
             [
                 {"$add":
                  ["$availableplaces","$availbalebike"]
                 },
                 0
             ]},
             {"$divide" : 
              ["$availbalebike", 
               {"$add":["$availableplaces","$availbalebike"]}
              ]
             },
             0
            ]}
         }
    
         
        },
        {"$match":
         {"hour":
          {"$in":[hourStart,hourEnd]},
          "datemaj":
          {'$gte': end, '$lt': start},
          "weekDay":{'$gte': 2, '$lte': 6}
         }
        },
        
        {
            "$group" :
            {
              "_id" : "$idstation",
              "station_ratio": { "$avg": "$ratio"}
            }
        },
        {"$match":
         {"station_ratio":{'$lte': 0.2}
         }
        }
        
        
    ])
    
    for f in found:
        pprint.pprint(f)
    
if __name__ == '__main__':
    with open('client.txt','r') as json_file:
        url = json.load(json_file)
        url = url["url"]
    client = pymongo.MongoClient(url)
    db = client.get_database('Locations')
    get_stations_under20(db)
