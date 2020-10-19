import stations
import pymongo
import pprint

client = pymongo.MongoClient("mongodb+srv://dbStations:rDvd903tAhvJyOKN@bikedb.ec1dc.gcp.mongodb.net/vls?retryWrites=true&w=majority")
db = client.vls
db.stations.create_index([('geometry', "2dsphere")])
collection = db.stations

def get_available_stations_near(lat, long, dist = 165):
    query = db.stations.find({'geometry': {"$near": {"$geometry": {'type': "Point" ,'coordinates': [ long, lat ]},"$maxDistance": dist,"$minDistance": 0}}})
    available = [{'nom':i.get('name')}for i in  query]
    for i in available:
        print(i['nom'])
