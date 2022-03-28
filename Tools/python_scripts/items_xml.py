#### USAGE ####
# 0. Ensure you have !!! Python 3 !!! installed (version 3.x -- does not matter).
# 1. Create a text file with specified name under specified path, see MOVE_ITEMS_IDS_LIST.
# 2. Type desired commands, one command per one line; save file. See available commands and syntax in the next section.
# 3. Run this script (i.e. "items_xml.py") in a cmd line window.
#
# Available commands with syntax/examples (use without quotes):
# + Comment line: "// any text"
# + What is item: "? item_id"
#   Print long name of the item only.
# + Look-up item: "* item_id"
#   Print all places where the item is referenced.
# + Move item: "old_item_id -> new_item_id"
#   Basically does swapping of given item ids. If new_item_id holds a placeholder, it will go onto old_item_id place.
# + Delete item: "x item_id"
#   In Items.xml, it will replace the whole specified item entry by a placeholder.
#   In other *.xml, it will delete all elements what use this item_id. Once again, not tags with that item_id, but the whole
#   elements if it is sematically need.


import os, sys;
import xml.etree.ElementTree as ET;

#
# Script setup values
#
SWDIR = os.getcwd();
TABLE_DATA_ROOT = r'{}\..\..\Data-BRAINMOD\TableData'.format(SWDIR);
MOVE_ITEMS_IDS_LIST = r'C:\Temp\lookup.txt';


#
# Constants, functions, classes etc
#
class Actions():
    LOOKUP = 0;
    MOVE = 1;
    WHATIS = 2;
#end class Actions():


class Rule():
    def __init__(self, relativePath, fileName, newRelativePath, newFileName, processorFunc):        
        self.relativePath = relativePath;
        self.fileName = fileName;
        self.newRelativePath = newRelativePath;
        self.newFileName = newFileName;
        self.processorFunc = processorFunc;
        self.dirty = False;
        self.xmlTree = None;

    def GetRelativePath(self):
        return os.path.join(self.relativePath, self.fileName);

    def GetFullPath(self):
        return os.path.join(TABLE_DATA_ROOT, self.GetRelativePath());

    def Process(self, itemId, newItemId, action):
        if self.xmlTree == None:
            self.xmlTree = ET.parse(self.GetFullPath());
        self.dirty = self.processorFunc(self.xmlTree.getroot(), itemId, newItemId, action, self.fileName) or self.dirty;
        
    def Save(self):
        result = self.dirty;
        if self.dirty:
            fullpathNew = os.path.join(self.relativePath, self.newRelativePath);
            if self.newRelativePath != None and self.newRelativePath != "":
                newDirPath = os.path.join(TABLE_DATA_ROOT, fullpathNew);
                if not os.path.exists(newDirPath):
                    os.makedirs(newDirPath);
            
            fullpathNew = os.path.join(fullpathNew, self.newFileName);
            fullpathNew = os.path.join(TABLE_DATA_ROOT, fullpathNew);
            f = open(fullpathNew, "wb");
            f.write(bytearray(r'<?xml version="1.0" encoding="utf-8"?>' + '\n', "utf-8"));
            self.xmlTree.write(f, encoding="utf-8", xml_declaration=None, default_namespace=None, method="xml");
            f.close();
            self.dirty = False;  #TODO: starting from this point, should work with newly saved XML data (in self.newFileName)
        return result;
#end class Rule():


def Proc_GunItemChoices(root, oldId, newId, action, fileName):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag.lower().find("bitemno") != -1:
                if tagObj.text == oldId:
                    if action == Actions.LOOKUP:
                        print("{2}: <{0}>{1}</{0}>".format(tagObj.tag, oldId, fileName));
                    else:
                        tagObj.text = newId;
                        result = True;
    #end for child in root:
    return result;
#end def Proc_GunItemChoices(root, oldId, newId, action, fileName):


def Proc_MercStartingGear(root, oldId, newId, action, fileName):
    result = False;
    for mercgear in root:
        for child in mercgear:
            if child.tag == "GEARKIT":
                for tagObj in child:
                    if (tagObj.tag == "mHelmet" or tagObj.tag == "mVest" or tagObj.tag == "mLeg" or tagObj.tag == "mWeapon" or tagObj.tag == "mBig0" or tagObj.tag == "mBig1" or tagObj.tag == "mBig2" or tagObj.tag == "mBig3" or tagObj.tag == "mSmall0" or tagObj.tag == "mSmall1" or tagObj.tag == "mSmall2" or tagObj.tag == "mSmall3" or tagObj.tag == "mSmall4" or tagObj.tag == "mSmall5" or tagObj.tag == "mSmall6" or tagObj.tag == "mSmall7" or tagObj.tag == "lVest" or tagObj.tag == "lLeftThigh" or tagObj.tag == "lRightThigh" or tagObj.tag == "lCPack" or tagObj.tag == "lBPack") and tagObj.text == oldId:
                        if action == Actions.LOOKUP:
                            print("{2}: <{0}>{1}</{0}>".format(tagObj.tag, oldId, fileName));
                        else:
                            tagObj.text = newId;
                            result = True;
    #end for mercgear in root:
    return result;
#end def Proc_MercStartingGear(root, oldId, newId, action, fileName):


def Proc_AttachmentComboMerges(root, oldId, newId, action, fileName):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "usItem" or tagObj.tag.lower().find("usattachment") != -1:
                if tagObj.text == oldId:
                    if action == Actions.LOOKUP:
                        print("{2}: <{0}>{1}</{0}>".format(tagObj.tag, oldId, fileName));
                    else:
                        tagObj.text = newId;
                        result = True;
    #end for child in root:
    return result;
#end def Proc_AttachmentComboMerges(root, oldId, newId, action, fileName):


def Proc_Attachments(root, oldId, newId, action, fileName):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "attachmentIndex" or tagObj.tag == "itemIndex":
                if tagObj.text == oldId:
                    if action == Actions.LOOKUP:
                        print("{2}: <{0}>{1}</{0}>".format(tagObj.tag, oldId, fileName));
                    else:
                        tagObj.text = newId;
                        result = True;
    #end for child in root:
    return result;
#end def Proc_Attachments(root, oldId, newId, action, fileName):


def Proc_CompatibleFaceItems(root, oldId, newId, action, fileName):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "compatiblefaceitemIndex" or tagObj.tag == "itemIndex":
                if tagObj.text == oldId:
                    if action == Actions.LOOKUP:
                        print("{2}: <{0}>{1}</{0}>".format(tagObj.tag, oldId, fileName));
                    else:
                        tagObj.text = newId;
                        result = True;
    #end for child in root:
    return result;
#end def Proc_CompatibleFaceItems(root, oldId, newId, action, fileName):


def Proc_IncompatibleAttachments(root, oldId, newId, action, fileName):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "incompatibleattachmentIndex" or tagObj.tag == "itemIndex":
                if tagObj.text == oldId:
                    if action == Actions.LOOKUP:
                        print("{2}: <{0}>{1}</{0}>".format(tagObj.tag, oldId, fileName));
                    else:
                        tagObj.text = newId;
                        result = True;
    #end for child in root:
    return result;
#end def Proc_IncompatibleAttachments(root, oldId, newId, action, fileName):


def Proc_Item_Transformations(root, oldId, newId, action, fileName):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "usItem" or tagObj.tag.lower().find("usresult") != -1:
                if tagObj.text == oldId:
                    if action == Actions.LOOKUP:
                        print("{2}: <{0}>{1}</{0}>".format(tagObj.tag, oldId, fileName));
                    else:
                        tagObj.text = newId;
                        result = True;
    #end for child in root:
    return result;
#end def Proc_Item_Transformations(root, oldId, newId, action, fileName):


def Proc_Launchables(root, oldId, newId, action, fileName):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "launchableIndex" or tagObj.tag == "itemIndex":
                if tagObj.text == oldId:
                    if action == Actions.LOOKUP:
                        print("{2}: <{0}>{1}</{0}>".format(tagObj.tag, oldId, fileName));
                    else:
                        tagObj.text = newId;
                        result = True;
    #end for child in root:
    return result;
#end def Proc_Launchables(root, oldId, newId, action, fileName):


def Proc_Merges(root, oldId, newId, action, fileName):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "firstItemIndex" or tagObj.tag == "secondItemIndex" or tagObj.tag == "firstResultingItemIndex" or tagObj.tag == "secondResultingItemIndex":
                if tagObj.text == oldId:
                    if action == Actions.LOOKUP:
                        print("{2}: <{0}>{1}</{0}>".format(tagObj.tag, oldId, fileName));
                    else:
                        tagObj.text = newId;
                        result = True;
    #end for child in root:
    return result;
#end def Proc_Merges(root, oldId, newId, action, fileName):


def Proc_StructureConstruct(root, oldId, newId, action, fileName):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "usCreationItem" or tagObj.tag == "usDeconstructItem" or tagObj.tag == "usItemToCreate":
                if tagObj.text == oldId:
                    if action == Actions.LOOKUP:
                        print("{2}: <{0}>{1}</{0}>".format(tagObj.tag, oldId, fileName));
                    else:
                        tagObj.text = newId;
                        result = True;
    #end for child in root:
    return result;
#end def Proc_StructureConstruct(root, oldId, newId, action, fileName):


def Proc_Weapons(root, oldId, newId, action, fileName):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "uiIndex":
                if tagObj.text == oldId:
                    if action == Actions.LOOKUP:
                        print("{2}: <{0}>{1}</{0}>".format(tagObj.tag, oldId, fileName));
                    else:
                        tagObj.text = newId;
                        result = True;
    #end for child in root:
    return result;
#end def Proc_Weapons(root, oldId, newId, action, fileName):


def Proc_NpcInventory(root, oldId, newId, action, fileName):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "sItemIndex":
                if tagObj.text == oldId:
                    if action == Actions.LOOKUP:
                        print("{2}: <{0}>{1}</{0}>".format(tagObj.tag, oldId, fileName));
                    else:
                        tagObj.text = newId;
                        result = True;
    #end for child in root:
    return result;
#end def Proc_NpcInventory(root, oldId, newId, action, fileName):


g_Proc_Items_return = None;
def Proc_Items(root, oldId, newId, action, fileName):
    def _CorrectPlaceholderName(item):
        for tagObj in item:
            if tagObj.tag == "uiIndex":
                uiIndexObj = tagObj;
            elif tagObj.tag == "szLongItemName":
                szNameObj = tagObj;
        if szNameObj.text.lower().find("placeholder") != -1:  # if it's a Placeholder -- put "Placeholder XXX" as item name.
            szNameObj.text = "Placeholder {0}".format(uiIndexObj.text);
    #end def _CorrectPlaceholderName(item):

    def _GetTagValue(item, tagName):
        for tagObj in item:
            if tagObj.tag == tagName:
                return tagObj.text;
        return None;
    #end def _GetTagValue(item):

    def _GetLongName(item):
        return _GetTagValue(item, "szLongItemName");
    #end def _GetLongName(item):

    def _GetDescription(item):
        return _GetTagValue(item, "szItemDesc");
    #end def _GetDescription(item):

    global g_Proc_Items_return;
    g_Proc_Items_return = None;

    oldItemIdx = None;
    newItemIdx = None;
    for itemIdx in range(0, len(root)):
        child = root[itemIdx];
        saveTagObj = None;
        for tagObj in child:
            if tagObj.tag == "uiIndex":
                if tagObj.text == oldId:
                    if action == Actions.LOOKUP:
                        print("{2}: <{0}>{1}</{0}>".format(tagObj.tag, oldId, fileName));
                        return False;  # skip all other manipulations as we need only print a match of this ID
                    elif action == Actions.WHATIS:
                        g_Proc_Items_return = "{}  [{}]".format(_GetLongName(child), _GetDescription(child));
                        return False;  # skip all other manipulations as we need name of the item
                    else:
                        tagObj.text = newId;
                        oldItemIdx = itemIdx;
                elif tagObj.text == newId:
                    tagObj.text = oldId;
                    newItemIdx = itemIdx;
                break;
        if oldItemIdx != None and newItemIdx != None:  # if both items found, swap them and exit
            temp = root[oldItemIdx];
            root[oldItemIdx] = root[newItemIdx];
            root[newItemIdx] = temp;
            _CorrectPlaceholderName(root[oldItemIdx]);
            _CorrectPlaceholderName(root[newItemIdx]);
            break;
    #end for child in root:
    
    if oldItemIdx == None or newItemIdx == None:
        raise Exception("New or old item ID is not found in Items.xml ({0} -> {1})".format(oldId, newId));
    
    if oldItemIdx != None and newItemIdx != None and action == Actions.MOVE:
        return True;
    else:
        return False;
#end def Proc_Items(root, oldId, newId, action, fileName):


g_rules = [
    Rule("Inventory", "EnemyGunChoices.xml", "NEW", "EnemyGunChoices.xml", Proc_GunItemChoices),
    Rule("Inventory", "EnemyItemChoices.xml", "NEW", "EnemyItemChoices.xml", Proc_GunItemChoices),
    Rule("Inventory", "GunChoices_Enemy_Admin.xml", "NEW", "GunChoices_Enemy_Admin.xml", Proc_GunItemChoices),
    Rule("Inventory", "GunChoices_Enemy_Elite.xml", "NEW", "GunChoices_Enemy_Elite.xml", Proc_GunItemChoices),
    Rule("Inventory", "GunChoices_Enemy_Regular.xml", "NEW", "GunChoices_Enemy_Regular.xml", Proc_GunItemChoices),
    Rule("Inventory", "GunChoices_Militia_Elite.xml", "NEW", "GunChoices_Militia_Elite.xml", Proc_GunItemChoices),
    Rule("Inventory", "GunChoices_Militia_Green.xml", "NEW", "GunChoices_Militia_Green.xml", Proc_GunItemChoices),
    Rule("Inventory", "GunChoices_Militia_Regular.xml", "NEW", "GunChoices_Militia_Regular.xml", Proc_GunItemChoices),
    Rule("Inventory", "IMPItemChoices.xml", "NEW", "IMPItemChoices.xml", Proc_GunItemChoices),
    Rule("Inventory", "ItemChoices_Enemy_Admin.xml", "NEW", "ItemChoices_Enemy_Admin.xml", Proc_GunItemChoices),
    Rule("Inventory", "ItemChoices_Enemy_Elite.xml", "NEW", "ItemChoices_Enemy_Elite.xml", Proc_GunItemChoices),
    Rule("Inventory", "ItemChoices_Enemy_Regular.xml", "NEW", "ItemChoices_Enemy_Regular.xml", Proc_GunItemChoices),
    Rule("Inventory", "ItemChoices_Militia_Elite.xml", "NEW", "ItemChoices_Militia_Elite.xml", Proc_GunItemChoices),
    Rule("Inventory", "ItemChoices_Militia_Green.xml", "NEW", "ItemChoices_Militia_Green.xml", Proc_GunItemChoices),
    Rule("Inventory", "ItemChoices_Militia_Regular.xml", "NEW", "ItemChoices_Militia_Regular.xml", Proc_GunItemChoices),
    Rule("Inventory", "MercStartingGear.xml", "NEW", "MercStartingGear.xml", Proc_MercStartingGear),
    
    Rule("Items", "AttachmentComboMerges.xml", "NEW", "AttachmentComboMerges.xml", Proc_AttachmentComboMerges),
    Rule("Items", "AttachmentInfo.xml", "NEW", "AttachmentInfo.xml", Proc_AttachmentComboMerges),
    Rule("Items", "Attachments.xml", "NEW", "Attachments.xml", Proc_Attachments),
    Rule("Items", "CompatibleFaceItems.xml", "NEW", "CompatibleFaceItems.xml", Proc_CompatibleFaceItems),
    Rule("Items", "IncompatibleAttachments.xml", "NEW", "IncompatibleAttachments.xml", Proc_IncompatibleAttachments),
    Rule("Items", "IncompatibleAttachments_2.xml", "NEW", "IncompatibleAttachments_2.xml", Proc_IncompatibleAttachments),
    Rule("Items", "Item_Transformations.xml", "NEW", "Item_Transformations.xml", Proc_Item_Transformations),
    Rule("Items", "Items.xml", "NEW", "Items.xml", Proc_Items),
    Rule("Items", "Launchables.xml", "NEW", "Launchables.xml", Proc_Launchables),
    Rule("Items", "Merges.xml", "NEW", "Merges.xml", Proc_Merges),
    Rule("Items", "StructureConstruct.xml", "NEW", "StructureConstruct.xml", Proc_StructureConstruct),
    Rule("Items", "StructureDeconstruct.xml", "NEW", "StructureDeconstruct.xml", Proc_StructureConstruct),
    Rule("Items", "Weapons.xml", "NEW", "Weapons.xml", Proc_Weapons),
    
    Rule("NPCInventory", "AlbertoInventory.xml","NEW", "AlbertoInventory.xml", Proc_NpcInventory),
    Rule("NPCInventory", "ArnieInventory.xml",  "NEW", "ArnieInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "CarloInventory.xml",  "NEW", "CarloInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "DevinInventory.xml",  "NEW", "DevinInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "ElginInventory.xml",  "NEW", "ElginInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "FrankInventory.xml",  "NEW", "FrankInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "FranzInventory.xml",  "NEW", "FranzInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "FredoInventory.xml",  "NEW", "FredoInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "GabbyInventory.xml",  "NEW", "GabbyInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "HerveInventory.xml",  "NEW", "HerveInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "HowardInventory.xml", "NEW", "HowardInventory.xml",  Proc_NpcInventory),
    Rule("NPCInventory", "JakeInventory.xml",   "NEW", "JakeInventory.xml",    Proc_NpcInventory),
    Rule("NPCInventory", "KeithInventory.xml",  "NEW", "KeithInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "MannyInventory.xml",  "NEW", "MannyInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "MickeyInventory.xml", "NEW", "MickeyInventory.xml",  Proc_NpcInventory),
    Rule("NPCInventory", "PerkoInventory.xml",  "NEW", "PerkoInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "PeterInventory.xml",  "NEW", "PeterInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "SamInventory.xml",    "NEW", "SamInventory.xml",     Proc_NpcInventory),
    Rule("NPCInventory", "TinaInventory.xml",   "NEW", "TinaInventory.xml",    Proc_NpcInventory),
    Rule("NPCInventory", "TonyInventory.xml",   "NEW", "TonyInventory.xml",    Proc_NpcInventory)
];
for i in range(1, 61):
    xmlFileName = "AdditionalDealer_{}_Inventory.xml".format(i);
    g_rules.append(Rule("NPCInventory", xmlFileName, "NEW", xmlFileName, Proc_NpcInventory));



class RulesManager():
    IDX_OLD = 0;
    IDX_NEW = 1;
    _rules = g_rules;
    _moveItemIdList = [];
    _lookupIdList = [];
    _whatisIdList = [];

    @classmethod
    def GetRule(cls, fileName, processorFunc):
        for rule in cls._rules:
            if rule.fileName == fileName and rule.processorFunc == processorFunc:
                return rule;
        return None;
    #end def GetRule(fileName, processorFunc):

    @classmethod
    def ProcessAll(cls):
        print("Process WhatIs item IDs:");
        rule = RulesManager.GetRule("Items.xml", Proc_Items);
        for item in cls._whatisIdList:
            rule.Process(item, 0, Actions.WHATIS);
            if g_Proc_Items_return.lower().find("placeholder") == -1:  # if there is no word "placeholder" then print
                print("    ? {0} is: {1}".format(item, g_Proc_Items_return));
        print("");

        print("Process Lookup item IDs:");
        for item in cls._lookupIdList:
            print("    * {0} mentioned in:".format(item));
            for rule in cls._rules:
                rule.Process(item, 0, Actions.LOOKUP);
        print("");

        print("Process Move item IDs:");
        for item in cls._moveItemIdList:
            for rule in cls._rules:
                rule.Process(item[cls.IDX_OLD], item[cls.IDX_NEW], Actions.MOVE);
            print("    {0} -> {1} done".format(item[cls.IDX_OLD], item[cls.IDX_NEW]));
        print("");

        print("Changed files:");
        for rule in cls._rules:
            if rule.Save():
                print("   {0}".format(rule.GetRelativePath()));
    #end def ProcessAll(cls):

    @classmethod
    def MoveItemId(cls, oldId, newId):
        cls._moveItemIdList.append([oldId, newId]);

    @classmethod
    def LookupItemId(cls, oldId):
        cls._lookupIdList.append(oldId);

    @classmethod
    def WhatisItemId(cls, oldId):
        cls._whatisIdList.append(oldId);
#end class RulesManager():


def ProcessItemsIds(idListFullPath):
    def _GetRangeIfAny(text):
        result = None;
        if text.find("..") != -1:
            nums = text.split("..");
            if len(nums) == 2:
                a = int(nums[0]);
                b = int(nums[1]);
                result = [a, b];
        else:  # one number is given
            a = int(text);
            result = [a, a];
        return result;
    #end def _GetRangeIfAny(text):
    
    idListFile = open(idListFullPath, "r");
    idLines = idListFile.readlines();
    idListFile.close();
    
    for line in idLines:
        if line.find("//") == 0:  # starts with "//" -- a comment
            pass;  # skip commented line

        elif line.find('x') != -1:
            #TODO: delete item
            pass;

        elif line.find('?') != -1:
            ids = line.split("? ");
            if len(ids) == 2:
                idsInt = _GetRangeIfAny(ids[1]);  # convert to int and back to str in order to drop any special characters, i.e. '\n' etc
                if idsInt != None:
                    for i in range(idsInt[0], idsInt[1] + 1): 
                        RulesManager.WhatisItemId(str(i));
                else:
                    raise Exception("Bad line on input", line);
            else:
                raise Exception("Bad line on input", line);

        elif line.find('*') != -1:
            ids = line.split("* ");
            if len(ids) == 2:
                idsInt = _GetRangeIfAny(ids[1]);  # convert to int and back to str in order to drop any special characters, i.e. '\n' etc
                if idsInt != None:
                    for i in range(idsInt[0], idsInt[1] + 1): 
                        RulesManager.LookupItemId(str(i));
                else:
                    raise Exception("Bad line on input", line);
            else:
                raise Exception("Bad line on input", line);

        elif line.find("->") != -1:
            ids = line.split(" -> ");
            if len(ids) == 2:
                oldIdInt = int(ids[0]);  # convert to int and back to str in order to drop any special characters, i.e. '\n' etc
                newIdInt = int(ids[1]);
                RulesManager.MoveItemId(str(oldIdInt), str(newIdInt));
            else:
                raise Exception("Bad line on input", line);

        elif line.find(">>") != -1:
            #TODO: move item with overriding (delete target/new ID if exists)
            pass;

        elif len(line.strip()) == 0:
            pass;  # skip empty line

        else:
            raise Exception("Bad line (unknown command) on input", line);
    
    RulesManager.ProcessAll();
#end def ProcessItemsIds(idListFullPath):


#
# Entry point (like Main())
#
ProcessItemsIds(MOVE_ITEMS_IDS_LIST);

