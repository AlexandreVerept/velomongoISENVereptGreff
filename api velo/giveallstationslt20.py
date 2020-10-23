from datetime import datetime
from datetime import timedelta
import time
import pprint
import pymongo
import dns

client = pymongo.MongoClient("mongodb+srv://admin:FzM8WTPuY5@cluster0.lgxev.gcp.mongodb.net/test?w=majority")
db = client.get_database('Locations')



hourStart = 15
hourEnd = 16
jours = 7



#get the day x day before at 17:59
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