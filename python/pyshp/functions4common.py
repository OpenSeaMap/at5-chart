import collections
from pprint import pprint
import urllib.request
import datetime
from time import sleep
import socket
import os
import xml.etree.ElementTree as xmlTree

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
all_elements["buoy_safe_water"] = [{"k": "seamark:type", "v": "buoy_safe_water", "t": "node"}]
all_elements["buoy_special_purpose"] = [{"k": "seamark:type", "v": "buoy_special_purpose", "t": "node"}]
#all_elements["buoy_all"] = [{"k": "seamark:type", "regv": "buoy*", "t": "node"}]
all_elements["buoy_mooring"] = [{"k": "seamark:type", "v": "mooring", "t": "node"}, {"k": "seamark:mooring:category", "v": "buoy"}]

all_elements["wreck"] = [{"k": "seamark:type", "v": "wreck", "t": "node"}]
all_elements["rock"] = [{"k": "seamark:type", "v": "rock", "t": "node"}]


all_elements["boom"] = [{"k": "seamark:type", "v": "obstruction", "t": "way"}, {"k": "seamark:obstruction:category", "v": "boom"}]
all_elements["fence"] = [{"k": "barrier", "v": "fence", "t": "way"}]
all_elements["borders"] = [{"k": "boundary", "v": "administrative", "t": "way"}]
all_elements["submarine_cable"] = [{"k": "seamark:type", "v": "cable_submarine", "t": "way"}]


all_elements["lake"] = [[{"k": "natural", "v": "water", "t": "area"}, {"k": "water", "v": "lake"}],[{"k": "natural", "v": "lake", "t": "area"}]] #or if water=lake not specified # <-- maybe add a dict around this to define multiple conditions for match.. then test if dict vs if list.. is this possible?
all_elements["estuary"] = [{"k": "natural", "v": "water", "t": "area"}, {"k": "water", "v": "cove"}, {"k": "estuary", "v": "yes"}]
all_elements["reservoir"] = [{"k": "natural", "v": "water", "t": "area"}, {"k": "water", "v": "reservoir"}]
all_elements["river"] = [{"k": "natural", "v": "water", "t": "area"}, {"k": "water", "v": "river"}]
all_elements["coral"] = [{"k": "subsea", "v": "coral", "t": "area"}]


all_elements["gate"] = [{"k": "seamark:type", "v": "gate", "t": ["node", "area"]}]
#natural=reef(area/node) rock(area/nodes)
#marine_farm (area)
#restricted areas



node_array = collections.OrderedDict();

def printElementsByKey(fullprint = False):
    if fullprint:
        pprint(all_elements)
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
            node_array[entry.attrib['id']] = {"lat": entry.attrib['lat'], "lon": entry.attrib['lon']}
            if (entry.find("tag") != None):
                thenode = collections.OrderedDict()
                for tag in entry.findall("tag"):
                    thenode[tag.attrib['k']] = tag.attrib['v']
                    
                for thekey, ele in all_elements_nice.items():
                    if type(ele) is dict or type(ele) is collections.OrderedDict:
                        shared_items = set(ele.items()) & set(thenode.items())
                        if len(shared_items) == len(ele):
                            print("WE FOUND ONE! " + thekey);
                            None;
                    elif type(ele) is list:
                        for altele in ele:
                            shared_items = set(altele.items()) & set(thenode.items())
                            if len(shared_items) == len(altele):
                                print("TODO: Check that this works.")
                                print("WE FOUND ONE MULTI! " + thekey);
                    
                #pprint (thenode);
                
                
            
        elif (entry.tag == "way"):
            None;
            #if (verboose):
            #    print("way or area");
    #node_array
    
def buildAllElementsNice():
    for thekey, ele in all_elements.items():
        thefinalele = collections.OrderedDict()
        #print(ele);
        if type(ele[0]) is dict:
            for kvpair in ele:
                thefinalele.update({kvpair['k']: kvpair['v']});
            all_elements_nice.update({thekey: thefinalele});
        elif type(ele[0]) is list:
            thesemifinalele = []
            for alternate in ele:
                thequarterfinalele = collections.OrderedDict()
                for kvpair in alternate:
                    thequarterfinalele.update({kvpair['k']: kvpair['v']});
                thesemifinalele.append(thequarterfinalele);
            all_elements_nice.update({thekey: thesemifinalele});
    
    
    
##all_elements["beacon_cardinal"] = [{"k": "seamark:type", "v": "beacon_cardinal", "t": "node"}]
##all_elements["beacon_lateral"] = [{"k": "seamark:type", "v": "beacon_lateral", "t": "node"}]
##all_elements["beacon_isolated_danger"] = [{"k": "seamark:type", "v": "beacon_isolated_danger", "t": "node"}]
##all_elements["beacon_safe_water"] = [{"k": "seamark:type", "v": "beacon_safe_water", "t": "node"}]
##all_elements["beacon_special_purpose"] = [{"k": "seamark:type", "v": "beacon_special_purpose", "t": "node"}]
#all_elements["beacon_all"] = [{"k": "seamark:type", "regv": "beacon*", "t": "node"}]
##all_elements["buoy_cardinal"] = [{"k": "seamark:type", "v": "buoy_cardinal", "t": "node"}]
##all_elements["buoy_lateral"] = [{"k": "seamark:type", "v": "buoy_lateral", "t": "node"}]
##all_elements["buoy_isolated_danger"] = [{"k": "seamark:type", "v": "buoy_isolated_danger", "t": "node"}]
##all_elements["buoy_safe_water"] = [{"k": "seamark:type", "v": "buoy_safe_water", "t": "node"}]
##all_elements["buoy_special_purpose"] = [{"k": "seamark:type", "v": "buoy_special_purpose", "t": "node"}]
#all_elements["buoy_mooring"] = [{"k": "seamark:type", "v": "mooring", "t": "node"}, {"k": "seamark:mooring:category", "v": "buoy"}]
#all_elements["buoy_all"] = [{"k": "seamark:type", "regv": "buoy*", "t": "node"}]
#all_elements["wreck"] = [{"k": "seamark:type", "v": "wreck", "t": "node"}]
#all_elements["rock"] = [{"k": "seamark:type", "v": "rock", "t": "node"}]
#all_elements["boom"] = [{"k": "seamark:type", "v": "obstruction", "t": "way"}, {"k": "seamark:obstruction:category", "v": "boom"}]
#all_elements["fence"] = [{"k": "barrier", "v": "fence", "t": "way"}]
#all_elements["borders"] = [{"k": "boundary", "v": "administrative", "t": "way"}]
#all_elements["subarine_cable"] = [{"k": "seamark:type", "v": "cable_submarine", "t": "way"}]
#all_elements["lake"] = [[{"k": "natural", "v": "water", "t": "area"}, {"k": "water", "v": "lake"}],[{"k": "natural", "v": "lake", "t": "area"}]] #or if water=lake not specified # <-- maybe add a dict around this to define multiple conditions for match.. then test if dict vs if list.. is this possible?
#all_elements["estuary"] = [{"k": "natural", "v": "water", "t": "area"}, {"k": "water", "v": "cove"}, {"k": "estuary", "v": "yes"}]
#all_elements["reservoir"] = [{"k": "natural", "v": "water", "t": "area"}, {"k": "water", "v": "reservoir"}]
#all_elements["river"] = [{"k": "natural", "v": "water", "t": "area"}, {"k": "water", "v": "river"}]
#all_elements["coral"] = [{"k": "subsea", "v": "coral", "t": "area"}]
#all_elements["gate"] = [{"k": "seamark:type", "v": "gate", "t": ["node", "area"]}]
    
    
    
    
    
    
    
    
    
def processOSMFiles(thefiles, verboose):
    if verboose:
        print ("- Processing files...")
    buildAllElementsNice();
    #pprint(all_elements_nice);
    for i, file in enumerate(thefiles):
        if verboose:
            print ("-- Processing " + file + " (file " + str(i+1) + " of " + str(len(thefiles)) + ")")
        processOSMFile(file, verboose);
        
    #pprint(node_array);
    #pprint(thefiles)
    sleep(3)






#processing rules
def handleWrecks(thepoint, w):
    infobox = "Name: ".join(thepoint.get('seamark:name', '')).join("\r\nNo further description available at this time.")
    majcat = 'NAUTICAL'
    mincat = 'WRECK'
    if thepoint['seamark:wreck:category'].lower() == "non-dangerous" or thepoint['seamark:wreck:category'].lower() == "distributed_remains":
        icon = 'PWRECKS_1_BIG'
    elif thepoint['seamark:wreck:category'].lower() == "dangerous" or thepoint['seamark:wreck:category'].lower() == "mast_showing":
        icon = 'PWRECKS_4_BIG'
    elif thepoint['seamark:wreck:category'].lower() == "hull_showing":
        icon = 'PWRECKS_5_BIG'
    else:
        icon = 'PWRECKS_4_BIG'
    
    w.point(float(thepoint['x']), float(thepoint['y']))
    w.record(
        thepoint['x'],
        thepoint['y'],
        thepoint['id'],
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
        thepoint.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    return w
    
def handleGates(thepoint, w):
    infobox = "Name: ".join(thepoint.get('seamark:name', '')).join("\r\nNo further description available at this time.")
    majcat = 'NAUTICAL'
    if thepoint['seamark:gate:category'].lower() == "dyke" \
        or thepoint['seamark:gate:category'].lower() == "lock" \
        or thepoint['seamark:gate:category'].lower() == "caisson" \
        or thepoint['seamark:gate:category'].lower() == "flood_barrage":
        mincat = 'Dyke'
        icon = 'PGATE'
    else:
        #thepoint['seamark:gate:category'].lower() == "sluice" or thepoint['seamark:gate:category'].lower() == "general"
        mincat = 'Gate'
        icon = 'PGATE'
    
    w.point(float(thepoint['x']), float(thepoint['y']))
    w.record(
        thepoint['x'],
        thepoint['y'],
        thepoint['id'],
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
        thepoint.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    return w

def handleBeaconCardinal(thepoint, w):
    infobox = "Name: ".join(thepoint.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(thepoint.get('seamark:type', ''))
    infobox.join("\r\nCategory ").join(thepoint.get('seamark:beacon_cardinal:category', ''))
    infobox.join("\r\nColour ").join(thepoint.get('seamark:beacon_cardinal:colour', ''))
    infobox.join("\r\nColour Pattern ").join(thepoint.get('seamark:beacon_cardinal:colour_pattern', ''))
    infobox.join("\r\nTopmark Shape ").join(thepoint.get('seamark:topmark:shape', ''))
    infobox.join("\r\nTopmark Colour ").join(thepoint.get('seamark:topmark:colour', ''))
    infobox.join("\r\nLight Character ").join(thepoint.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(thepoint.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(thepoint.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(thepoint.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(thepoint.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(thepoint.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Cardinal'
    
    if thepoint.get('seamark:beacon_cardinal:category', '') == "north":
        icon = "TrNorthCardinalBuoy"
    elif thepoint.get('seamark:beacon_cardinal:category', '') == "south":
        icon = "TrSouthCardinalBuoy"
    elif thepoint.get('seamark:beacon_cardinal:category', '') == "east":
        icon = "TrEastCardinalBuoy"
    elif thepoint.get('seamark:beacon_cardinal:category', '') == "west":
        icon = "TrWestCardinalBuoy"
    
    if thepoint.get('seamark:light:colour', '') != '':
        icon += "L"
    else:
        icon = icon
    
    icon += "Big"
    
    w.point(float(thepoint['x']), float(thepoint['y']))
    w.record(
        thepoint['x'],
        thepoint['y'],
        thepoint['id'],
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
        thepoint.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    return w
    
    
def handleBeaconIsolatedDanger(thepoint, w):
    infobox = "Name: ".join(thepoint.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(thepoint.get('seamark:type', ''))
    infobox.join("\r\nColour: ").join(thepoint.get('seamark:beacon_isolated_danger:colour', ''))
    infobox.join("\r\nColour Pattern: ").join(thepoint.get('seamark:beacon_isolated_danger:colour_pattern', ''))
    infobox.join("\r\nTopmark Shape: ").join(thepoint.get('seamark:topmark:shape', ''))
    infobox.join("\r\nTopmark Colour: ").join(thepoint.get('seamark:topmark:colour', ''))
    infobox.join("\r\nLight Character ").join(thepoint.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(thepoint.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(thepoint.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(thepoint.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(thepoint.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(thepoint.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Danger'
    
    icon = "TrIsoDangerBuoy"
    if thepoint.get('seamark:light:colour', '') != '':
        icon += "L"
    icon += "Big"
    
    w.point(float(thepoint['x']), float(thepoint['y']))
    w.record(
        thepoint['x'],
        thepoint['y'],
        thepoint['id'],
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
        thepoint.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    return w
    
    
def handleBeaconLateral(thepoint, w):
    infobox = "Name: ".join(thepoint.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(thepoint.get('seamark:type', ''))
    infobox.join("\r\nCategory ").join(thepoint.get('seamark:beacon_lateral:category', ''))
    infobox.join("\r\nColour ").join(thepoint.get('seamark:beacon_lateral:colour', ''))
    infobox.join("\r\nShape ").join(thepoint.get('seamark:beacon_lateral:shape', ''))
    infobox.join("\r\nTopmark Shape ").join(thepoint.get('seamark:topmark:shape', ''))
    infobox.join("\r\nSystem ").join(thepoint.get('seamark:beacon_lateral:system', ''))
    infobox.join("\r\nLight Character ").join(thepoint.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(thepoint.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(thepoint.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(thepoint.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(thepoint.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(thepoint.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Lateral'
    if thepoint.get('seamark:beacon_lateral:category', '') == "port":
        if thepoint.get('seamark:beacon_lateral:system', '') == "iala-b":
            icon = "TrPortHandBeaconRegB"
        else:
            icon = "TrPortHandBeaconRegA"
    elif thepoint.get('seamark:beacon_lateral:category', '') == "starboard":
        if thepoint.get('seamark:beacon_lateral:system', '') == "iala-b":
            icon = "TrStarboardHandBeaconRegB"
        else:
            icon = "TrStarboardHandBeaconRegA"
    else:
        #prefered channel buoys and inland buoys - as there are no default icons in IMC yet #tofix this.. for beacons
        icon = "TrBeaconGeneric";
    
    if thepoint.get('seamark:light:colour', '') != '':
        icon += "LBig"
    else:
        icon += "Big"
    
    w.point(float(thepoint['x']), float(thepoint['y']))
    w.record(
        thepoint['x'],
        thepoint['y'],
        thepoint['id'],
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
        thepoint.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    return w

    
def handleBeaconSafeWater(thepoint, w):
    infobox = "Name: ".join(thepoint.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(thepoint.get('seamark:type', ''))
    infobox.join("\r\nColour: ").join(thepoint.get('seamark:beacon_safe_water:colour', ''))
    infobox.join("\r\nColour Pattern: ").join(thepoint.get('seamark:beacon_safe_water:colour_pattern', ''))
    infobox.join("\r\nTopmark Shape: ").join(thepoint.get('seamark:topmark:shape', ''))
    infobox.join("\r\nTopmark Colour: ").join(thepoint.get('seamark:topmark:colour', ''))
    infobox.join("\r\nLight Character ").join(thepoint.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(thepoint.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(thepoint.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(thepoint.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(thepoint.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(thepoint.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Safe Water'
    
    icon = "TrSafeWatersBuoy"
    if thepoint.get('seamark:light:colour', '') != '':
        icon += "L"
    
    w.point(float(thepoint['x']), float(thepoint['y']))
    w.record(
        thepoint['x'],
        thepoint['y'],
        thepoint['id'],
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
        thepoint.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    return w
    
def handleBeaconSpecialPurpose(thepoint, w):
    infobox = "Name: ".join(thepoint.get('seamark:name', '')).join("\r\nCategory: ").join(thepoint.get('seamark:beacon_special_purpose:category', '')).join("\r\nNo further description available at this time.")
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Special Purpose'
    
    icon = "TrSpecialPurposeBuoyYellow"
    if thepoint.get('seamark:light:colour', '') != '':
        icon += "L"
    
    w.point(float(thepoint['x']), float(thepoint['y']))
    w.record(
        thepoint['x'],
        thepoint['y'],
        thepoint['id'],
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
        thepoint.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    return w
    
    


def handleBuoyCardinal(thepoint, w):
    infobox = "Name: ".join(thepoint.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(thepoint.get('seamark:type', ''))
    infobox.join("\r\nCategory ").join(thepoint.get('seamark:buoy_cardinal:category', ''))
    infobox.join("\r\nColour ").join(thepoint.get('seamark:buoy_cardinal:colour', ''))
    infobox.join("\r\nColour Pattern ").join(thepoint.get('seamark:buoy_cardinal:colour_pattern', ''))
    infobox.join("\r\nTopmark Shape ").join(thepoint.get('seamark:topmark:shape', ''))
    infobox.join("\r\nTopmark Colour ").join(thepoint.get('seamark:topmark:colour', ''))
    infobox.join("\r\nLight Character ").join(thepoint.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(thepoint.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(thepoint.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(thepoint.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(thepoint.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(thepoint.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Cardinal'
    
    if thepoint.get('seamark:buoy_cardinal:category', '') == "north":
        icon = "TrNorthCardinalBuoy"
    elif thepoint.get('seamark:buoy_cardinal:category', '') == "south":
        icon = "TrSouthCardinalBuoy"
    elif thepoint.get('seamark:buoy_cardinal:category', '') == "east":
        icon = "TrEastCardinalBuoy"
    elif thepoint.get('seamark:buoy_cardinal:category', '') == "west":
        icon = "TrWestCardinalBuoy"
    
    if thepoint.get('seamark:light:colour', '') != '':
        icon += "L"
    else:
        icon = icon
    
    icon += "Big"
    
    w.point(float(thepoint['x']), float(thepoint['y']))
    w.record(
        thepoint['x'],
        thepoint['y'],
        thepoint['id'],
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
        thepoint.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    return w
    
def handleBuoyIsolatedDanger(thepoint, w):
    infobox = "Name: ".join(thepoint.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(thepoint.get('seamark:type', ''))
    infobox.join("\r\nColour: ").join(thepoint.get('seamark:buoy_isolated_danger:colour', ''))
    infobox.join("\r\nColour Pattern: ").join(thepoint.get('seamark:buoy_isolated_danger:colour_pattern', ''))
    infobox.join("\r\nTopmark Shape: ").join(thepoint.get('seamark:topmark:shape', ''))
    infobox.join("\r\nTopmark Colour: ").join(thepoint.get('seamark:topmark:colour', ''))
    infobox.join("\r\nLight Character ").join(thepoint.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(thepoint.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(thepoint.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(thepoint.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(thepoint.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(thepoint.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Danger'
    
    icon = "TrIsoDangerBuoy"
    if thepoint.get('seamark:light:colour', '') != '':
        icon += "L"
    icon += "Big"
    
    w.point(float(thepoint['x']), float(thepoint['y']))
    w.record(
        thepoint['x'],
        thepoint['y'],
        thepoint['id'],
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
        thepoint.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    return w

def handleBuoyLateral(thepoint, w):
    infobox = "Name: ".join(thepoint.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(thepoint.get('seamark:type', ''))
    infobox.join("\r\nCategory ").join(thepoint.get('seamark:buoy_lateral:category', ''))
    infobox.join("\r\nColour ").join(thepoint.get('seamark:buoy_lateral:colour', ''))
    infobox.join("\r\nShape ").join(thepoint.get('seamark:buoy_lateral:shape', ''))
    infobox.join("\r\nTopmark Shape ").join(thepoint.get('seamark:topmark:shape', ''))
    infobox.join("\r\nSystem ").join(thepoint.get('seamark:buoy_lateral:system', ''))
    infobox.join("\r\nLight Character ").join(thepoint.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(thepoint.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(thepoint.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(thepoint.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(thepoint.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(thepoint.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Lateral'
    
    if thepoint.get('seamark:buoy_lateral:category', '') == "port":
        if thepoint.get('seamark:buoy_lateral:shape', '') == "pillar" or \
        thepoint.get('seamark:buoy_lateral:shape', '') == "spar" or \
        thepoint.get('seamark:buoy_lateral:shape', '') == "ice_buoy" or \
        thepoint.get('seamark:buoy_lateral:shape', '') == "super-buoy":
            if thepoint.get('seamark:buoy_lateral:system', '') == "iala-b":
                icon = "TrPortHandBuoyRegB"
            else:
                icon = "TrPortHandBuoyRegA"
        else:
            #includes conical, can, spherical, barrel
            if thepoint.get('seamark:buoy_lateral:system', '') == "iala-b":
                icon = "TrBuoyFinalGreen"
            else:
                icon = "TrBuoyFinalRed"
    elif thepoint.get('seamark:buoy_lateral:category', '') == "starboard":
        if thepoint.get('seamark:buoy_lateral:shape', '') == "pillar" or \
        thepoint.get('seamark:buoy_lateral:shape', '') == "spar" or \
        thepoint.get('seamark:buoy_lateral:shape', '') == "ice_buoy" or \
        thepoint.get('seamark:buoy_lateral:shape', '') == "super-buoy":
            if thepoint.get('seamark:buoy_lateral:system', '') == "iala-b":
                icon = "TrStarboardHandBuoyRegB"
            else:
                icon = "TrStarboardHandBuoyRegA"
        else:
            #includes conical, can, spherical, barrel
            if thepoint.get('seamark:buoy_lateral:system', '') == "iala-b":
                icon = "TrBuoyFinalRed"
            else:
                icon = "TrBuoyFinalGreen"
    else:
        #prefered channel buoys and inland buoys - as there are no default icons in IMC yet
        icon = "TrBuoyFinalWhite";
    
    if thepoint.get('seamark:light:colour', '') != '':
        icon += "L"
    else:
        icon = icon
    
    w.point(float(thepoint['x']), float(thepoint['y']))
    w.record(
        thepoint['x'],
        thepoint['y'],
        thepoint['id'],
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
        thepoint.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    return w

def handleBuoySafeWater(thepoint, w):
    infobox = "Name: ".join(thepoint.get('seamark:name', ''))
    infobox.join("\r\nType: ").join(thepoint.get('seamark:type', ''))
    infobox.join("\r\nColour: ").join(thepoint.get('seamark:buoy_safe_water:colour', ''))
    infobox.join("\r\nColour Pattern: ").join(thepoint.get('seamark:buoy_safe_water:colour_pattern', ''))
    infobox.join("\r\nTopmark Shape: ").join(thepoint.get('seamark:topmark:shape', ''))
    infobox.join("\r\nTopmark Colour: ").join(thepoint.get('seamark:topmark:colour', ''))
    infobox.join("\r\nLight Character ").join(thepoint.get('seamark:light:character', ''))
    infobox.join("\r\nLight Colour ").join(thepoint.get('seamark:light:colour', ''))
    infobox.join("\r\nLight Period ").join(thepoint.get('seamark:light:period', ''))
    infobox.join("\r\nLight Height ").join(thepoint.get('seamark:light:height', ''))
    infobox.join("\r\nLight Range ").join(thepoint.get('seamark:light:range', ''))
    infobox.join("\r\nLight Reference ").join(thepoint.get('seamark:light:reference', ''))
    
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Safe Water'
    
    icon = "TrSafeWatersBuoy"
    if thepoint.get('seamark:light:colour', '') != '':
        icon += "L"
    
    w.point(float(thepoint['x']), float(thepoint['y']))
    w.record(
        thepoint['x'],
        thepoint['y'],
        thepoint['id'],
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
        thepoint.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    return w
    
def handleBuoySpecialPurpose(thepoint, w):
    infobox = "Name: ".join(thepoint.get('seamark:name', '')).join("\r\nCategory: ").join(thepoint.get('seamark:buoy_special_purpose:category', '')).join("\r\nNo further description available at this time.")
    majcat = 'NAUTICAL'
    mincat = 'Beacon/Buoy - Special Purpose'
    
    icon = "TrSpecialPurposeBuoyYellow"
    if thepoint.get('seamark:light:colour', '') != '':
        icon += "L"
    
    w.point(float(thepoint['x']), float(thepoint['y']))
    w.record(
        thepoint['x'],
        thepoint['y'],
        thepoint['id'],
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
        thepoint.get('seamark:name', ''),
        majcat,
        mincat,
        icon,
        icon
    )
    return w


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