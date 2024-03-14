#### USAGE ####
# 0. Ensure you have !!! Python 3 !!! installed (version 3.x -- does not matter).
# 1. Edit Main(); no CmdLineProcessor integration =(
# 2. Run this script (i.e. "weapons_xml.py") in a cmd line window.
#

import codecs;
import xml.etree.ElementTree as ET;
from imports.JA2TableData import JA2TableData, JA2Workspaces, JA2Xmls, SWDIR;
from imports.xml_utils import XmlUtils;
from imports.cmd_line import CmdLineProcessor;

#
# Script setup values
#
TARGET_WEAPONS_XML = r'{}\..\..\Data-BRAINMOD\TableData\Items\Weapons.xml'.format(SWDIR);
OUTPUT_WEAPONS_XML = r'{}_NEW'.format(TARGET_WEAPONS_XML);
TARGET_EXPLOSIVES_XML = r'{}\..\..\Data-BRAINMOD\TableData\Items\Explosives.xml'.format(SWDIR);
OUTPUT_EXPLOSIVES_XML = r'{}_NEW'.format(TARGET_EXPLOSIVES_XML);


#
# Constants, functions, classes etc
#
def WeaponClassText(code):
    if code == '1': return "Pistol";
    if code == '2': return "SMG";
    if code == '3': return "Carbine";
    if code == '4': return "LMG";
    if code == '5': return "Shotgun";
    if code == '6': return "Melee";
    if code == '7': return "Others";
    return "N/a";


def WeaponTypeText(code):
    if code == '6': return "Rifle";
    return "N/a";


def GetOutputLine(uiIndex, ubWeaponClass, szWeaponName, rng_tiles, rng_meters, ubAttackVolume):
    raz = szWeaponName.encode('ascii', 'ignore');
    dwa = szWeaponName.replace('\"', '\'\'');
    weaponName = "\"{0}\"".format(dwa);
    return str(uiIndex) +','+ str(ubWeaponClass) +','+ weaponName +','+ str(rng_tiles) +','+ str(rng_meters) + ','+ str(ubAttackVolume) + '\n';
#end def GetOutputLine(uiIndex, ubWeaponClass, szWeaponName, rng_tiles, rng_meters, ubAttackVolume):


def GenerateCSV(root):
    file1 = codecs.open("output.csv", "w", "utf-8");
    file1.write(u'\ufeff');
    file1.write("Index,Class,Name,\"Range (t)\",\"Range (m)\",Volume\n");
    
    for child in root:
        for piska in child:
            if piska.tag == "uiIndex":
                uiIndex = piska.text;
            if piska.tag == "ubWeaponClass":
                ubWeaponClass = WeaponClassText(piska.text);
            if piska.tag == "ubWeaponType":
                ubWeaponType = WeaponTypeText(piska.text);
            if piska.tag == "szWeaponName":
                szWeaponName = piska.text;
            if piska.tag == "usRange":
                usRange = piska.text;
            if piska.tag == "ubAttackVolume":
                ubAttackVolume = piska.text;
        
        if ubWeaponClass == "Carbine" and ubWeaponType == "Rifle":
            ubWeaponClass = "Assault rifle";
        
        if ubWeaponClass == "Melee" or ubWeaponClass == "Others" or ubWeaponClass == "N/a":
            continue;
        
        rng_tiles = int(int(usRange) / 10);
        rng_meters = rng_tiles #* 4;  # 1 tile == 4 meters
        
        line = GetOutputLine(uiIndex, ubWeaponClass, szWeaponName, rng_tiles, rng_meters, ubAttackVolume);
        try:
            file1.write(line);
        except Exception:
            print("Failed at: {}".format(line));
    #end for child in root:
    
    print("CSV DONE!");
    file1.close();
#end def GenerateCSV(root):


def ModifyXML_IncreaseFirearmsRange(root, percents, tresholds):
    result = False;
    foldingItems = [];

    maxRng = 0;
    manRngName = "";
    for child in root:
        for piska in child:
            if piska.tag == "uiIndex":
                uiIndex = piska.text;
            if piska.tag == "szWeaponName":
                szWeaponName = piska.text;
            if piska.tag == "usRange":
                usRange = piska.text;
                rangeObj = piska;

        rng_tiles = int(int(usRange) / 10);
        rng_meters = rng_tiles * 4;
        if rng_tiles > maxRng:
            maxRng = rng_tiles;
            manRngName = szWeaponName;
            
        if rng_tiles >= 250:
            print("{0} -- {1}  ({2} m)".format(szWeaponName, str(rng_tiles), str(rng_meters)));

        if rangeObj is not None:  # attribute "usRange" exists
            if rng_tiles > tresholds[0] and rng_tiles < tresholds[1]:
                adjustment = max(tresholds[2], int(rng_tiles * percents / 100));
                new_range = (rng_tiles + adjustment) * 10;  # usRange is in units "10 units per tile"
                rangeObj.text = str(new_range);
                result = True;
    #end for child in root:
    
    print("XML DONE! max rng = " + str(maxRng) + "    // " + manRngName);
    return result;
#end def ModifyXML_IncreaseFirearmsRange(root, percents, tresholds):


def ModifyXML_IncreaseFirearmsLoudness(root, percents, tresholds):
    result = False;
    for child in root:
        attVolumeObj = None;
        for piska in child:
            if piska.tag == "ubAttackVolume":
                ubAttackVolume = piska.text;  # already in tiles, but it is string yet
                attVolumeObj = piska;
        
        if attVolumeObj is not None:  # attribute "ubAttackVolume" exists
            rng_tiles = int(ubAttackVolume);
            if rng_tiles > tresholds[0] and rng_tiles < tresholds[1]:
                adjustment = max(tresholds[2], int(rng_tiles * percents / 100));
                rng_tiles = min(rng_tiles + adjustment, 255);  # "ubAttackVolume" is of UINT8 type, trim to 255
                attVolumeObj.text = str(rng_tiles);
                result = True;
    #end for child in root:
    
    print("XML DONE! modified = " + str(result));
    return result;
#end def ModifyXML_IncreaseFirearmsLoudness(root, percents, tresholds):


def ModifyXML_SetExplosivesLoudness(coef, tresholds):
    tree = ET.parse(TARGET_EXPLOSIVES_XML);
    root = tree.getroot();
    
    result = False;
    for child in root:
        attVolumeObj = None;
        for piska in child:
            if piska.tag == "ubType":
                ubType = piska.text;
            if piska.tag == "ubVolume":
                ubVolume = piska.text;  # already in tiles, but it is string yet
                attVolumeObj = piska;
            if piska.tag == "ubDamage":
                ubDamage = piska.text;
            if piska.tag == "ubRadius":
                ubRadius = piska.text;
                
        if ubType == "0" and int(ubRadius) > 1 and attVolumeObj is not None:  # impact type is explosion and attribute "ubVolume" exists
            rng_tiles = (int(ubDamage) + int(ubRadius)) * coef;
            if rng_tiles > tresholds[0] and rng_tiles < tresholds[1]:
                rng_tiles = min(int(rng_tiles), 255);  # "ubVolume" is of UINT8 type, trim to 255
                attVolumeObj.text = str(rng_tiles);
                result = True;
    #end for child in root:
    
    print("XML DONE! modified = " + str(result));
    if result:
        tree.write(OUTPUT_EXPLOSIVES_XML);
    return result;
#end def ModifyXML_SetExplosivesLoudness(coef, tresholds):


def ModifyXML_ChangeExplosivesLoudness(percents, tresholds):
    tree = ET.parse(TARGET_EXPLOSIVES_XML);
    root = tree.getroot();
    
    result = False;
    for child in root:
        attVolumeObj = None;
        for piska in child:
            if piska.tag == "ubType":
                ubType = piska.text;
            if piska.tag == "ubVolume":
                ubVolume = piska.text;  # already in tiles, but it is string yet
                attVolumeObj = piska;
            if piska.tag == "ubRadius":
                ubRadius = piska.text;
                
        if ubType == "0" and int(ubRadius) > 1 and attVolumeObj is not None:  # impact type is explosion and attribute "ubVolume" exists
            if int(ubVolume) > tresholds[0] and int(ubVolume) < tresholds[1]:
                adjustment = int(int(ubVolume) * percents / 100);
                rng_tiles = min(int(int(ubVolume) + adjustment), 255);  # "ubVolume" is of UINT8 type, trim to 255
                attVolumeObj.text = str(rng_tiles);
                result = True;
    #end for child in root:
    
    print("XML DONE! modified = " + str(result));
    if result:
        tree.write(OUTPUT_EXPLOSIVES_XML);
    return result;
#end def ModifyXML_ChangeExplosivesLoudness(percents, tresholds):


#
# Entry point (like Main())
#
tree = ET.parse(TARGET_WEAPONS_XML);
root = tree.getroot();
#GenerateCSV(root);

# tresholds (all integers): [min, max, min_value_to_apply]
#   'min' - min range to touch, all guns with range <= 'min' will be skipped. Use 0 to remove this margin.
#   'max' - max range to touch, all guns with range >= 'max' will be skipped. Use 65535 to remove this margin.
#   'min_value_to_apply' - all affected ranges will be changed by at least this value. Example: increase by 3% gives 0.2 tiles to add, and it is wanted to +1 anyway in this case.
modified = False;
modified = ModifyXML_IncreaseFirearmsLoudness(root, 300, [0, 65000, 1]) or modified;
modified = ModifyXML_IncreaseFirearmsRange(root, 300, [0, 65000, 1]) or modified;
if modified:
    tree.write(OUTPUT_WEAPONS_XML);

#ModifyXML_SetExplosivesLoudness(1.70, [10, 1000]);
# ModifyXML_ChangeExplosivesLoudness(300, [0, 5000]);

tree2 = ET.parse(OUTPUT_WEAPONS_XML);
root2 = tree2.getroot();
GenerateCSV(root2);
