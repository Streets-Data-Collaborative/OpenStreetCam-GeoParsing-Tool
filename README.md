# OpenStreetCam-GeoParsing-Tool
_ARGO team lead: David Marulli ( david@argolabs.org )_


## High-level Description
Create an open-source tool that, given a city, give can pull each OpenStreetCam (OSM) Track file No. associated with that city. Building on existing open-source work (references to come), this will permit the creation ride quality maps of any location with OSM tracks. For a demo, see [here](https://demo.streetsdatacollaborative.org/commute/).

Plan for a launch 1/22/18!

## Approach

The OSM user interface takes post requests based on lat/lngs and returns nearby-tracks, so defining “city” as points on its street grid may be the most straightforward approach. However, “city” may be defined in whatever way seems technically feasible (rectangular bounding box, polygon boundary file, etc.)

### Skills (or Interests)
python data wrangling + web parsing/scraping (e.g. curl, beautifulsoup, urllib2, etc.)

### Example Screenshots
#### Form Parameters
![post request form](./img/post_req_example_form.png?raw=true "Form Parameters")

#### Response
![post request response](./img/post_req_example_response.png?raw=true "Response")
