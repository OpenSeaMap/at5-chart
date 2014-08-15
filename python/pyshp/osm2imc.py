import shapefile
import xml.etree.ElementTree as ET
import argparse

from functions4points import *

def handleArgs(args):
    if args.list_elements_debug:
        printElementsByKey(True)
        return (None)
    elif args.list_elements:
        printElementsByKey(False)
        return (None)
    
    osmfiles = []
    if type(args.local) is list:
        if len(args.local) > 0:
            if args.verboose:
                print ("Local files option detected. Will process local files as specified.")
            for eachfile in args.local:
                if os.path.isdir(eachfile.strip('"\'').rstrip("\\")):
                    osmfiles.extend(getOSMFilesInDir(eachfile.strip('"\'').rstrip("\\")))
                else:
                    osmfiles.append(eachfile);
        else:
            if args.verboose:
                print ("Local files option detected. Will process local files in current directory.")
            osmfiles.extend(getOSMFilesInDir())
    else:
        if len(args.elements) > 0:
            eles = args.elements
        else:
            eles = []
        
        if args.all:
            eles = []
        
        osmfiles.extend(downloadOSM(args.oapi, "./", args.bounds, True, True, False, eles))
    
    if args.download:
        return (None)
    else:
        processOSMFiles(osmfiles, args.verboose)
    #
    #print(args.elements)
    ##print(args)
    ##downloadOSM(False)
    return (None, args.verboose)



parser = argparse.ArgumentParser(description='Python tool to get OSM/OSeaM data via the Overpass API and convert that data to an ESRI Shapefile that is readable by IMC (Lowrance\'s/Navico\'s Insight Map Creator). [Requires shapefile library to be installed: pip install shapefile]')
parser.add_argument('-a', '--all', action='store_true', help='Download/Process all nodes/ways/areas that are recognised by this program. (Default: yes)', required=False)
parser.add_argument('-d', '--download', action='store_true', help='Only download data from the Overpass API from Overpass API and do NOT process. (Default: no)', required=False)
parser.add_argument('--local', nargs='*', metavar='FILENAME', help='Use local files (separated by spaces) as OSM/OSeaM data instead of the Overpass API. No download is performed. Shapefile names follow the local file names. If no path is specified, all .osm files in current directory are processed. (Default: no)', required=False)
parser.add_argument('--oapi', nargs='?', metavar='URL', help='Specify which Overpass API to use. (Default: "http://overpass.osm.rambler.ru/cgi/interpreter")', required=False, default="http://overpass.osm.rambler.ru/cgi/interpreter")
parser.add_argument('-o', '--output', nargs='?', metavar='/PATH/TO/DIRECTORY/', help='Specify where downloaded/processed files are sent. If no path is specified, default to current directory unless --local is used in which case it defaults to wherever those files are. (Default: <Current Directory or LocalFile Directory>)', required=False, default="./")
parser.add_argument('--rules', nargs='?', metavar='RULES_FILENAME', help='<NOT CURRENTLY IMPLEMENTED>If file specified, use a specific rules file. If no file specified, will use rules.ini in the current working directory. If this option is not present, will use internal rules. (Default: no)', default='rules.ini', required=False)
parser.add_argument('--keys', nargs='+', metavar='"key"="value"', help='<NOT CURRENTLY IMPLEMENTED> Space separated list of specific elements based on keys to download/process (as opposed to --all). Will accept nested selections e.g. (("seamark:type"="buoy_lateral"),("seamark:category:buoy_lateral"="port")). If --all is set this becomes a negation?', default='', required=False)
parser.add_argument('--elements', nargs='+', metavar='value', help='Space separated list of specific elements to download/process (as opposed to --all). If --all is set this becomes a negation?', default='', required=False)
parser.add_argument('-b', '--bounds', nargs=4, help='Specify the bounds from which data is retrieved (NOT processed) in the form of degrees minutes.decimalMinutes as <North South East West>/<latMax latMin lonMin lonMax>. Defaults to 1.5962442743900633 1.0553144713908544 103.41430664062499 104.315185546875, which is roughly the bounds of Singapore.', metavar=('NORTH', 'SOUTH', 'EAST', 'WEST'), required=False, default=[1.5962442743900633, 1.0553144713908544, 103.41430664062499, 104.315185546875])
parser.add_argument('-v', '--verboose', action='store_true', help='Verboose output. Says what element it is currently on. (Default: no)', required=False)
parser.add_argument('--combine-osm', action='store_true', help='If downloading data via Overpass API, and if this is used, data will be stored in 1 to 3 osm files (points, ways/polylines, and areas/polygons are separated). (Default: no)', required=False)
parser.add_argument('--combine-shp', action='store_true', help='If processing data, and if this is used, shapfiles will be stored in 1 to 3 files (points, ways/polylines, and areas/polygons are separated). (Default: no)', required=False)
parser.add_argument('--list-elements', action='store_true', help='List elements currently supported by this program, by internal name', required=False)
parser.add_argument('--list-elements-debug', action='store_true', help='List elements currently supported by this program, as a pprint dump of the elements dictionary.', required=False)

args = parser.parse_args()
(files, verboosity) = handleArgs(args)