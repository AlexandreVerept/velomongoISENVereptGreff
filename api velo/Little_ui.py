import del_station_datas
import deactivate_station_in_an_area
import find_with_some_letters
import initbase
import update_single_station
import userprogram
import worker_lille

while True:
    choice = int(input("""Choose what you want to do: \n
    1: Initialise the database \n
    2: Launch the worker for Lille \n
    3: Find near station \n
    4: Find Station with name (only some let \n
    5: Delete a station \n
    6: Deactivate all station in an area \n
    7: Give all stations with a ration bike/total_stand < 20%\n
       between 18h and 19h (Monday to friday) \n"""))
    if choice == 1:
        initbase.init_base() 
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
    elif choice == 4:
        station = str(input("Search a station\n"))
        find_with_some_letters.search(station)
    elif choice == 5:
        _id_station = str(input("Choose the id station you want to remove\n"))
        del_station_datas.delete_station_datas (_id_station)
    elif choice == 6:
        lat = float(input("lat for zone to desactivate ?\n"))
        lon = float(input("lon for zone to desactivate ?\n"))
        dist = int(input("dist for zone to desactivate ?\n"))
        deactivate_zone_location_program(lat,lon,dist)
    elif choice == 7:
        print("to be implemented\n")
