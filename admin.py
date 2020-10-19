import pymongo
import time

client = pymongo.MongoClient("mongodb+srv://dbStations:rDvd903tAhvJyOKN@bikedb.ec1dc.gcp.mongodb.net/vls?retryWrites=true&w=majority")
db = client.vls
db.stations.create_index([('geometry', "2dsphere")])
stations = db.stations
data = db.data

def find_station(name):
    query = stations.find({"$regex":'/'+name+'/'})
    available = [{'nom':i.get('name'), 'source': i.get('source')}for i in  query]
    for i in available:
        print(i['nom'])

def update_station(source, key, value):
    query = stations.find_one({'source':source})
    if query == None:
        print('Erreur id')
    else:
        collection.updateOne(query,{"$set":{key:value}})

def delete_station(source):
    query = stations.find_one({'source':source})
    if query == None:
        print('Erreur id')
    else:
        collection.deleteOne(query)

def change_statut(coordinates:list, enabled):
    query = stations.find({'geometry':{"$geometry":{"type":"Polygon","coordinates":coordinates}})
    if query == None:
        print('None')
    else:
        for i in query:
            collection.updateOne(query,{"$set":{"enabled":enabled}})

def stats():
    now = time.time()
    if now[1]==1 and now[2]==1 and now[3]<18:
        year = now[0]-1
    else:
        year = now[0]
    if now[2]==1 and now[3]<18:
        month = now[1]-1
    else:
        month = now[1]
    if now[3]<18:
        day = now[2]-1
    else:
        day = now[2]
    if now[6]==5:
        day -= 1
    if now[6]==6:
        day -= 2
    query = data.find()
    stat = [{'nom':i.get('name'), 'source': i.get('source')} for i in query if ((100*i.get('bike')/i.get('size'))<=20) and (18<=i.get('date')[3]<=19) and (i.get('date')[2]==day) and (i.get('date')[1]==month) and (i.get('date')[0]==year)]
    for i in stat:
        print(i)
