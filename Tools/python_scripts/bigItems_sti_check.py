import os, sys;
import xml.etree.ElementTree as ET;

#
# Script setup values
#
SWDIR = os.getcwd();
BIG_ITEMS_ROOT = r'{}\..\..\Data-BRAINMOD\BigItems'.format(SWDIR);
TABLE_DATA_ROOT = r'{}\..\..\Data-BRAINMOD\TableData'.format(SWDIR);
ITEMS_XML_PATH = r'{}\Items\Items.xml'.format(TABLE_DATA_ROOT);


#
# Constants, functions, classes etc
#
ITEM_CLASS_GUN = 2;
ITEM_CLASS_BLADE = 4;
ITEM_CLASS_THRKNIFE = 8;
ITEM_CLASS_LAUNCHER = 16;

def LoadGunsSti(stiDir):
    def _FetchStiId(fileName, pattern):
        stiId = None;
        parts = fileName.lower().split(pattern);
        if len(parts) == 2:
            subparts = parts[1].split(".sti");
            if len(subparts) == 2:
                stiId = subparts[0];
            else:
                raise Exception("Bad fileName[2] ", fileName);
        else:
            raise Exception("Bad fileName ", fileName);
        return stiId;
    #end def _FetchStiId(fileName):

    stiIdList = [];
    
    for objectName in os.listdir(stiDir):
        objectPath = os.path.join(stiDir, objectName);
        if os.path.isfile(objectPath):
            if objectName.lower().find("gun") != -1:
                stiIdList.append(_FetchStiId(objectName, "gun"));
    
    return stiIdList;
#end def LoadGunsSti(stiDir):

def LookupStiUsage(root, stiId, graphicType, printAll):
    def _IsValidItemClass(validItemClasses, targetItemClass):
        return False;
    #end def _IsValidItemClass(validItemClasses, targetItemClass):
    
    result = 0;
    for itemIdx in range(0, len(root)):
        child = root[itemIdx];
        
        uiIndex = None;
        szLongItemName = None;
        ubGraphicNum = None;
        usItemClass = None;
        ubGraphicType = None;
        for tagObj in child:
            if tagObj.tag == "uiIndex":
                uiIndex = tagObj.text;
            elif tagObj.tag == "szLongItemName":
                szLongItemName = tagObj.text;
            elif tagObj.tag == "ubGraphicNum":
                ubGraphicNum = tagObj.text;
            elif tagObj.tag == "usItemClass":
                usItemClass = tagObj.text;
            elif tagObj.tag == "ubGraphicType":
                ubGraphicType = tagObj.text;
            
            if uiIndex != None and szLongItemName != None and ubGraphicNum != None and usItemClass != None and ubGraphicType != None:
                break;
        
        if ubGraphicType == None:
            ubGraphicType = 0;
        else:
            ubGraphicType = int(ubGraphicType);
        
        if ubGraphicNum != None and usItemClass != None and int(ubGraphicNum) == int(stiId) and ubGraphicType == graphicType:
            if printAll:
                print("{} is {}({})".format(stiId, szLongItemName, uiIndex));
            result = result + 1;
    #end for child in root:
    return result;
#end def Proc_Items(root, oldId, newId, action, fileName):

#
# Entry point (like Main())
#
itemsXmlTree = ET.parse(ITEMS_XML_PATH);
itemsXmlTreeRoot = itemsXmlTree.getroot();

graphicType = 0;
stiIds = LoadGunsSti(BIG_ITEMS_ROOT);

# now do lookup for usage of each sti
validItemClasses = [ITEM_CLASS_GUN, ITEM_CLASS_BLADE, ITEM_CLASS_THRKNIFE, ITEM_CLASS_LAUNCHER];
for stiId in stiIds:
    matchCnt = LookupStiUsage(itemsXmlTreeRoot, stiId, graphicType, False);
    if matchCnt == 0:
        print("STI {} is not in use".format(stiId));

print("END.");
