import collections
from pprint import pprint

all_elements = collections.OrderedDict()
all_elements["beacon_cardinal"] = [{"k": "seamark:type", "v": "beacon_cardinal", "t": "point"}]
all_elements["beacon_lateral"] = [{"k": "seamark:type", "v": "beacon_lateral", "t": "point"}]
all_elements["beacon_isolated_danger"] = [{"k": "seamark:type", "v": "beacon_isolated_danger", "t": "point"}]
all_elements["beacon_safe_water"] = [{"k": "seamark:type", "v": "beacon_safe_water", "t": "point"}]
all_elements["beacon_special_purpose"] = [{"k": "seamark:type", "v": "beacon_special_purpose", "t": "point"}]

all_elements["buoy_cardinal"] = [{"k": "seamark:type", "v": "buoy_cardinal", "t": "point"}]
all_elements["buoy_lateral"] = [{"k": "seamark:type", "v": "buoy_lateral", "t": "point"}]
all_elements["buoy_isolated_danger"] = [{"k": "seamark:type", "v": "buoy_isolated_danger", "t": "point"}]
all_elements["buoy_safe_water"] = [{"k": "seamark:type", "v": "buoy_safe_water", "t": "point"}]
all_elements["buoy_special_purpose"] = [{"k": "seamark:type", "v": "buoy_special_purpose", "t": "point"}]


all_elements["gate"] = [{"k": "seamark:type", "v": "gate", "t": "point"}]
all_elements["wreck"] = [{"k": "seamark:type", "v": "wreck", "t": "point"}]


all_elements["boom"] = [{"k": "seamark:type", "v": "obstruction", "t": "way"}, {"k": "seamark:obstruction:category", "v": "boom"}]

def printElementsByKey(fullprint = False):
    if fullprint:
        pprint(all_elements)
    else:
        for key in all_elements.keys():
            print(key + " (" + all_elements[key][0]['t'] + ")")
    exit()
    
def downloadOSM(combine = False, elements = []):
    #omit elements to get ALL
    #if not elements:
    print(all_elements)
        
    

#bounds_lat_north = "1.5962442743900633"
#bounds_lat_south = "1.0553144713908544"
#bounds_lon_west = "103.41430664062499"
#bounds_lon_east = "104.315185546875"
#mark_type = 'marine_farm'
#additional_keys = ''
#
##osmurl = 'http://overpass.osm.rambler.ru/cgi/interpreter?data=[out:xml];(way["natural"="water"](' + bounds_lat_south + ',' + bounds_lon_west + ',' + bounds_lat_north + ',' + bounds_lon_east + ');way["seamark:type"="marine_farm"](' + bounds_lat_south + ',' + bounds_lon_west + ',' + bounds_lat_north + ',' + bounds_lon_east + '););(._;>;);out;'
#osmurl = 'http://overpass.osm.rambler.ru/cgi/interpreter?data=[out:xml];way["seamark:type"="marine_farm"](' + bounds_lat_south + ',' + bounds_lon_west + ',' + bounds_lat_north + ',' + bounds_lon_east + ');(._;>;);out;'
#osmfile = mark_type + '_singapore.osm'
#
##urllib.request.urlretrieve(osmurl, osmfile)