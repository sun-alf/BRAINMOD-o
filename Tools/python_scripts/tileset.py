import xml.etree.ElementTree as ET;

#
# Script setup values
#
TARGET_TILESET_XML = r'D:\Programs\JaggedAlliance2\Data-BRAINMOD\Ja2Set.dat.xml';
REFERENCE_TILESET_XML = r'D:\Programs\JaggedAlliance2\Data-1.13\Ja2Set.dat.xml';


#
# Constants, functions, classes etc
#
class Tileset():
    _generic = None;

    def __init__(self, slotCnt):        
        self.slots = [None] * slotCnt;
        self.index = -1;
        self.name = None;
        self.uniqueList = None;

    def PrintSlots(self):
        for i in range (0, len(self.slots)):
            print("[{0}]: {1}".format(i, self.slots[i]));

    def LoadXmlElement(self, xmlTileset):
        def _CopyGenericSlots(self):
            for i in range (0, len(self.slots)):
                self.slots[i] = Tileset._generic.slots[i];
        #end def _CopyGenericSlots(self):
    
        self.index = int(xmlTileset.attrib["index"]);
        self.name = xmlTileset[0].text;

        if self.index == 0:
            if Tileset._generic == None:
                Tileset._generic = self;
            else:
                raise Exception("Tileset index=\"0\" is not unique!");
        else:
            _CopyGenericSlots(self);
        
        for el in xmlTileset[2]:  # in <Files>
            self.slots[int(el.attrib["index"])] = el.text;
        
        if self.index == 0:
            self.uniqueList = [];
            for slot in self.slots:
                if not slot in self.uniqueList:
                    self.uniqueList.append(slot);
        #else:
        #    self.Check_GenericFiles_IsFullSet();
    #end def LoadXmlElement(self, xmlTileset):

    def GetMissingGenericFiles(self, genericTileset):
        missingFiles = [];
        for uniq in genericTileset.uniqueList:
            if not uniq in self.slots:
                missingFiles.append(uniq);
        return missingFiles;

    def PrintDuplicateSlots(self):
        print("Tileset[{0}] ({1}) duplicated files:".format(self.index, self.name));
        duplicatesList = [];
        for slot in self.slots:
            if slot in duplicatesList:
                continue;
            firstEntry = None;
            for i in range (0, len(self.slots)):
                if slot == self.slots[i]:
                    if firstEntry == None:
                        firstEntry = i;
                    else:  # a duplicate is found
                        print("    [{0}] {1}  (dupl. of [{2}])".format(i, self.slots[i], firstEntry));
                        duplicatesList.append(slot);
    #end def PrintDuplicateSlots(self):

#end class Rule():


def LoadXmlTilesets(fPath):
    tree = ET.parse(fPath);
    root = tree.getroot();
    
    xmlTilesets = root[0];
    if xmlTilesets.tag != "tilesets":
        raise Exception("Missing <tilesets> element.");
    
    numTilesets = int(xmlTilesets.attrib["numTilesets"]);
    numFiles = int(xmlTilesets.attrib["numFiles"]);
    tilesets = [None] * numTilesets;
    
    for xmlTileset in xmlTilesets:
        tileset = Tileset(numFiles);
        tileset.LoadXmlElement(xmlTileset);
        tilesets[tileset.index] = tileset;
    
    Tileset._generic = None;
    return tilesets;
#end def LoadTilesetsXML(fPath):


def CheckTilesetsIntegrity(refXmlPath, workXmlPath):
    def _CompareLists(refList, workList):
        result = [];  # list of extra missing generic files in a working tileset
        for el in workList:
            if not el in refList:
                result.append(el);
        return result;
    #end def _CompareLists(l1, l2):
    
    refTilesets = LoadXmlTilesets(refXmlPath);
    workTilesets = LoadXmlTilesets(workXmlPath);
    
    # enlist all "free" file slots in generic tileset
    workTilesets[0].PrintDuplicateSlots();
    
    for i in range(1, len(refTilesets)):
        extraMiss = _CompareLists(refTilesets[i].GetMissingGenericFiles(refTilesets[0]), workTilesets[i].GetMissingGenericFiles(workTilesets[0]));
        if len(extraMiss) > 0:
            print("Tileset[{0}] ({1}) lacks of generic files:".format(workTilesets[i].index, workTilesets[i].name));
            for mf in extraMiss:
                print("    " + mf);
#end def CheckTilesetsIntegrity(refXmlPath, workXmlPath):


#
# Entry point (like Main())
#
CheckTilesetsIntegrity(REFERENCE_TILESET_XML, TARGET_TILESET_XML);
