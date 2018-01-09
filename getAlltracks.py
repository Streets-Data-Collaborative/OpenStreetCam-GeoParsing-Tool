import osmnx as ox
import requests

def getIntersection(city, state, country):
    place = (city + ", " + state + ", " + country)
    G = ox.graph_from_place(place)
    nodes_gdf = ox.save_load.graph_to_gdfs(G, edges=False, node_geometry=False)
    nodes_list = nodes_gdf[['y', 'x']].to_records(index=False).tolist()
    return nodes_list

url = 'http://openstreetcam.org/nearby-tracks'
sequence_ids = []

def getNearbytracks(lat, lng):
    data = {'lat': lat, 'lng': lng, 'distance': '5.0', 'myTracks': 'false', 'filterUserNames': 'false'}
    r = requests.post(url=url, data=data)
    extract = r.json()
    for i in range(len(extract)):
        try:
            sequence_ids.append(extract['osv']['sequences'][i]['sequence_id'])
        except:
            pass
    return sequence_ids

def getAlltracks(city, state, country):
    city_sids = set()
    for lat, lng in getIntersection(city, state, country):
        lat = str(lat)
        lng = str(lng)
        tempTracks = getNearbytracks(lat, lng)
        for x in tempTracks: city_sids.add(x)
    return city_sids