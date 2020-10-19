import requests
import json

def get_bike_lille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET",url)
    response_json = json.loads(response.text.encode('utf8'))
    bike = response_json.get("records", [])
    bike_to_insert = [
        {
            'name': elem.get('fields', {}).get('nom', '').title(),
            'geometry': elem.get('geometry'),
            'size': elem.get('fields', {}).get('nbvelosdispo') + elem.get('fields', {}).get('nbplacesdispo'),
            'source': {
                'dataset': 'Lille',
                'id_ext': elem.get('fields', {}).get('libelle')
            },
            'enabled': elem.get('fields', {}).get('etat', '') == 'EN SERVICE'
            'tpe': elem.get('fields', {}).get('type', '') == 'AVEC TPE'
        }
        for elem in bike
    ]
    return bike_to_insert

def get_bike_paris():
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=-1&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"
    response = requests.request("GET",url)
    response_json = json.loads(response.text.encode('utf8'))
    bike = response_json.get("records", [])
    bike_to_insert = [
        {
            'name': elem.get('fields', {}).get('name', '').title(),
            'geometry': elem.get('geometry'),
            'size': elem.get('fields', {}).get('numdocksavailable'),
            'source': {
                'dataset': 'Paris',
                'id_ext': elem.get('fields', {}).get('stationcode')
            },
            'tpe': True
        }
        for elem in bike
    ]
    return bike_to_insert

def get_bike_lyon():
    url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=station-velov-grand-lyon&q=&rows=-1&facet=name&facet=commune&facet=status&facet=available&facet=availabl_1&facet=availabili&facet=availabi_1&facet=last_upd_1"
    response = requests.request("GET",url)
    response_json = json.loads(response.text.encode('utf8'))
    bike = response_json.get("records", [])
    bike_to_insert = [
        {
            'name': elem.get('fields', {}).get('name', '').title(),
            'geometry': elem.get('geometry'),
            'size': elem.get('fields', {}).get('bike_stand'),
            'source': {
                'dataset': 'Lyon',
                'id_ext': elem.get('fields', {}).get('number')
            },
            'tpe': elem.get('fields', {}).get('banking', '') == 't'
        }
        for elem in bike
    ]
    return bike_to_insert

def get_bike_rennes():
    url = "https://data.explore.star.fr/api/records/1.0/search/?dataset=vls-stations-etat-tr&q=&rows=-1&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
    response = requests.request("GET",url)
    response_json = json.loads(response.text.encode('utf8'))
    bike = response_json.get("records", [])
    bike_to_insert = [
        {
            'name': elem.get('fields', {}).get('nom', '').title(),
            'geometry': elem.get('geometry'),
            'size': elem.get('fields', {}).get('nombreemplacementsactuels'),
            'source': {
                'dataset': 'Rennes',
                'id_ext': elem.get('fields', {}).get('idstation')
            },
            'tpe': True
        }
        for elem in bike
    ]
    return bike_to_insert

datas = stations.get_bike_lille()
    for d in datas:
        query = collection.find_one({'source':d['source']})
        if query == None:
            collection.insert_one(d).inserted_id
            print("INSERT")
