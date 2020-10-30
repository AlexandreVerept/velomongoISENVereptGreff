# velomongoISENVereptGreff



**Authors:** *Jean-loup Greff ; Alexandre Verept*



### Subject:

Write 4 programs in python and mongo
(1) Get self-services Bicycle Stations (geolocations, size, name, tpe, available): Lille, Lyon, Paris and
Rennes
(2) Worker who refresh and store live data for a city (history data)
(3) User program: give available stations name next to the user lat, lon with last data (bikes and stand)
(4) Business program:

- find station with name (with some letters)

- update a stations

- delete a station and datas

- deactivate all station in an area

- give all stations with a ratio bike/total_stand under 20% between 18h and 19h00 (monday to
  friday)

  Disclaimer: for this last exercice, we did not managed to put the correct UTC while inserting the dates, so we need to check between

### How to launch the project

* Check the url in the `client.txt` to match your cluster mongoAtlas:

  !["url txt"](pictures/url.png)

* Then launch the file `Little_ui.py` in the folder `api velo` in order to choose which part of the project you want to test.

  !["littleUI"](pictures/choseprog.png)

### Our Data base structure:

At first, we have a database named `Locations`

!["databasesmongo"](pictures/databasesmongo.png)

In `Locations`, here are the collections we use:

!["Mongo db tables"](pictures/mongodbtables.png)

An example of station in `global_velo`:

!["globalexamples"](pictures/globalexamples.png)

The `_id` is the result of the concatenation of both the latitude and longitude, as it should be unique for each station.



An example of record in `lille_velo`:

!["lilleexamples"](pictures/lilleexamples.png)

We can link each `lille_velo` record to the corresponding `global_velo` station with the `idstation`.

