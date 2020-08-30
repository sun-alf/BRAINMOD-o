import xml.etree.ElementTree as ET;

#
# Script setup values
#
TARGET_WEAPONS_XML = r'D:\Programs\JaggedAlliance2\Data-AIM\TableData\Items\Weapons.xml';
OUTPUT_WEAPONS_XML = r'D:\Programs\JaggedAlliance2\Data-AIM\TableData\Items\Weapons_NEW.xml';

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


def GetOutputLine(uiIndex, ubWeaponClass, szWeaponName, rng_tiles, rng_meters):
    weaponName = '\"' + str(szWeaponName) + '\"';
    return str(uiIndex) +','+ str(ubWeaponClass) +','+ weaponName +','+ str(rng_tiles) +','+ str(rng_meters) + '\n';


def GenerateCSV(root):
    file1 = open("output.csv", "w");
    file1.write("Index,Class,Name,\"Range (t)\",\"Range (m)\"\n");
    
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
        
        if ubWeaponClass == "Carbine" and ubWeaponType == "Rifle":
            ubWeaponClass = "Assault rifle";
        
        if ubWeaponClass == "Melee" or ubWeaponClass == "Others" or ubWeaponClass == "N/a":
            continue;
        
        rng_tiles = int(int(usRange) / 10);
        rng_meters = rng_tiles * 4;  # 1 tile == 4 meters
        file1.write(GetOutputLine(uiIndex, ubWeaponClass, szWeaponName, rng_tiles, rng_meters));
    #end for child in root:
    
    print("CSV DONE!");
    file1.close();
#end def GenerateCSV(root):


def ModifyOriginalXML(root, outFileName):
    foldingItems = [];

    maxRng = 0;
    manRngName = "";
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
        
        if ubWeaponClass == "Carbine" and ubWeaponType == "Rifle":
            ubWeaponClass = "Assault rifle";
        
        rng_tiles = int(int(usRange) / 10);
        rng_meters = rng_tiles * 4;
        if rng_tiles > maxRng:
            maxRng = rng_tiles;
            manRngName = szWeaponName;
            
        if rng_tiles > 250:
            print(szWeaponName + " -- " +  str(rng_tiles));
        """
        if szWeaponName.find("- folded") != -1 or szWeaponName.find("- collapsed") != -1:
            item = {};
            idx_fold = szWeaponName.find("- folded");
            idx_coll = szWeaponName.find("- collapsed");
            if idx_fold != -1:
                item["name"] = szWeaponName[: idx_fold];
            else:
                item["name"] = szWeaponName[: idx_coll];
            iten["fold_rng"] = 
            foldingItems.append(item);"""
    #end for child in root:
    
    print("XML DONE! max rng = " + str(maxRng) + "    // " + manRngName);
#end def ModifyOriginalXML(root, outFileName):


def ModifyXML_IncreaseFirearmsLoudness(root, percents):
    result = False;
    for child in root:
        attVolumeObj = None;
        for piska in child:
            if piska.tag == "ubAttackVolume":
                ubAttackVolume = piska.text;  # already in tiles, but it is string yet
                attVolumeObj = piska;
        
        if attVolumeObj is not None:  # attribute "ubAttackVolume" exists
            rng_tiles = int(ubAttackVolume);
            if rng_tiles > 5:
                rng_tiles = rng_tiles + int(rng_tiles * percents / 100);
                attVolumeObj.text = str(rng_tiles);
                result = True;
    #end for child in root:
    
    print("XML DONE! modified = " + str(result));
    return result;
#end def ModifyXML_IncreaseFirearmsLoudness(root, percent):


#
# Entry point (like Main())
#
tree = ET.parse(TARGET_WEAPONS_XML);
root = tree.getroot();
modified = ModifyXML_IncreaseFirearmsLoudness(root, 25);
if modified:
    tree.write(OUTPUT_WEAPONS_XML);

