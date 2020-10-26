import del_station_datas
import pymongo
import deactivate_station_in_an_area
import find_with_some_letters
import initbase
import update_single_station
import userprogram
import worker_lille
import giveallstationslt20
import json

def make_choice():
    """
    Allow you to launch every scripts corresponding to all the exercices
    """
    with open('client.txt','r') as json_file:
        url = json.load(json_file)
        url = url["url"]
    client = pymongo.MongoClient(url)
    db = client.get_database('Locations')
    
    
    choice = int(input("""Choose what you want to do: \n
    1: Initialise the database \n
    2: Launch the worker for Lille \n
    3: Find the nearests stations \n
    4: Find Station with name (only some letters) \n
    5: Delete a station \n
    6: Update a station \n
    7: Deactivate all station in an area \n
    8: Give all stations with a ration bike/total_stand < 20%\n
       between 18h and 19h (Monday to friday) in the last x days \n"""))

    
    
    if choice == 1:
        initbase.init_base(db) 
        
    elif choice == 2:
        try:
            worker_lille.launch_worker_Lille()
        except:
            print("You leave the worker\n")
            
    elif choice == 3:
        print("Give your coordinate")
        lat = float(input("lat ?\n"))
        lon = float(input("lon ?\n"))
        dist = int(input("dist ?\n"))
        userprogram.location_program(lat, lon, dist)
        
    elif choice == 4:
        station = str(input("Search a station\n"))
        find_with_some_letters.search(station, db)

    elif choice == 5:
        station = str(input("Choose the id station you want to update\n"))
        update_single_station.update_station(station, db)
    
    elif choice == 6:
        _id_station = str(input("Choose the id station you want to remove\n"))
        del_station_datas.delete_station_datas (_id_station, db)
        
    elif choice == 7:
        lat = float(input("lat for zone to desactivate ?\n"))
        lon = float(input("lon for zone to desactivate ?\n"))
        dist = int(input("dist for zone to desactivate ?\n"))
        deactivate_station_in_an_area.deactivate_zone(lat, lon, dist, db)
        
    elif choice == 8:
        print("Here are the stations with a ratio bike/total_stand smaller than 20% in the last week:")
        giveallstationslt20.get_stations_under20(db)

if __name__ == '__main__':
    while True:
        make_choice()
