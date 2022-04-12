#### USAGE ####
# 0. Ensure you have !!! Python 3 !!! installed (version 3.x -- does not matter).
# 1. Run this script (i.e. "mercs_starting_gear.py") in a cmd line window with the following arguments format:
#    mercs_starting_gear.py  <cmd>  <arg1>  <arg2> ...
#    <cmd>  :
#      l - list all, no args.
#      f - fix total costs; <arg1> - discount % ("-10", "5", "+3" etc); <arg2> - affected merc type ("all", "aim", "merc").
#          other args: "nice" - round up cost to hundreds//, "nice-" - round floor cost to hundreds.
# 
#  "mercs_starting_gear.py  f -10" - will put fair [real] total costs in MercStartingGear.xml with -10% off.
#  "mercs_starting_gear.py  f 5"   - will put fair [real] total costs in MercStartingGear.xml with +5% surplus.


import os, sys;
import xml.etree.ElementTree as ET;
import math;

#
# Script setup values
#
SWDIR = os.getcwd();
TABLE_DATA_ROOT = r'{}\..\..\Data-BRAINMOD\TableData'.format(SWDIR);
TABLE_DATA_ROOT = r'D:\Programs\JaggedAlliance2\Data-BRAINMOD\TableData';
INVENTORY_DATA_ROOT = os.path.join(TABLE_DATA_ROOT, "Inventory");
ITEMS_DATA_ROOT = os.path.join(TABLE_DATA_ROOT, "Items");


#
# Constants, functions, classes etc
#
class MercTypes():
    ALL = 0;
    AIM = 1;
    MERC = 2;
    RPC = 3;
    NPC = 4;
    MAX_VAL = NPC;
    
    @classmethod
    def ToType(cls, param):
        if param.lower() == "all":
            return cls.ALL;
        elif param.lower() == "aim":
            return cls.AIM;
        elif param.lower() == "merc":
            return cls.MERC;
        return None;
    #end def ToType(cls, param):
    
    @classmethod
    def IsValidType(cls, param):
        result = False;
        if type(param) == int:
            result = (cls.ALL <= param) and (param <= cls.MAX_VAL);
        elif type(param) == str:
            result = cls.ToType(param) != None;
        return result;
    #end def ToType(cls, param):
#end class MercTypes():


def _GetTagValue(item, tagName):
    for tagObj in item:
        if tagObj.tag == tagName:
            return tagObj.text;
    return None;
#end def _GetTagValue(item, tagName):

def _SetTagValue(item, tagName, tagValue):
    for tagObj in item:
        if tagObj.tag == tagName:
            tagObj.text = tagValue;
            return True;
    return False;
#end def _SetTagValue(item, tagName, tagValue):

def _GetItemName(itemXmlObj):
    result = "?None?";
    for tagObj in itemXmlObj:
        if tagObj.tag == "szLongItemName":
            result = tagObj.text;
            break;
    if result == None:
        result = "0";
    return result;
#end def _GetItemName(itemXmlObj):

def _GetItemCost(itemXmlObj):
    result = None;
    for tagObj in itemXmlObj:
        if tagObj.tag == "usPrice":
            result = int(tagObj.text);
            break;
    if result == None:
        result = 0;
    return result;
#end def _GetItemCost(itemXmlObj):

def _DoesTypeMatch(profilesRoot, index, selectedType):
    if selectedType == MercTypes.ALL:
        return True;
    
    mercProfile = profilesRoot[index];
    if int(mercProfile[0].text) != index:  # tag mercProfile[0] is "uiIndex", must match.
        raise Exception("Merc Profiles XML is malformed at index", index);
    
    return int(mercProfile[1].text) == selectedType;
#end def _DoesTypeMatch(profilesRoot, index, selectedType):

def _CalcGearkitCost(itemsRoot, gearkit):
    result = 0;
    itemId = 0;
    itemCost = 0;
    for child in gearkit:
        if child.tag == "mPriceMod" or child.tag == "mGearKitName" or child.tag == "mAbsolutePrice" or \
                child.tag.find("Drop") != -1 or child.tag.find("Status") != -1:
            continue;
        if child.tag.find("Quantity") != -1:
            itemQty = int(child.text);
            if itemId != 0:
                result = result - itemCost + itemQty * itemCost;
                itemId = 0;
        else:
            itemId = int(child.text);
            if itemId != 0:
                itemCost = _GetItemCost(itemsRoot[itemId]);
                result = result + itemCost;
    return result;
#end def _CalcGearkitCost(itemsRoot, gearkit):


def PrintGearKits(root, itemsRoot, profilesRoot, args):    
    selectedType = MercTypes.ALL;
    if len(args) >= 1 and IsValidType(args[0]):
        selectedType = args[0];
    
    for mercgear in root:
        index = int(mercgear[0].text);
        name = mercgear[1].text;
        gearkits = mercgear[2 : ];
        
        if name == None or name == "":  # skip empty merc entry
            continue;
        
        if _DoesTypeMatch(profilesRoot, index, selectedType):
            gkText = "";
            for gkIdx in range(0, len(gearkits)):
                fairCost = 0;
                if len(gearkits[gkIdx]) > 2:  # non-valid gearkits are almost empty
                    fairCost = _CalcGearkitCost(itemsRoot, gearkits[gkIdx]);
                gkText = "{}kit{} = ${} | ".format(gkText, gkIdx + 1, fairCost);
            print("[{}] {} ({})".format(index, name, gkText));
    #end for mercgear in root:
    
    return False;
#end PrintGearKits(root, itemsRoot, profilesRoot, args):


def FixGearKitsCost(root, itemsRoot, profilesRoot, args):
    result = False;
    
    priceMod = args[0];
    selectedType = args[1];
    nice = False;
    if len(args) >= 3 and args[2].lower() == "nice":
        nice = True;
    
    for mercgear in root:
        index = int(mercgear[0].text);
        name = mercgear[1].text;
        gearkits = mercgear[2 : ];
        
        if name == None or name == "":  # skip empty merc entry
            continue;
        
        if _DoesTypeMatch(profilesRoot, index, selectedType):
            gkText = "";
            print("[{}] {}:".format(index, name));
            for gkIdx in range(0, len(gearkits)):
                fairCost = 0;
                if len(gearkits[gkIdx]) > 2:  # non-valid gearkits are almost empty
                    fairCost = _CalcGearkitCost(itemsRoot, gearkits[gkIdx]);
                else:
                    continue;
                
                currentCost = _GetTagValue(gearkits[gkIdx], "mAbsolutePrice");
                
                altCost = fairCost;
                if priceMod != 0:
                    altCost = altCost * ((priceMod + 100) / 100.0);
                
                if nice == True:
                    altCost = math.ceil(altCost / 100.0) * 100.0;
                
                overflowWarningText = "";
                if altCost > 32000:
                    overflowWarningText = "!!! exceeds 32000 !!!";
                
                # now let's apply new values back to XML tree
                altCost = min(int(altCost), 32000);
                if nice == True:  # both price modifier and "nicefication" are applied, then the only way to force JA2.exe to show our decired price is
                    _SetTagValue(gearkits[gkIdx], "mPriceMod", "0");                 # disable this just in case, and
                    _SetTagValue(gearkits[gkIdx], "mAbsolutePrice", str(altCost));   # set this.
                else:  # only price modifier is applied -- let JA2.exe do rest work by setting "mPriceMod"
                    _SetTagValue(gearkits[gkIdx], "mPriceMod", str(priceMod));
                    _SetTagValue(gearkits[gkIdx], "mAbsolutePrice", "-1");
                
                # print log to terminal
                print("    kit{}: cur=${} | ${} --> ${}  {}".format(gkIdx + 1, currentCost, fairCost, altCost, overflowWarningText));
                result = True;
            print("");
    #end for mercgear in root:
    
    return result;
#end def FixGearKitsCost(root, itemsRoot, profilesRoot, args):

#
# Entry point (like Main())
#

fileName = "MercStartingGear.xml";
newfileName = "NEW_MercStartingGear.xml";

cmdFunc = None;
args = [];

for i in range(1, len(sys.argv)):
    if i == 1 and sys.argv[i] == 'l':
        cmdFunc = PrintGearKits;
    elif i == 1 and sys.argv[i] == 'f':
        cmdFunc = FixGearKitsCost;
    else:
        dec = 0;
        
        try:
            dec = int(sys.argv[i]);
        except Exception as e:
            dec = MercTypes.ToType(sys.argv[i]);
            if dec == None:
                dec = sys.argv[i];
            #args.append(int(argv[i]));
        
        args.append(dec);


if (cmdFunc == None) and (len(args) == 0):
    cmdFunc = PrintGearKits;

if cmdFunc != None:
    itemsTree = ET.parse(os.path.join(ITEMS_DATA_ROOT, "Items.xml"));
    itemsRoot = itemsTree.getroot();
    
    profilesTree = ET.parse(os.path.join(TABLE_DATA_ROOT, "MercProfiles.xml"));
    profilesRoot = profilesTree.getroot();
    
    tree = ET.parse(os.path.join(INVENTORY_DATA_ROOT, fileName));
    root = tree.getroot();
    
    dirty = cmdFunc(root, itemsRoot, profilesRoot, args);
    
    if dirty:
        f = open(os.path.join(INVENTORY_DATA_ROOT, newfileName), "wb");
        f.write(bytearray(r'<?xml version="1.0" encoding="utf-8"?>' + '\n', "utf-8"));
        tree.write(f, encoding="utf-8", xml_declaration=None, default_namespace=None, method="xml");
        f.close();
else:
    print("Invalid input arguments.");
