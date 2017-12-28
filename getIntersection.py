def getIntersection(city, state, country):
    '''Takes a city, state, and country as strings
    and returns a list of lat/long pairs
    for each intersection of the city street network.'''
    place = (city + ", " + state + ", " + country)
    
    # Create a networkx graph from OSM data within the spatial boundaries of some geocodable place
    G = ox.graph_from_place(place)
    
    # Save graph nodes as a GeoDataFrame
    nodes_gdf = ox.save_load.graph_to_gdfs(G, edges=False, node_geometry=False)
    
    # Output list of lng/lat pairs
    nodes_list = nodes_gdf[['x', 'y']].to_records(index=False).tolist()
    
    return nodes_list