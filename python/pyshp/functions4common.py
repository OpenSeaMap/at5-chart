import collections
from pprint import pprint
import urllib.request
import datetime
from time import sleep
import socket
import os
import xml.etree.ElementTree as xmlTree
import shapefile
import sys
import re

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

x = shapefile.Writer(shapefile.POLYLINE)

x.field('id', 'N')
x.field('L_LIMIT', 'N', 50, 0)
x.field('U_LIMIT', 'N')
x.field('COLOR', 'N')
x.field('RTP_COLOR', 'N')
x.field('RTP_LIMIT', 'N')
x.field('BFR_COLOR', 'N') #15
x.field('BFR_WIDTH', 'N') #2
x.field('BDR_COLOR', 'N')
x.field('HAL_COLOR', 'N')
x.field('WIDTH', 'N')
x.field('WIDTH_MULT', 'N') #multiplied with width
x.field('FONT', 'N')
x.field('LAYER', 'N')
x.field('MODE')
x.field('VALUE')
x.field('MAJ_CAT')
x.field('MIN_CAT')
x.field('ICON')
x.field('BFR_PATTERN') #11001100110011 #"dotted" line expressed in 1(line) and 0 (no line) up to 32 chars
x.field('PATTERN') #11001100110011
#x.field('HAL_CLRRGB')

y = shapefile.Writer(shapefile.POLYGON)

y.field('id', 'N')
y.field('L_LIMIT', 'N', 50, 0)
y.field('U_LIMIT', 'N')
y.field('COLOR', 'N')
y.field('LAYER', 'N')
y.field('MODE')
y.field('VALUE')
y.field('ICON')
y.field('MAJ_CAT')
y.field('MIN_CAT')




all_elements_nice = collections.OrderedDict()

all_elements = collections.OrderedDict()
#Each entry contains a list of dicts. Each dict will contain k/v pairs. The first dict will also specify the type of object it is, or a list of objects it is. If the list of dicts is contained with another list, 2 different ways of tagging an object are checked.
all_elements["beacon_cardinal"] = [{"k": "seamark:type", "v": "beacon_cardinal", "t": "node"}]
all_elements["beacon_lateral"] = [{"k": "seamark:type", "v": "beacon_lateral", "t": "node"}]
all_elements["beacon_isolated_danger"] = [{"k": "seamark:type", "v": "beacon_isolated_danger", "t": "node"}]
all_elements["beacon_safe_water"] = [{"k": "seamark:type", "v": "beacon_safe_water", "t": "node"}]
all_elements["beacon_special_purpose"] = [{"k": "seamark:type", "v": "beacon_special_purpose", "t": "node"}]
#all_elements["beacon_all"] = [{"k": "seamark:type", "regv": "beacon*", "t": "node"}]

all_elements["buoy_cardinal"] = [{"k": "seamark:type", "v": "buoy_cardinal", "t": "node"}]
all_elements["buoy_lateral"] = [{"k": "seamark:type", "v": "buoy_lateral", "t": "node"}]
all_elements["buoy_isolated_danger"] = [{"k": "seamark:type", "v": "buoy_isolated_danger", "t": "node"}]
all_elements["buoy_mooring"] = [{"k": "seamark:type", "v": "mooring", "t": "node"}, {"k": "seamark:mooring:category", "v": "buoy"}]
all_elements["buoy_safe_water"] = [{"k": "seamark:type", "v": "buoy_safe_water", "t": "node"}]
all_elements["buoy_special_purpose"] = [{"k": "seamark:type", "v": "buoy_special_purpose", "t": "node"}]
#all_elements["buoy_all"] = [{"k": "seamark:type", "regv": "buoy*", "t": "node"}]

all_elements["gate"] = [{"k": "seamark:type", "v": "gate", "t": ["node", "area"]}]
all_elements["rock"] = [{"k": "seamark:type", "v": "rock", "t": "node"}] # to add support for an area instead of just node
all_elements["wreck"] = [{"k": "seamark:type", "v": "wreck", "t": "node"}]


all_elements["boom"] = [{"k": "seamark:type", "v": "obstruction", "t": "way"}, {"k": "seamark:obstruction:category", "v": "boom"}]
all_elements["fence"] = [{"k": "barrier", "v": "fence", "t": "way"}]
all_elements["borders"] = [{"k": "boundary", "v": "administrative", "t": "way"}]
all_elements["submarine_cable"] = [{"k": "seamark:type", "v": "cable_submarine", "t": "way"}]


all_elements["lake"] = [[{"k": "natural", "v": "water", "t": "area"}, {"k": "water", "v": "lake"}],[{"k": "natural", "v": "lake", "t": "area"}]] #or if water=lake not specified # <-- maybe add a dict around this to define multiple conditions for match.. then test if dict vs if list.. is this possible?
all_elements["estuary"] = [{"k": "natural", "v": "water", "t": "area"}, {"k": "water", "v": "cove"}, {"k": "estuary", "v": "yes"}]
all_elements["reservoir"] = [{"k": "natural", "v": "water", "t": "area"}, {"k": "water", "v": "reservoir"}]
all_elements["river"] = [{"k": "natural", "v": "water", "t": "area"}, {"k": "water", "v": "river"}]
all_elements["coral"] = [{"k": "subsea", "v": "coral", "t": "area"}]
all_elements["marine_farm"] = [{"k": "seamark:type", "v": "marine_farm", "t": "area"}]

#natural=reef(area/node) rock(area/nodes)
#restricted areas

#specify multiple types with the same keys via t: [type, type]
#TODO TO FIX: currently, multiple types with the same keys may throw an error, to check if multiple types via (if type(all_elements[key][ind][0]['t']) is list: #multiple types) and then use the old method to check if a way is closed or unclosed to determine if way or area. To add this check for nodes as well, just in case
#todo, download coastline

#all_elements["testlake"] = [[{"k": "natural", "v": "water", "t": "area"}, {"k": "water", "v": "lake"}],[{"k": "natural", "v": "lake", "t": "way"}]]

node_array = collections.OrderedDict();

    
def printElementsByKey(fullprint = False):
    firstcolwidth = 35
    if fullprint:
        #pprint(all_elements)
        print("List of elements with the key/value pairs that define them")
        for thename, element in all_elements.items():
            entry = ""
            if type(element[0]) is dict:
                for thekey in element:
                    entry += thekey['k'] + " = " + thekey['v'] + "\n".ljust(firstcolwidth)
                if type(element[0]['t']) is list:
                    origentry = entry
                    entry = "";
                    for thetype in element[0]['t']:
                        entry += (thename + " (" + thetype + ")").ljust(firstcolwidth-4) + " : " + re.sub('\n( *?)$', '', origentry) + "\n\n"
                    entry = re.sub('\n\n$', '\n', entry);
                else:
                    entry = (thename + " (" + element[0]['t'] + ")").ljust(firstcolwidth-4) + " : " + re.sub('\n( *?)$', '', entry) + "\n"
                print(entry)
                
            elif type(element[0]) is list:
                for altelement in element:
                    entry = ""
                    for thekey in altelement:
                        entry += thekey['k'] + " = " + thekey['v'] + "\n".ljust(firstcolwidth)
                    if type(altelement[0]['t']) is list:
                        origentry = entry
                        entry = "";
                        for thetype in altelement[0]['t']:
                            entry += (thename + " (" + thetype + ")").ljust(firstcolwidth-4) + " : " + re.sub('\n( *?)$', '', origentry) + "\n\n"
                        entry = re.sub('\n\n$', '\n', entry);
                    else:
                        entry = (thename + " (" + altelement[0]['t'] + ")").ljust(firstcolwidth-4) + " : " + re.sub('\n( *?)$', '', entry) + "\n"
                    print(entry)
            #elif element[0] is list:
                
    else:
        for key in all_elements.keys():
            #pprint (all_elements[key]);
            if type(all_elements[key][0]) is list:
                if type(all_elements[key][0][0]['t']) is list:
                    temptypestr = ', '.join(all_elements[key][0][0]['t'])
                else:
                    temptypestr = all_elements[key][0][0]['t']
                print(key + " (" + temptypestr + ")")
            else:
                if type(all_elements[key][0]['t']) is list:
                    temptypestr = ', '.join(all_elements[key][0]['t'])
                else:
                    temptypestr = all_elements[key][0]['t']
                print(key + " (" + temptypestr + ")")
    exit()
    
def downloadOSM(oapi, outdir, bounds, verboosity = False, combine = False, mix = True, eles = []): #mix stores a mixture (randomly) of types (nodes, ways, areas) in the same file; this function currently ignores the value and assumes True AND will only matter (once we fix this function to stop ignoring it) if combine==True; to fix this we will probably need to revert to queryargs old code (sublist for nodes, etc, then each subsublist is named like ['buoy_all'] etc
    if verboosity:
        print("Pre-processing elements. Preparing to download...")
    
    elements = []
    if not eles:
        for elekey in all_elements.keys():
            elements.append(elekey)
    else:
        for elekey in eles:
            if elekey in all_elements.keys():
                elements.append(elekey)
            else:
                print("Warning: Unknown element '" + elekey + "'!")
    
    queries = {'node': {}, 'way': {}, 'area': {}}
    for key in elements:
        if type(all_elements[key][0]) is dict: #no alternate tags (may still have multiple keys/values)
            query = ""
            for obj in all_elements[key]:
                if "regv" in obj.keys():
                    query += '["' + obj['k'] + '"~"' + obj['regv'] + '"]'
                else:
                    query += '["' + obj['k'] + '"="' + obj['v'] + '"]'
                    
            if type(all_elements[key][0]['t']) is list: #multiple types
                for thetype in all_elements[key][0]['t']:
                    queries[thetype][key] = queries[thetype].get(key, '') + ((thetype if (thetype != "area") else "way") + query + '(' + str(bounds[1]) + ',' + str(bounds[2]) + ',' + str(bounds[0]) + ',' + str(bounds[3]) + ');')
            else:
                queries[all_elements[key][0]['t']][key] = queries[all_elements[key][0]['t']].get(key, '') + ((all_elements[key][0]['t'] if (all_elements[key][0]['t'] != "area") else "way") + query + '(' + str(bounds[1]) + ',' + str(bounds[2]) + ',' + str(bounds[0]) + ',' + str(bounds[3]) + ');')
        elif type(all_elements[key][0]) is list: #has alternate tags (see "lake" for example)
            for ind in range(0, len(all_elements[key])):
                query = ""
                for obj in all_elements[key][ind]:
                    if "regv" in obj.keys():
                        query += '["' + obj['k'] + '"~"' + obj['regv'] + '"]'
                    else:
                        query += '["' + obj['k'] + '"="' + obj['v'] + '"]'
                        
                if type(all_elements[key][ind][0]['t']) is list: #multiple types
                    for thetype in all_elements[key][ind][0]['t']:
                        queries[thetype][key] = queries[thetype].get(key, '') + ((thetype if (thetype != "area") else "way") + query + '(' + str(bounds[1]) + ',' + str(bounds[2]) + ',' + str(bounds[0]) + ',' + str(bounds[3]) + ');')
                else:
                    queries[all_elements[key][ind][0]['t']][key] = queries[all_elements[key][ind][0]['t']].get(key, '') + ((all_elements[key][ind][0]['t'] if (all_elements[key][ind][0]['t'] != "area") else "way") + query + '(' + str(bounds[1]) + ',' + str(bounds[2]) + ',' + str(bounds[0]) + ',' + str(bounds[3]) + ');')

    if verboosity:
        print("Downloading elements:")
    
    osmfiles = []
    osmurl = {}
    
    if combine:
        if mix:
            cmbmixstr = []
            for thetype, thelist in queries.items():
                for thename, theobject in thelist.items():
                    cmbmixstr.append(theobject)
            osmurl["combined_mixed"] = (oapi + '?data=[maxsize:1073741824][timeout:900][out:xml];(' + ''.join(cmbmixstr) + ');(._;>;);out;')
            #print(osmurl)
            #overpass.osm.rambler.ru/cgi/interpreter?data=[maxsize:1073741824][timeout:900][out:xml];(node["seamark:type"~"beacon*"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499);node["seamark:type"~"buoy*"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499);node["seamark:type"="wreck"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499);node["seamark:type"="rock"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499);way["seamark:type"="obstruction"]["seamark:obstruction:category"="boom"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499);way["barrier"="fence"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499);way["boundary"="administrative"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499);way["natural"="water"]["water"="lake"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499);way["natural"="lake"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499);way["natural"="water"]["water"="cove"]["estuary"="yes"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499);way["natural"="water"]["water"="reservoir"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499);way["natural"="water"]["water"="river"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499);way["subsea"="coral"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499);node["seamark:type"="gate"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499);way["seamark:type"="gate"](1.0553144713908544,104.315185546875,1.5962442743900633,103.41430664062499););(._;>;);out;
        else:
            for thetype, thelist in queries.items():
                cmbstr = []
                for thename, theobject in thelist.items():
                    cmbstr.append(theobject)
                osmurl["combined_" + thetype] = (oapi + '?data=[maxsize:1073741824][timeout:900][out:xml];(' + ''.join(cmbstr) + ');(._;>;);out;')
    else:
        for thetype, thelist in queries.items():
            for thename, theobject in thelist.items():
                osmurl[thetype + "_" + thename] = (oapi + '?data=[maxsize:1073741824][timeout:900][out:xml];(' + theobject + ');(._;>;);out;')
    
    datetimestamp = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
    for ind, (thename, theurl) in enumerate(osmurl.items()):
        osmfile = outdir + "/" + "osm2inc_" + str(bounds[1]) + "N_" + str(bounds[3]) + "S_" + str(bounds[0]) + "E_" + str(bounds[2]) + "W-" + datetimestamp + "_" + thename + ".osm"
        
        attempts = 1
        while attempts <= 3:
            try:
                print("- Downloading .osm file " + str(ind+1) + " of " + str(len(osmurl)) + ": " + osmfile)
                urllib.request.urlretrieve(theurl, osmfile)
            except (urllib.error.HTTPError, urllib.error.URLError, socket.timeout) as e:
                attempts += 1
                print ("-- Error while retrieving data! Sleeping for 5 seconds...")
                sleep(5)
                print ("--- Retrying download... (attempt " + str(attempts) + " of 3)")
                pass
            else:
                break
        if attempts >= 3:
            print("Error: Problem downloading file. Maybe try it in your browser:\n" + osmurl[ind])
        else:
            osmfiles.append(osmfile)
    
    return osmfiles
    
def getOSMFilesInDir(dir = "./"):
    filelist = []
    for file in os.listdir(dir):
        if file.endswith(".osm"):
            filelist.append(file)
    return filelist
    
def processOSMFile(file, verboose):
    xml = xmlTree.parse(file)
    root = xml.getroot()
    
    for entry in root:
        if (entry.tag == "node"):
            node_array[entry.attrib['id']] = {"x": entry.attrib['lat'], "y": entry.attrib['lon']}
            if (entry.find("tag") != None):
                thenode = collections.OrderedDict()
                for tag in entry.findall("tag"):
                    thenode[tag.attrib['k']] = tag.attrib['v']
                    
                cmpnode = dict(thenode)
                thenode['id'] = entry.attrib['id']
                thenode['x'] = entry.attrib['lat']
                thenode['y'] = entry.attrib['lon']
                    
                for thekey, ele in all_elements_nice.items():
                    if type(ele) is dict or type(ele) is collections.OrderedDict:
                        cmpdict = dict(ele)
                        del cmpdict['t']
                        shared_items = set(cmpdict.items()) & set(cmpnode.items())
                        if len(shared_items) == len(cmpdict):
                            getattr(sys.modules[__name__], 'handle_node_' + thekey)(thenode);
                            break;
                    elif type(ele) is list:
                        for altele in ele:
                            cmpdict = dict(altele)
                            del cmpdict['t']
                            shared_items = set(cmpdict.items()) & set(cmpnode.items())
                            if len(shared_items) == len(cmpdict):
                                getattr(sys.modules[__name__], 'handle_node_' + thekey)(thenode);
                                break; #it doesn't break out of the second loop though. We don't care because I'm tired of this shit.
        elif (entry.tag == "way"):
            # We don't rely on the following anymore. because areas may be unclosed (like chek jawa restricted area, or very long closed was that are split up, like coastlines), and ways may be closed (like fences). We now rely on key/value mapping (like for the node identification above)
            #if entry.find(".//nd[last()]").attrib['ref'] == entry.find(".//nd[1]").attrib['ref']:
            #    print ("We Found an Area" + entry.attrib['id'])
            #else:
            #    print("We Found a way" + entry.attrib['id'])
            if (entry.find("tag") != None):
                theway = collections.OrderedDict()
                for tag in entry.findall("tag"):
                    theway[tag.attrib['k']] = tag.attrib['v']
                
                cmpway = dict(theway)
                theway['id'] = entry.attrib['id']
                thepoints = []
                for thepoint in entry.findall("nd"):
                    thepoints.append(thepoint.attrib['ref'])
                theway['points'] = thepoints;
                
                for thekey, ele in all_elements_nice.items():
                    if type(ele) is dict or type(ele) is collections.OrderedDict:
                        cmpdict = dict(ele)
                        del cmpdict['t']
                        shared_items = set(cmpdict.items()) & set(cmpway.items())
                        if len(shared_items) == len(cmpdict):
                            if ele['t'] == 'way':
                                getattr(sys.modules[__name__], 'handle_way_' + thekey)(theway);
                                break;
                            elif ele['t'] == 'area':
                                getattr(sys.modules[__name__], 'handle_area_' + thekey)(theway);
                                break;
                    elif type(ele) is list:
                        for altele in ele:
                            cmpdict = dict(altele)
                            del cmpdict['t']
                            shared_items = set(cmpdict.items()) & set(cmpway.items())
                            if len(shared_items) == len(cmpdict):
                                if altele['t'] == 'way':
                                    getattr(sys.modules[__name__], 'handle_way_' + thekey)(theway);
                                    break;
                                elif altele['t'] == 'area':
                                    getattr(sys.modules[__name__], 'handle_area_' + thekey)(theway);
                                    break;
            
    
def buildAllElementsNice():
    for thekey, ele in all_elements.items():
        thefinalele = collections.OrderedDict()
        if type(ele[0]) is dict:
            for kvpair in ele:
                thefinalele.update({kvpair['k']: kvpair['v']});
            thefinalele.update({'t': ele[0]['t']})
            all_elements_nice.update({thekey: thefinalele});
        elif type(ele[0]) is list:
            thesemifinalele = []
            for alternate in ele:
                thequarterfinalele = collections.OrderedDict()
                for kvpair in alternate:
                    thequarterfinalele.update({kvpair['k']: kvpair['v']});
                thequarterfinalele.update({'t': alternate[0]['t']})
                thesemifinalele.append(thequarterfinalele);
            all_elements_nice.update({thekey: thesemifinalele});
    
def processOSMFiles(thefiles, verboose):
    if verboose:
        print ("- Processing files...")
    buildAllElementsNice();
    #pprint(all_elements_nice);
    for i, file in enumerate(thefiles):
        if verboose:
            print ("-- Processing " + file + " (file " + str(i+1) + " of " + str(len(thefiles)) + ")")
        processOSMFile(file, verboose);
        
    datetimestamp = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
    if len(w._shapes) > 0:
        if (verboose):
            pprint("- Saving 'nodes' shapefile...");
        w.save("osm2inc_" + datetimestamp + "_combined_nodes.osm")
    else:
        if (verboose):
            pprint("Warning! No nodes detected! Not generating 'node' shapefile");
    if len(x._shapes) > 0:
        if (verboose):
            pprint("- Saving 'ways' shapefile...");
        x.save("osm2inc_" + datetimestamp + "_combined_ways.osm")
    else:
        if (verboose):
            pprint("Warning! No ways detected! Not generating 'ways' shapefile");
    if len(y._shapes) > 0:
        if (verboose):
            pprint("- Saving 'areas' shapefile...");
        y.save("osm2inc_" + datetimestamp + "_combined_areas.osm")
    else:
        if (verboose):
            pprint("Warning! No areas(closed ways) detected! Not generating 'areas' shapefile");
    #pprint(node_array);
    #pprint(thefiles)
    if (verboose):
        pprint("Done.")


def handle_node_beacon_cardinal(theobject):
    infobox = "Name: ".join(theobject.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(theobject.get('seamark:type', ''))
    infobox.join("\r\nCategory ").join(theobject.get('seamark:beacon_cardinal:category', ''))
    infobox.join("\r\nColour ").join(theobject.get('seamark:beacon_cardinal:colour', ''))
    infobox.join("\r\nColour Pattern ").join(theobject.get('seamark:beacon_cardinal:colour_pattern', ''))
    infobox.join("\r\nTopmark Shape ").join(theobject.get('seamark:topmark:shape', ''))
    infobox.join("\r\nTopmark Colour ").join(theobject.get('seamark:topmark:colour', ''))
    infobox.join("\r\nLight Character ").join(theobject.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(theobject.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(theobject.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(theobject.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(theobject.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(theobject.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Cardinal'
    
    if theobject.get('seamark:beacon_cardinal:category', '') == "north":
        icon = "TrNorthCardinalBuoy"
    elif theobject.get('seamark:beacon_cardinal:category', '') == "south":
        icon = "TrSouthCardinalBuoy"
    elif theobject.get('seamark:beacon_cardinal:category', '') == "east":
        icon = "TrEastCardinalBuoy"
    elif theobject.get('seamark:beacon_cardinal:category', '') == "west":
        icon = "TrWestCardinalBuoy"
    
    if theobject.get('seamark:light:colour', '') != '':
        icon += "L"
    else:
        icon = icon
    
    icon += "Big"
    
    w.point(float(theobject['x']), float(theobject['y']))
    w.record(
        theobject['x'],
        theobject['y'],
        theobject['id'],
        0,
        19,
        19,
        19,
        15,
        1,
        15,
        50,
        'T',
        infobox,
        theobject.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    
def handle_node_beacon_isolated_danger(theobject):
    infobox = "Name: ".join(theobject.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(theobject.get('seamark:type', ''))
    infobox.join("\r\nColour: ").join(theobject.get('seamark:beacon_isolated_danger:colour', ''))
    infobox.join("\r\nColour Pattern: ").join(theobject.get('seamark:beacon_isolated_danger:colour_pattern', ''))
    infobox.join("\r\nTopmark Shape: ").join(theobject.get('seamark:topmark:shape', ''))
    infobox.join("\r\nTopmark Colour: ").join(theobject.get('seamark:topmark:colour', ''))
    infobox.join("\r\nLight Character ").join(theobject.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(theobject.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(theobject.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(theobject.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(theobject.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(theobject.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Danger'
    
    icon = "TrIsoDangerBuoy"
    if theobject.get('seamark:light:colour', '') != '':
        icon += "L"
    icon += "Big"
    
    w.point(float(theobject['x']), float(theobject['y']))
    w.record(
        theobject['x'],
        theobject['y'],
        theobject['id'],
        0,
        19,
        19,
        19,
        15,
        1,
        15,
        50,
        'T',
        infobox,
        theobject.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    
def handle_node_beacon_lateral(theobject):
    infobox = "Name: ".join(theobject.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(theobject.get('seamark:type', ''))
    infobox.join("\r\nCategory ").join(theobject.get('seamark:beacon_lateral:category', ''))
    infobox.join("\r\nColour ").join(theobject.get('seamark:beacon_lateral:colour', ''))
    infobox.join("\r\nShape ").join(theobject.get('seamark:beacon_lateral:shape', ''))
    infobox.join("\r\nTopmark Shape ").join(theobject.get('seamark:topmark:shape', ''))
    infobox.join("\r\nSystem ").join(theobject.get('seamark:beacon_lateral:system', ''))
    infobox.join("\r\nLight Character ").join(theobject.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(theobject.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(theobject.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(theobject.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(theobject.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(theobject.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Lateral'
    if theobject.get('seamark:beacon_lateral:category', '') == "port":
        if theobject.get('seamark:beacon_lateral:system', '') == "iala-b":
            icon = "TrPortHandBeaconRegB"
        else:
            icon = "TrPortHandBeaconRegA"
    elif theobject.get('seamark:beacon_lateral:category', '') == "starboard":
        if theobject.get('seamark:beacon_lateral:system', '') == "iala-b":
            icon = "TrStarboardHandBeaconRegB"
        else:
            icon = "TrStarboardHandBeaconRegA"
    else:
        #prefered channel buoys and inland buoys - as there are no default icons in IMC yet #tofix this.. for beacons
        icon = "TrBeaconGeneric";
    
    if theobject.get('seamark:light:colour', '') != '':
        icon += "LBig"
    else:
        icon += "Big"
    
    w.point(float(theobject['x']), float(theobject['y']))
    w.record(
        theobject['x'],
        theobject['y'],
        theobject['id'],
        0,
        19,
        19,
        19,
        15,
        1,
        15,
        50,
        'T',
        infobox,
        theobject.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    
def handle_node_beacon_safe_water(theobject):
    infobox = "Name: ".join(theobject.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(theobject.get('seamark:type', ''))
    infobox.join("\r\nColour: ").join(theobject.get('seamark:beacon_safe_water:colour', ''))
    infobox.join("\r\nColour Pattern: ").join(theobject.get('seamark:beacon_safe_water:colour_pattern', ''))
    infobox.join("\r\nTopmark Shape: ").join(theobject.get('seamark:topmark:shape', ''))
    infobox.join("\r\nTopmark Colour: ").join(theobject.get('seamark:topmark:colour', ''))
    infobox.join("\r\nLight Character ").join(theobject.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(theobject.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(theobject.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(theobject.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(theobject.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(theobject.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Safe Water'
    
    icon = "TrSafeWatersBuoy"
    if theobject.get('seamark:light:colour', '') != '':
        icon += "L"
    
    w.point(float(theobject['x']), float(theobject['y']))
    w.record(
        theobject['x'],
        theobject['y'],
        theobject['id'],
        0,
        19,
        19,
        19,
        15,
        1,
        15,
        50,
        'T',
        infobox,
        theobject.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    
def handle_node_beacon_special_purpose(theobject):
    infobox = "Name: ".join(theobject.get('seamark:name', '')).join("\r\nCategory: ").join(theobject.get('seamark:beacon_special_purpose:category', '')).join("\r\nNo further description available at this time.")
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Special Purpose'
    
    icon = "TrSpecialPurposeBuoyYellow"
    if theobject.get('seamark:light:colour', '') != '':
        icon += "L"
    
    w.point(float(theobject['x']), float(theobject['y']))
    w.record(
        theobject['x'],
        theobject['y'],
        theobject['id'],
        0,
        19,
        19,
        19,
        15,
        1,
        15,
        50,
        'T',
        infobox,
        theobject.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    

def handle_node_buoy_cardinal(theobject):
    infobox = "Name: ".join(theobject.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(theobject.get('seamark:type', ''))
    infobox.join("\r\nCategory ").join(theobject.get('seamark:buoy_cardinal:category', ''))
    infobox.join("\r\nColour ").join(theobject.get('seamark:buoy_cardinal:colour', ''))
    infobox.join("\r\nColour Pattern ").join(theobject.get('seamark:buoy_cardinal:colour_pattern', ''))
    infobox.join("\r\nTopmark Shape ").join(theobject.get('seamark:topmark:shape', ''))
    infobox.join("\r\nTopmark Colour ").join(theobject.get('seamark:topmark:colour', ''))
    infobox.join("\r\nLight Character ").join(theobject.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(theobject.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(theobject.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(theobject.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(theobject.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(theobject.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Cardinal'
    
    if theobject.get('seamark:buoy_cardinal:category', '') == "north":
        icon = "TrNorthCardinalBuoy"
    elif theobject.get('seamark:buoy_cardinal:category', '') == "south":
        icon = "TrSouthCardinalBuoy"
    elif theobject.get('seamark:buoy_cardinal:category', '') == "east":
        icon = "TrEastCardinalBuoy"
    elif theobject.get('seamark:buoy_cardinal:category', '') == "west":
        icon = "TrWestCardinalBuoy"
    
    if theobject.get('seamark:light:colour', '') != '':
        icon += "L"
    else:
        icon = icon
    
    icon += "Big"
    
    w.point(float(theobject['x']), float(theobject['y']))
    w.record(
        theobject['x'],
        theobject['y'],
        theobject['id'],
        0,
        19,
        19,
        19,
        15,
        1,
        15,
        50,
        'T',
        infobox,
        theobject.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    
def handle_node_buoy_isolated_danger(theobject):
    infobox = "Name: ".join(theobject.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(theobject.get('seamark:type', ''))
    infobox.join("\r\nColour: ").join(theobject.get('seamark:buoy_isolated_danger:colour', ''))
    infobox.join("\r\nColour Pattern: ").join(theobject.get('seamark:buoy_isolated_danger:colour_pattern', ''))
    infobox.join("\r\nTopmark Shape: ").join(theobject.get('seamark:topmark:shape', ''))
    infobox.join("\r\nTopmark Colour: ").join(theobject.get('seamark:topmark:colour', ''))
    infobox.join("\r\nLight Character ").join(theobject.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(theobject.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(theobject.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(theobject.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(theobject.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(theobject.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Danger'
    
    icon = "TrIsoDangerBuoy"
    if theobject.get('seamark:light:colour', '') != '':
        icon += "L"
    icon += "Big"
    
    w.point(float(theobject['x']), float(theobject['y']))
    w.record(
        theobject['x'],
        theobject['y'],
        theobject['id'],
        0,
        19,
        19,
        19,
        15,
        1,
        15,
        50,
        'T',
        infobox,
        theobject.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    
def handle_node_buoy_lateral(theobject):
    infobox = "Name: ".join(theobject.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(theobject.get('seamark:type', ''))
    infobox.join("\r\nCategory ").join(theobject.get('seamark:buoy_lateral:category', ''))
    infobox.join("\r\nColour ").join(theobject.get('seamark:buoy_lateral:colour', ''))
    infobox.join("\r\nShape ").join(theobject.get('seamark:buoy_lateral:shape', ''))
    infobox.join("\r\nTopmark Shape ").join(theobject.get('seamark:topmark:shape', ''))
    infobox.join("\r\nSystem ").join(theobject.get('seamark:buoy_lateral:system', ''))
    infobox.join("\r\nLight Character ").join(theobject.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(theobject.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(theobject.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(theobject.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(theobject.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(theobject.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Lateral'
    
    if theobject.get('seamark:buoy_lateral:category', '') == "port":
        if theobject.get('seamark:buoy_lateral:shape', '') == "pillar" or \
        theobject.get('seamark:buoy_lateral:shape', '') == "spar" or \
        theobject.get('seamark:buoy_lateral:shape', '') == "ice_buoy" or \
        theobject.get('seamark:buoy_lateral:shape', '') == "super-buoy":
            if theobject.get('seamark:buoy_lateral:system', '') == "iala-b":
                icon = "TrPortHandBuoyRegB"
            else:
                icon = "TrPortHandBuoyRegA"
        else:
            #includes conical, can, spherical, barrel
            if theobject.get('seamark:buoy_lateral:system', '') == "iala-b":
                icon = "TrBuoyFinalGreen"
            else:
                icon = "TrBuoyFinalRed"
    elif theobject.get('seamark:buoy_lateral:category', '') == "starboard":
        if theobject.get('seamark:buoy_lateral:shape', '') == "pillar" or \
        theobject.get('seamark:buoy_lateral:shape', '') == "spar" or \
        theobject.get('seamark:buoy_lateral:shape', '') == "ice_buoy" or \
        theobject.get('seamark:buoy_lateral:shape', '') == "super-buoy":
            if theobject.get('seamark:buoy_lateral:system', '') == "iala-b":
                icon = "TrStarboardHandBuoyRegB"
            else:
                icon = "TrStarboardHandBuoyRegA"
        else:
            #includes conical, can, spherical, barrel
            if theobject.get('seamark:buoy_lateral:system', '') == "iala-b":
                icon = "TrBuoyFinalRed"
            else:
                icon = "TrBuoyFinalGreen"
    else:
        #prefered channel buoys and inland buoys - as there are no default icons in IMC yet
        icon = "TrBuoyFinalWhite";
    
    if theobject.get('seamark:light:colour', '') != '':
        icon += "L"
    else:
        icon = icon
    
    w.point(float(theobject['x']), float(theobject['y']))
    w.record(
        theobject['x'],
        theobject['y'],
        theobject['id'],
        0,
        19,
        19,
        19,
        15,
        1,
        15,
        50,
        'T',
        infobox,
        theobject.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    
    
def handle_node_buoy_mooring(theobject):
    handle_node_buoy_special_purpose(theobject);
    
def handle_node_buoy_safe_water(theobject):
    infobox = "Name: ".join(theobject.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(theobject.get('seamark:type', ''))
    infobox.join("\r\nColour: ").join(theobject.get('seamark:buoy_safe_water:colour', ''))
    infobox.join("\r\nColour Pattern: ").join(theobject.get('seamark:buoy_safe_water:colour_pattern', ''))
    infobox.join("\r\nTopmark Shape: ").join(theobject.get('seamark:topmark:shape', ''))
    infobox.join("\r\nTopmark Colour: ").join(theobject.get('seamark:topmark:colour', ''))
    infobox.join("\r\nLight Character ").join(theobject.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(theobject.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(theobject.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(theobject.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(theobject.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(theobject.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Safe Water'
    
    icon = "TrSafeWatersBuoy"
    if theobject.get('seamark:light:colour', '') != '':
        icon += "L"
    
    w.point(float(theobject['x']), float(theobject['y']))
    w.record(
        theobject['x'],
        theobject['y'],
        theobject['id'],
        0,
        19,
        19,
        19,
        15,
        1,
        15,
        50,
        'T',
        infobox,
        theobject.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    
def handle_node_buoy_special_purpose(theobject):
    infobox = "Name: ".join(theobject.get('seamark:name', '')).join("\r\nCategory: ").join(theobject.get('seamark:buoy_special_purpose:category', '')).join("\r\nNo further description available at this time.")
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Special Purpose'
    
    icon = "TrSpecialPurposeBuoyYellow"
    if theobject.get('seamark:light:colour', '') != '':
        icon += "L"
    
    w.point(float(theobject['x']), float(theobject['y']))
    w.record(
        theobject['x'],
        theobject['y'],
        theobject['id'],
        0,
        19,
        19,
        19,
        15,
        1,
        15,
        50,
        'T',
        infobox,
        theobject.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    

def handle_node_gate(theobject):
    infobox = "Name: ".join(theobject.get('seamark:name', '')).join("\r\nNo further description available at this time.")
    majcat = 'NAUTICAL'
    if theobject['seamark:gate:category'].lower() == "dyke" \
        or theobject['seamark:gate:category'].lower() == "lock" \
        or theobject['seamark:gate:category'].lower() == "caisson" \
        or theobject['seamark:gate:category'].lower() == "flood_barrage":
        mincat = 'Dyke'
        icon = 'PGATE'
    else:
        #theobject['seamark:gate:category'].lower() == "sluice" or theobject['seamark:gate:category'].lower() == "general"
        mincat = 'Gate'
        icon = 'PGATE'
    
    w.point(float(theobject['x']), float(theobject['y']))
    w.record(
        theobject['x'],
        theobject['y'],
        theobject['id'],
        0,
        19,
        19,
        19,
        15,
        1,
        15,
        50,
        'T',
        infobox,
        theobject.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    
def handle_node_rock(theobject):
    None;
    
def handle_node_wreck(theobject):
    infobox = "Name: ".join(theobject.get('seamark:name', '')).join("\r\nNo further description available at this time.")
    majcat = 'NAUTICAL'
    mincat = 'WRECK'
    if theobject['seamark:wreck:category'].lower() == "non-dangerous" or theobject['seamark:wreck:category'].lower() == "distributed_remains":
        icon = 'PWRECKS_1_BIG'
    elif theobject['seamark:wreck:category'].lower() == "dangerous" or theobject['seamark:wreck:category'].lower() == "mast_showing":
        icon = 'PWRECKS_4_BIG'
    elif theobject['seamark:wreck:category'].lower() == "hull_showing":
        icon = 'PWRECKS_5_BIG'
    else:
        icon = 'PWRECKS_4_BIG'
    
    w.point(float(theobject['x']), float(theobject['y']))
    w.record(
        theobject['x'],
        theobject['y'],
        theobject['id'],
        0,
        19,
        19,
        19,
        15,
        1,
        15,
        50,
        'T',
        infobox,
        theobject.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    

def handle_way_boom(theobject):
    wayparts = []
    for node in theobject['points']:
        wayparts.append([float(node_array[node]['x']), float(node_array[node]['y'])])
    x.line(parts=[wayparts])
    x.record(theobject['id'], 
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
    
def handle_way_fence(theobject):
    None;
    
def handle_way_borders(theobject):
    None;
    
def handle_way_submarine_cable(theobject):
    None;
    

def handle_area_lake(theobject):
    None;
    
def handle_area_estuary(theobject):
    None;
    
def handle_area_reservoir(theobject):
    None;
    
def handle_area_river(theobject):
    None;
    
def handle_area_coral(theobject):
    None;
    
def handle_area_marine_farm(theobject):
    wayparts = []
    for node in theobject['points']:
        wayparts.append([float(node_array[node]['x']), float(node_array[node]['y'])])
        
    if theobject['points'][0] != theobject['points'][last()]: #close unclosed ways
        wayparts.append([float(node_array[theobject['points'][0]]['x']), float(node_array[theobject['points'][0]]['y'])])
        
    y.poly(parts=[wayparts])
    y.record(theobject['id'], 
    0,
    34,
    30,
    50,
    "T",
    theobject.get('name', ''),
    'FHS_FISHERYAP_FY',
    "NAUTICAL",
    "Marine Farm")
    
    
    
    
    
    
    
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