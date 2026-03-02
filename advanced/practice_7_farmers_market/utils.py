from math import radians, sin, cos, sqrt, asin


def get_distance(lat1, lon1, lat2, lon2):
    '''
    @requires: lat1, lon1, lat2, lon2 are float coordinates in decimal degrees
               uses Haversine formula for spherical Earth
    @modifies: None
    @effects:  calculates great-circle distance between two geographic points
    @returns:  float distance in miles (Earth radius = 3959 miles)
    '''
    R = 3959
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c
