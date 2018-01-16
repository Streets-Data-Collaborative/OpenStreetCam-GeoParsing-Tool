import osmnx as ox
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
    try:
        sequences = extract['osv']['sequences']
        for i in range(len(sequences)):
            sequence_ids.append(sequences[i]['sequence_id'])
    except TypeError:
        pass
    return sequence_ids

def getAlltracks(city, state, country):
    '''
    This function takes a city's name as an input, and 
    returns a list of all `sequence_id`s from that city.
    city: str
    state: str
    country: str
    '''
    city_sids = set()
    for lat, lng in getIntersection(city, state, country):
        tempTracks = getNearbytracks(lat, lng)
        for x in tempTracks: city_sids.add(x)
    return city_sids

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
keyfile = 'xxxxx_xxxx.json' ## replace with JSON keyfile name
creds = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)
client = gspread.authorize(creds)
 
# find a workbook by name and open the first sheet
workbook = 'XXXXXXXXX' ## replace with Google Sheets filename
sheet = client.open(workbook).sheet1

# print city track sequence IDs to SQUID Uploader
def getTracksheet(city, state, country):
    tracklist = list(getAlltracks('Sand City', 'California', 'USA'))
    for i in range(len(tracklist)):
        sheet.update_cell(i+2, 1, tracklist[i])
    for i in range(len(tracklist)):
        sheet.update_cell(i+2, 2, city)