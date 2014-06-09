import shapefile
import xml.etree.ElementTree as ET
import urllib.request

#freshwater: 11
#brackish 16
#salt 3
#Currently assumes that the ways are closed.

bounds_lat_north = "1.5962442743900633"
bounds_lat_south = "1.0553144713908544"
bounds_lon_west = "103.41430664062499"
bounds_lon_east = "104.315185546875"
mark_type = 'marine_farm'
additional_keys = ''

#osmurl = 'http://overpass.osm.rambler.ru/cgi/interpreter?data=[out:xml];(way["natural"="water"](' + bounds_lat_south + ',' + bounds_lon_west + ',' + bounds_lat_north + ',' + bounds_lon_east + ');way["seamark:type"="marine_farm"](' + bounds_lat_south + ',' + bounds_lon_west + ',' + bounds_lat_north + ',' + bounds_lon_east + '););(._;>;);out;'
osmurl = 'http://overpass.osm.rambler.ru/cgi/interpreter?data=[out:xml];way["seamark:type"="marine_farm"](' + bounds_lat_south + ',' + bounds_lon_west + ',' + bounds_lat_north + ',' + bounds_lon_east + ');(._;>;);out;'
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
                if subchild.attrib.get('k', '').lower() == "natural":
                    if subchild.attrib.get('v', '').lower() == "water":
                        way['stype'] = "water"
                    else:
                        way[subchild.attrib.get('k', '').lower()] = subchild.attrib['v'].lower()
                elif subchild.attrib.get('k', '').lower() == "salt":
                    if subchild.attrib.get('v', '').lower() == "yes" or subchild.attrib.get('v', '').lower() == "*":
                        way['wtype'] = "salt"
                    else:
                        way['wtype'] = "fresh"
                elif subchild.attrib.get('k', '').lower() == "seamark:type":
                    way['stype'] = subchild.attrib.get('v', '').lower()
                else:
                    way[subchild.attrib.get('k', '').lower()] = subchild.attrib['v'].lower()
            elif subchild.tag == "nd":
                cnodes.append(subchild.attrib['ref'])
            
        way['cnodes'] = cnodes
        if way.get('wtype', '') == '':
            way['wtype'] = "fresh"
        
        ways.append(way)
        

def handleFW(way, nodes, w):
    wayparts = []
    for node in way['cnodes']:
        wayparts.append([float(nodes[node]['x']), float(nodes[node]['y'])])
    w.poly(parts=[wayparts])
    w.record(way['id'], 
    0,
    34,
    16,
    98,
    "T",
    way.get('name', 'Freshwater'),
    '',
    "NAUTICAL",
    "Lake")
    
def handleSW(way, nodes, w):
    wayparts = []
    for node in way['cnodes']:
        wayparts.append([float(nodes[node]['x']), float(nodes[node]['y'])])
    w.poly(parts=[wayparts])
    w.record(way['id'], 
    0,
    34,
    11,
    98,
    "T",
    way.get('name', 'Salt/Brackish'),
    '',
    "NAUTICAL",
    "River")
    
    
def handleMarineFarm(way, nodes, w):
    wayparts = []
    for node in way['cnodes']:
        wayparts.append([float(nodes[node]['x']), float(nodes[node]['y'])])
    w.poly(parts=[wayparts])
    w.record(way['id'], 
    0,
    34,
    30,
    50,
    "T",
    way.get('name', 'Salt/Brackish'),
    'FHS_FISHERYAP_FY',
    "NAUTICAL",
    "Marine Farm")
    

w = shapefile.Writer(shapefile.POLYGON)

w.field('id', 'N')
w.field('L_LIMIT', 'N', 50, 0)
w.field('U_LIMIT', 'N')
w.field('COLOR', 'N')
w.field('LAYER', 'N')
w.field('MODE')
w.field('VALUE')
w.field('ICON')
w.field('MAJ_CAT')
w.field('MIN_CAT')

for way in ways:
    if way['stype'] == "water":
        if way.get('wtype', '') == "fresh":
            handleFW(way, nodes, w)
        elif way.get('wtype', '') == "salt":
            handleSW(way, nodes, w)
    if way['stype'] == "marine_farm":
        handleMarineFarm(way, nodes, w)

w.save(mark_type + '_singapore')