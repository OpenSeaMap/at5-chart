import shapefile
import xml.etree.ElementTree as ET
import urllib.request

bounds_lat_north = "1.5962442743900633"
bounds_lat_south = "1.0553144713908544"
bounds_lon_west = "103.41430664062499"
bounds_lon_east = "104.315185546875"
mark_type = "obstruction"
additional_keys = ''

osmurl = 'http://overpass.osm.rambler.ru/cgi/interpreter?data=[out:xml];way["seamark:type"="' + mark_type + '"]' + additional_keys + '(' + bounds_lat_south + ',' + bounds_lon_west + ',' + bounds_lat_north + ',' + bounds_lon_east + ');(._;>;);out;'
osmfile = mark_type + '_singapore.osm'

#urllib.request.urlretrieve(osmurl, osmfile)

thefile = ET.parse(osmfile)
root = thefile.getroot()

nodes = {}
for child in root:
    node_attribs = {}
    if child.tag == "node":
        node_attribs['x'] = child.attrib['lon']
        node_attribs['y'] = child.attrib['lat']
        nodes[child.attrib['id']] = node_attribs


ways = []
for child in root:
    way = {}
    cnodes = []
    if child.tag == "way":
        way['id'] = child.attrib['id'];
        
        for subchild in child:
            if subchild.tag == "tag":
                if subchild.attrib.get('k', '').lower() == "seamark:type":
                    way['stype'] = subchild.attrib['v'].lower()
                else:
                    way[subchild.attrib.get('k', '').lower()] = subchild.attrib['v'].lower()
            elif subchild.tag == "nd":
                cnodes.append(subchild.attrib['ref'])
            
        way['cnodes'] = cnodes
        
        ways.append(way)
        

def handleObstructionBoom(way, nodes, w):
    wayparts = []
    for node in way['cnodes']:
        wayparts.append([float(nodes[node]['x']), float(nodes[node]['y'])])
    w.line(parts=[wayparts])
    w.record(way['id'], 
    0,
    19,
    1,
    19,
    19,
    255,
    0,
    255,
    19,
    2,
    2,
    15,
    50,
    "T",
    "Blue Barrels",
    "NAUTICAL",
    "OBSTRUCTION",
    "TrObstruction",
    "11001100110011",
    "11001100110011")
    

w = shapefile.Writer(shapefile.POLYLINE)

w.field('id', 'N')
w.field('L_LIMIT', 'N', 50, 0)
w.field('U_LIMIT', 'N')
w.field('COLOR', 'N')
w.field('RTP_COLOR', 'N')
w.field('RTP_LIMIT', 'N')
w.field('BFR_COLOR', 'N') #15
w.field('BFR_WIDTH', 'N') #2
w.field('BDR_COLOR', 'N')
w.field('HAL_COLOR', 'N')
w.field('WIDTH', 'N')
w.field('WIDTH_MULT', 'N') #multiplied with width
w.field('FONT', 'N')
w.field('LAYER', 'N')
w.field('MODE')
w.field('VALUE')
w.field('MAJ_CAT')
w.field('MIN_CAT')
w.field('ICON')
w.field('BFR_PATTERN') #11001100110011 #"dotted" line expressed in 1(line) and 0 (no line) up to 32 chars
w.field('PATTERN') #11001100110011
#w.field('HAL_CLRRGB')

for way in ways:
    if way['stype'] == "obstruction":
        if way['seamark:obstruction:category'] == "boom":
            handleObstructionBoom(way, nodes, w)

w.save('test')