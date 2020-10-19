import pymongo
import time

client = pymongo.MongoClient("mongodb+srv://dbStations:rDvd903tAhvJyOKN@bikedb.ec1dc.gcp.mongodb.net/vls?retryWrites=true&w=majority")
db = client.vls
collection = db.data

while True:
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET",url)
    response_json = json.loads(response.text.encode('utf8'))
    bike = response_json.get("records", [])
    bike_to_insert = [
        {
            'date': time.time()
            'bike': elem.get('fields', {}).get('nbvelosdispo'),
            'stand': elem.get('fields', {}).get('nbplacesdispo')
            'source': {
                'dataset': 'Lille',
                'id_ext': elem.get('fields', {}).get('libelle')
            }
        }
        for elem in bike
    ]

    for d in bike_to_insert:
        collection.insert_one(d).inserted_id
    time.sleep(30)
