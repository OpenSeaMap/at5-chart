import shapefile
import xml.etree.ElementTree as ET
import argparse

from functions4points import *

#thefile = ET.parse('../Assets/2014-04-11-wrecks_singapore/wrecks_singapore.osm')
#thefile = ET.parse('../Assets/2014-04-10-buoy_lateral_singapore/buoy_lateral_singapore.osm')
#thefile = ET.parse('../Assets/points/2014-04-11-gates_singapore/gates_singapore.osm')
#thefile = ET.parse('../Assets/points/2014-04-11-buoy_special_purpose_singapore/buoy_special_purpose_singapore.osm')
#thefile = ET.parse('../Assets/points/2014-04-11-buoy_safe_water_singapore/buoy_safe_water_singapore.osm')
#thefile = ET.parse('../Assets/points/2014-04-11-buoy_isolated_danger_singapore/buoy_isolated_danger_singapore.osm')
#thefile = ET.parse('../Assets/points/2014-04-11-buoy_cardinal_singapore/buoy_cardinal_singapore.osm')
#thefile = ET.parse('../Assets/points/2014-04-11-beacon_special_purpose_singapore/beacon_special_purpose_singapore.osm')
#thefile = ET.parse('../Assets/points/2014-04-11-beacon_safe_water_singapore/beacon_safe_water_singapore.osm')
#thefile = ET.parse('../Assets/points/2014-04-11-beacon_isolated_danger_singapore/beacon_isolated_danger_singapore.osm')

parser = argparse.ArgumentParser(description='Python tool to get OSM/OSeaM data via the Overpass API and convert that data to an ESRI Shapefile that is readable by IMC (Lowrance\'s/Navico\'s Insight Map Creator). [Requires shapefile library to be installed: pip install shapefile]')
parser.add_argument('-a', '--all', action='store_true', help='Download/Process all nodes/ways/areas that are recognised by this program. (Default: yes)', required=False)
parser.add_argument('-d', '--download', action='store_true', help='Only download data from the Overpass API from Overpass API and do NOT process. (Default: no)', required=False)
parser.add_argument('--local', nargs='*', metavar='FILENAME', help='Use local files (separated by spaces) as OSM/OSeaM data instead of the Overpass API. No download is performed. Shapefile names follow the local file names. If no path is specified, all .osm files in current directory are processed. (Default: no)', required=False)
parser.add_argument('--oapi', nargs='?', metavar='URL', help='Specify which Overpass API to use. (Default: "http://overpass.osm.rambler.ru/cgi/interpreter")', required=False, default="http://overpass.osm.rambler.ru/cgi/interpreter")
parser.add_argument('-o', '--output', nargs='?', metavar='/PATH/TO/DIRECTORY/', help='Specify where downloaded/processed files are sent. If no path is specified, default to current directory unless --local is used in which case it defaults to wherever those files are. (Default: <Current Directory or LocalFile Directory>)', required=False, default="./")
parser.add_argument('--rules', nargs='?', metavar='RULES_FILENAME', help='<NOT CURRENTLY IMPLEMENTED>If file specified, use a specific rules file. If no file specified, will use rules.ini in the current working directory. If this option is not present, will use internal rules. (Default: no)', default='rules.ini', required=False)
parser.add_argument('--elements', nargs='+', metavar='"key"="value"', help='<NOT CURRENTLY IMPLEMENTED> Space separated list of specific elements to download/process (as opposed to --all). Will accept nested selections e.g. (("seamark:type"="buoy_lateral"),("seamark:category:buoy_lateral"="port")). If --all is set this becomes a negation?', default='', required=False)
parser.add_argument('-b', '--bounds', nargs=4, help='Specify the bounds from which data is retrieved (NOT processed) in the form of degrees minutes.decimalMinutes as <North South East West>/<latMax latMin lonMin lonMax>. Defaults to 1.5962442743900633 1.0553144713908544 103.41430664062499 104.315185546875, which is roughly the bounds of Singapore.', metavar=('NORTH', 'SOUTH', 'EAST', 'WEST'), required=False, default="1.5962442743900633 1.0553144713908544 103.41430664062499 104.315185546875")
parser.add_argument('-v', '--verboose', action='store_true', help='Verboose output. Says what element it is currently on. (Default: no)', required=False)
parser.add_argument('--combine-osm', action='store_true', help='If downloading data via Overpass API, and if this is used, data will be stored in 1 to 3 osm files (points, ways/polylines, and areas/polygons are separated). (Default: no)', required=False)
parser.add_argument('--combine-shp', action='store_true', help='If processing data, and if this is used, shapfiles will be stored in 1 to 3 files (points, ways/polylines, and areas/polygons are separated). (Default: no)', required=False)
parser.add_argument('--list-elements', action='store_true', help='List elements currently supported by this program, by internal name', required=False)
parser.add_argument('--list-elements-debug', action='store_true', help='List elements currently supported by this program, as a pprint dump of the elements dictionary.', required=False)

args = parser.parse_args()
(files, verboosity) = handleArgs(args)
    
exit()


thefile = ET.parse('../Assets/points/2014-04-11-beacon_cardinal_singapore/beacon_cardinal_singapore.osm')
root = thefile.getroot()

w = shapefile.Writer(shapefile.POINT)
w.field('x', 'N')
w.field('y', 'N')
w.field('id', 'N')
w.field('L_LIMIT', 'N', 50, 0)
w.field('U_LIMIT', 'N')
w.field('COLOR', 'N')
w.field('RTP_COLOR', 'N')
w.field('RTP_LIMIT', 'N')
w.field('WIDTH', 'N')
w.field('FONT', 'N')
w.field('LAYER', 'N')
w.field('MODE')
w.field('INFO_BOX')
w.field('VALUE')
w.field('MAJ_CAT')
w.field('MIN_CAT')
w.field('ICON')
w.field('P_ICON')




points = []
for child in root:
    point = {}
    if child.tag == "node":
        point['id'] = child.attrib['id'];
        point['x'] = child.attrib['lon'];
        point['y'] = child.attrib['lat'];
        
        for subchild in child:
            if subchild.tag == "tag":
                if subchild.attrib['k'].lower() == "seamark:type":
                    point['stype'] = subchild.attrib['v'].lower()
                else:
                    point[subchild.attrib['k'].lower()] = subchild.attrib['v'].lower()
        
        #print(child.attrib['lat']);
        points.append(point)


for point in points:
    if point['stype'] == "wreck":
        w = handleWrecks(point, w)
    elif point['stype'] == "buoy_lateral":
        w = handleBuoyLateral(point, w)
    elif point['stype'] == "gate":
        w = handleGates(point, w)
    elif point['stype'] == "buoy_special_purpose":
        w = handleBuoySpecialPurpose(point, w)
    elif point['stype'] == "buoy_safe_water":
        w = handleBuoySafeWater(point, w)
    elif point['stype'] == "buoy_isolated_danger":
        w = handleBuoyIsolatedDanger(point, w)
    elif point['stype'] == "buoy_cardinal":
        w = handleBuoyCardinal(point, w)
    elif point['stype'] == "beacon_cardinal":
        w = handleBeaconCardinal(point, w)
    elif point['stype'] == "beacon_isolated_danger":
        w = handleBeaconIsolatedDanger(point, w)
    elif point['stype'] == "beacon_safe_water":
        w = handleBeaconSafeWater(point, w)
    elif point['stype'] == "beacon_special_purpose":
        w = handleBeaconSpecialPurpose(point, w)



#w.save('wrecks_singapore')
#w.save('buoy_lateral_singapore')
#w.save('gates_singapore')
#w.save('../Assets/points/2014-04-11-buoy_special_purpose_singapore/buoy_special_purpose_singapore')
#w.save('../Assets/points/2014-04-11-buoy_safe_water_singapore/buoy_safe_water_singapore')
#w.save('../Assets/points/2014-04-11-buoy_isolated_danger_singapore/buoy_isolated_danger_singapore')
#w.save('../Assets/points/2014-04-11-buoy_cardinal_singapore/buoy_cardinal_singapore')
#w.save('../Assets/points/2014-04-11-beacon_special_purpose_singapore/beacon_special_purpose_singapore')
#w.save('../Assets/points/2014-04-11-beacon_safe_water_singapore/beacon_safe_water_singapore')
#w.save('../Assets/points/2014-04-11-beacon_isolated_danger_singapore/beacon_isolated_danger_singapore')
#w.save('../Assets/points/2014-04-11-beacon_cardinal_singapore/beacon_cardinal_singapore')

