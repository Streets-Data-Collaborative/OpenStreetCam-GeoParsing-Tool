url = 'http://openstreetcam.org/nearby-tracks'
sequence_ids = []

def getNearbytracks(lat, lng):
    '''
    Takes lat and lng as strings and
    returns nearby OSC tracks as a list
    of sequence_ids.
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