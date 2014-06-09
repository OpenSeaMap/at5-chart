import shapefile
import xml.etree.ElementTree as ET
import argparse

from functions4points import *


#http://overpass.osm.rambler.ru/cgi/interpreter?data=[out:json];(node["seamark:type"~"buoy*"](1.0553144713908544,103.41430664062499,1.5962442743900633,104.315185546875));out;
#1.5962442743900633 1.0553144713908544 103.41430664062499 104.315185546875"


#s w n e

thefile = ET.parse('allbuoys-2014-05-23_singapore.osm')
#thefile = ET.parse('allbeacons-2014-05-23_singapore.osm')
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
    elif point['stype'] == "beacon_lateral":
        w = handleBeaconLateral(point, w)
    elif point['stype'] == "beacon_safe_water":
        w = handleBeaconSafeWater(point, w)
    elif point['stype'] == "beacon_special_purpose":
        w = handleBeaconSpecialPurpose(point, w)


w.save('allbuoys-2014-05-23_singapore')
#w.save('allbeacons-2014-05-23_singapore')
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

