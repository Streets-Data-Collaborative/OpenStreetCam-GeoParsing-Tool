import osmnx as ox
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def getIntersection(city, state, country):
    '''
    This function takes a city, state, and country as inputs
    and returns a list of lat/long pairs
    for each intersection of the city street network.
    '''
    place = (city + ", " + state + ", " + country)
    
    # Create a networkx graph from OSM data within the spatial boundaries of some geocodable place
    G = ox.graph_from_place(place)
    
    # Save graph nodes as a GeoDataFrame
    nodes_gdf = ox.save_load.graph_to_gdfs(G, edges=False, node_geometry=False)
    
    # Output list of lng/lat pairs
    nodes_list = nodes_gdf[['x', 'y']].to_records(index=False).tolist()
    
    return nodes_list

url = 'http://openstreetcam.org/nearby-tracks'
sequence_ids = []

def getNearbytracks(lat, lng):
    '''
    This function takes a decimal degree latitude/longitude 
    pair as two strings and returns nearby OpenStreetCam 
    tracks as a list of sequence_ids.
    '''
    # form data to be sent to API
    data = {'lat': lat, 'lng': lng, 'distance': '5.0',
           'myTracks': 'false', 'filterUserNames': 'false'}
        
    # sending post request and saving response as response object
    r = requests.post(url=url, data=data)
        
    # extracting data in json format
    extract = r.json()
    
    # if nearby tracks exist, store them in a list
    try:
        sequences = extract['osv']['sequences'] # indexes post request json with nearby tracks
        for i in range(len(sequences)): 
            sequence_ids.append(sequences[i]['sequence_id'])
    except:
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
    # store as unordered collection of unique elements
    city_sids = set()
    
    # loop through coordinates in city street network
    for lat, lng in getIntersection(city, state, country):
        tempTracks = getNearbytracks(lat, lng)
        for x in tempTracks: city_sids.add(x)
            
    return city_sids

# requires a service account and OAuth2 credentials from the Google API Console
# enable Google Drive API and download application data as a JSON keyfile
keyfile = 'xxxxx_xxxx.json' ## replace with JSON keyfile name
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)

# creates a client to interact with the Google Drive API
client = gspread.authorize(creds)
 
# finds a workbook by name and opens the first sheet
workbook = 'XXXXXXXXX' ## replace with Google Sheets filename
sheet = client.open(workbook).sheet1

# print city track sequence IDs to SQUID Uploader
def getTracksheet(city, state, country):
    '''
    This function takes city, state, and country as input
    and pushes each OSC sequence_id within the street network
    as a new record to a given Google Sheet.
    '''
    # store set of sequence_ids as list
    tracklist = list(getAlltracks('Sand City', 'California', 'USA'))
    
    # update Sheet with elements of sequence_id list
    for i in range(len(tracklist)):
        sheet.update_cell(i+2, 1, tracklist[i])
        
    # update Sheet with city name for each sequence_id
    for i in range(len(tracklist)):
        sheet.update_cell(i+2, 2, city)