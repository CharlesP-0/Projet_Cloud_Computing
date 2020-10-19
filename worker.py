import stations
import pymongo
import time

client = pymongo.MongoClient("mongodb+srv://dbStations:rDvd903tAhvJyOKN@bikedb.ec1dc.gcp.mongodb.net/vls?retryWrites=true&w=majority")
db = client.vls
collection = db.stations

while True:
    datas = stations.get_bike_lille()
    for d in datas:
        query = collection.find_one({'source':d['source']})
        if query != None:
            collection.update_one(query,{"$set":d})
            print("UPDATE")
        else:
            collection.insert_one(d).inserted_id
            print("INSERT")
    time.sleep(30)
    print("SLEEP")
