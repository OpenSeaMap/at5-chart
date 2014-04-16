from functions4common import *

def handleArgs(args):
    if args.list_elements_debug:
        printElementsByKey(True)
    elif args.list_elements:
        printElementsByKey(False)
    print(args)
    #downloadOSM(False)
    return (None, args.verboose)



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
        icon = icon.join("L")
    else:
        icon = icon
    
    icon.join("Big")
    
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
        icon.join("L")
    icon.join("Big")
    
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
        icon.join("L")
    
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
        icon.join("L")
    
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
        icon = icon.join("L")
    else:
        icon = icon
    
    icon.join("Big")
    
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
        icon.join("L")
    icon.join("Big")
    
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
        icon = icon.join("L")
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
        icon.join("L")
    
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
        icon.join("L")
    
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




def writeRecordPoint():

    return 1