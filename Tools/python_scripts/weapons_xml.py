import xml.etree.ElementTree as ET;

#
# Script setup values
#
TARGET_WEAPONS_XML = r'D:\Programs\JaggedAlliance2\Data-AIM\TableData\Items\Weapons.xml';
OUTPUT_WEAPONS_XML = r'D:\Programs\JaggedAlliance2\Data-AIM\TableData\Items\Weapons_NEW.xml';
TARGET_EXPLOSIVES_XML = r'D:\Programs\JaggedAlliance2\Data-AIM\TableData\Items\Explosives.xml';
OUTPUT_EXPLOSIVES_XML = r'D:\Programs\JaggedAlliance2\Data-AIM\TableData\Items\Explosives_NEW.xml';

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
    weaponName = "\"{0}\"".format(szWeaponName.encode('ascii', 'ignore').replace('\"', '\'\''));
    return str(uiIndex) +','+ str(ubWeaponClass) +','+ weaponName +','+ str(rng_tiles) +','+ str(rng_meters) + ','+ str(ubAttackVolume) + '\n';
#end def GetOutputLine(uiIndex, ubWeaponClass, szWeaponName, rng_tiles, rng_meters, ubAttackVolume):


def GenerateCSV(root):
    file1 = open("output.csv", "w");
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
        rng_meters = rng_tiles * 4;  # 1 tile == 4 meters
        file1.write(GetOutputLine(uiIndex, ubWeaponClass, szWeaponName, rng_tiles, rng_meters, ubAttackVolume));
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


#
# Entry point (like Main())
#
tree = ET.parse(TARGET_WEAPONS_XML);
root = tree.getroot();
#GenerateCSV(root);

modified = False;
#modified = modified or ModifyXML_IncreaseFirearmsLoudness(root, 6, [29, 205, 1]);
#modified = modified or ModifyXML_IncreaseFirearmsRange(root, 9, [41, 77, 1]);
if modified:
    tree.write(OUTPUT_WEAPONS_XML);

ModifyXML_SetExplosivesLoudness(1.70, [10, 1000]);
