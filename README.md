# OpenStreetCam-GeoParsing-Tool
_Created by: Charlie Moffett ( charlie.moffett@nyu.edu )_  
_ARGO team lead: David Marulli ( david@argolabs.org )_


## High-level Description
Create an open-source tool that, given a city, give can pull each OpenStreetCam (OSM) Track file No. associated with that city. Building on existing open-source work (references to come), this will permit the creation ride quality maps of any location with OSM tracks. For a demo, see [here](https://demo.streetsdatacollaborative.org/commute/).

Plan for a launch 1/22/18!

#### Scripts
- `getIntersection.py`: Extracts a list of decimal degree coordinates for each intersection in a given city’s street network from OpenStreetMap. Using Geoff Boeing’s [OSMnx](https://github.com/gboeing/osmnx) Python package, the function generates a NetworkX graph within the administrative GIS boundary for that city before converting the graph nodes (intersections) into a geopandas GeoDataFrame.

- `getNearbytracks.py`: Transforms a single latitude-longitude point into a list of nearby OpenStreetCam sequence_ids within 5km along the street network. Using Kenneth Reitz's [Requests](http://docs.python-requests.org/en/master/) HTTP library, the function sends a POST request to the OSC API and stores the response object in JSON format before gathering any nearby sequence_ids.

- `getAlltracks.py`: Generates the set of sequence_ids for all intersections in a city. By storing OpenStreetCam sequence_ids as an unordered collection of unique elements, the function removes duplicates from the sequence being pulled in by getNearbytracks().

- `getTracksheet.py`: Updates a Google Sheet with all OSM sequence_ids for a given city. Using Anton Burnashev’s [gspread](https://gspread.readthedocs.io/en/latest/) module, the function uses OAuth2 credentials to authorize with the Google Drive API and writes to the spreadsheet by changing specific cells. To programmatically access your spreadsheet, you’ll need to create a service account from the Google API Console.


## Approach

The OSM user interface takes post requests based on lat/lngs and returns nearby-tracks, so defining “city” as points on its street grid may be the most straightforward approach. However, “city” may be defined in whatever way seems technically feasible (rectangular bounding box, polygon boundary file, etc.)

### Skills (or Interests)
python data wrangling + web parsing/scraping (e.g. curl, beautifulsoup, urllib2, etc.)

### Example Screenshots
#### Form Parameters
![post request form](./img/post_req_example_form.png?raw=true "Form Parameters")

#### Response
![post request response](./img/post_req_example_response.png?raw=true "Response")
