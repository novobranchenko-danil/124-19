import sys
import console_handler as ch
from math import radians, sin, cos, sqrt, asin


def dd_to_dms(latitude, longitude):
    '''
    @requires: latitude, longitude are float/int coordinates in decimal degrees
               latitude between -90 and 90
               longitude between -180 and 180
    @modifies: None
    @effects:  converts decimal degrees coordinates to degrees-minutes-seconds format
    @returns:  tuple of two strings: (latitude_dms, longitude_dms)
               format: "DDD°MM'SS.SS"[N/S/E/W]
    '''
    def convert(coord, for_latitude):
        if for_latitude:
            pos_dir, neg_dir = 'N', 'S'
        else:
            pos_dir, neg_dir = 'E', 'W'

        direction = pos_dir if coord >= 0 else neg_dir
        coord = abs(coord)

        degrees = int(coord)
        minutes_decimal = (coord - degrees) * 60
        minutes = int(minutes_decimal)
        seconds = (minutes_decimal - minutes) * 60

        return f"{degrees:03d}°{minutes:02d}'{seconds:05.2f}\"{direction}"

    lat_str = convert(latitude, True)
    lon_str = convert(longitude, False)

    return lat_str, lon_str


def handle_special_commands(command):
    if command == "end":
        ch.print_end()
        sys.exit()
    elif command == "return":
        return True
    return False


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
