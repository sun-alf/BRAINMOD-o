import os, sys;
import xml.etree.ElementTree as ET;

#
# Script setup values
#
TABLE_DATA_ROOT = r'D:\Programs\JaggedAlliance2\Data-BRAINMOD\TableData';
MOVE_ITEMS_IDS_LIST = r'E:\Upload\id_list.txt';


#
# Constants, functions, classes etc
#
class Rule():
    def __init__(self, relativePath, fileName, newFileName, processorFunc):        
        self.relativePath = relativePath;
        self.fileName = fileName;
        self.newFileName = newFileName;
        self.processorFunc = processorFunc;
        self.dirty = False;
        self.xmlTree = None;

    def GetRelativePath(self):
        return os.path.join(self.relativePath, self.fileName);

    def GetFullPath(self):
        return os.path.join(TABLE_DATA_ROOT, self.GetRelativePath());

    def Process(self, itemId, newItemId):
        if self.xmlTree == None:
            self.xmlTree = ET.parse(self.GetFullPath());
        self.dirty = self.dirty or self.processorFunc(self.xmlTree.getroot(), itemId, newItemId);
        
    def Save(self):
        result = self.dirty;
        if self.dirty:
            fullpathNew = os.path.join(self.relativePath, self.newFileName);
            fullpathNew = os.path.join(TABLE_DATA_ROOT, fullpathNew);
            f = open(fullpathNew, "w");
            f.write(r'<?xml version="1.0" encoding="utf-8"?>' + '\n');
            self.xmlTree.write(f, encoding="utf-8", xml_declaration=None, default_namespace=None, method="xml");
            f.close();
            self.dirty = False;  #TODO: starting from this point, should work with newly saved XML data (in self.newFileName)
        return result;
#end class Rule():


def Proc_GunItemChoices(root, oldId, newId):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag.lower().find("bitemno") != -1:
                if tagObj.text == oldId:
                    tagObj.text = newId;
                    result = True;
    #end for child in root:
    return result;
#end def Proc_GunItemChoices(root, oldId, newId):


def Proc_MercStartingGear(root, oldId, newId):
    result = False;
    for mercgear in root:
        for child in mercgear:
            if child.tag == "GEARKIT":
                for tagObj in child:
                    if (tagObj.tag == "mHelmet" or tagObj.tag == "mVest" or tagObj.tag == "mLeg" or tagObj.tag == "mWeapon" or tagObj.tag == "mBig0" or tagObj.tag == "mBig1" or tagObj.tag == "mBig2" or tagObj.tag == "mBig3" or tagObj.tag == "mSmall0" or tagObj.tag == "mSmall1" or tagObj.tag == "mSmall2" or tagObj.tag == "mSmall3" or tagObj.tag == "mSmall4" or tagObj.tag == "mSmall5" or tagObj.tag == "mSmall6" or tagObj.tag == "mSmall7" or tagObj.tag == "lVest" or tagObj.tag == "lLeftThigh" or tagObj.tag == "lRightThigh" or tagObj.tag == "lCPack" or tagObj.tag == "lBPack") and tagObj.text == oldId:
                        tagObj.text = newId;
                        result = True;
    #end for mercgear in root:
    return result;
#end def Proc_MercStartingGear(root, oldId, newId):


def Proc_AttachmentComboMerges(root, oldId, newId):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "usItem" or tagObj.tag.lower().find("usattachment") != -1:
                if tagObj.text == oldId:
                    tagObj.text = newId;
                    result = True;
    #end for child in root:
    return result;
#end def Proc_AttachmentComboMerges(root, oldId, newId):


def Proc_Attachments(root, oldId, newId):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "attachmentIndex" or tagObj.tag == "itemIndex":
                if tagObj.text == oldId:
                    tagObj.text = newId;
                    result = True;
    #end for child in root:
    return result;
#end def Proc_Attachments(root, oldId, newId):


def Proc_CompatibleFaceItems(root, oldId, newId):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "compatiblefaceitemIndex" or tagObj.tag == "itemIndex":
                if tagObj.text == oldId:
                    tagObj.text = newId;
                    result = True;
    #end for child in root:
    return result;
#end def Proc_CompatibleFaceItems(root, oldId, newId):


def Proc_IncompatibleAttachments(root, oldId, newId):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "incompatibleattachmentIndex" or tagObj.tag == "itemIndex":
                if tagObj.text == oldId:
                    tagObj.text = newId;
                    result = True;
    #end for child in root:
    return result;
#end def Proc_IncompatibleAttachments(root, oldId, newId):


def Proc_Item_Transformations(root, oldId, newId):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "usItem" or tagObj.tag.lower().find("usresult") != -1:
                if tagObj.text == oldId:
                    tagObj.text = newId;
                    result = True;
    #end for child in root:
    return result;
#end def Proc_Item_Transformations(root, oldId, newId):


def Proc_Launchables(root, oldId, newId):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "launchableIndex" or tagObj.tag == "itemIndex":
                if tagObj.text == oldId:
                    tagObj.text = newId;
                    result = True;
    #end for child in root:
    return result;
#end def Proc_Launchables(root, oldId, newId):


def Proc_Merges(root, oldId, newId):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "firstItemIndex" or tagObj.tag == "secondItemIndex" or tagObj.tag == "firstResultingItemIndex" or tagObj.tag == "secondResultingItemIndex":
                if tagObj.text == oldId:
                    tagObj.text = newId;
                    result = True;
    #end for child in root:
    return result;
#end def Proc_Merges(root, oldId, newId):


def Proc_StructureConstruct(root, oldId, newId):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "usCreationItem" or tagObj.tag == "usDeconstructItem" or tagObj.tag == "usItemToCreate":
                if tagObj.text == oldId:
                    tagObj.text = newId;
                    result = True;
    #end for child in root:
    return result;
#end def Proc_StructureConstruct(root, oldId, newId):


def Proc_Weapons(root, oldId, newId):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "uiIndex":
                if tagObj.text == oldId:
                    tagObj.text = newId;
                    result = True;
    #end for child in root:
    return result;
#end def Proc_Weapons(root, oldId, newId):


def Proc_NpcInventory(root, oldId, newId):
    result = False;
    for child in root:
        for tagObj in child:
            if tagObj.tag == "sItemIndex":
                if tagObj.text == oldId:
                    tagObj.text = newId;
                    result = True;
    #end for child in root:
    return result;
#end def Proc_NpcInventory(root, oldId, newId):


def Proc_Items(root, oldId, newId):
    def _CorrectPlaceholderName(item):
        for tagObj in item:
            if tagObj.tag == "uiIndex":
                uiIndexObj = tagObj;
            elif tagObj.tag == "szLongItemName":
                szNameObj = tagObj;
        if szNameObj.text.lower() == "placeholder":  # if "wrong" name text, put desired one -- Placeholder XXX.
            szNameObj.text = "Placeholder {0}".format(uiIndexObj.text);

    oldItemIdx = None;
    newItemIdx = None;
    for itemIdx in range(0, len(root)):
        child = root[itemIdx];
        for tagObj in child:
            if tagObj.tag == "uiIndex":
                if tagObj.text == oldId:
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
    return True;
#end def Proc_Items(root, oldId, newId):


g_rules = [
    Rule("Inventory", "EnemyGunChoices.xml", "NEW_EnemyGunChoices.xml", Proc_GunItemChoices),
    Rule("Inventory", "EnemyItemChoices.xml", "NEW_EnemyItemChoices.xml", Proc_GunItemChoices),
    Rule("Inventory", "GunChoices_Enemy_Admin.xml", "NEW_GunChoices_Enemy_Admin.xml", Proc_GunItemChoices),
    Rule("Inventory", "GunChoices_Enemy_Elite.xml", "NEW_GunChoices_Enemy_Elite.xml", Proc_GunItemChoices),
    Rule("Inventory", "GunChoices_Enemy_Regular.xml", "NEW_GunChoices_Enemy_Regular.xml", Proc_GunItemChoices),
    Rule("Inventory", "GunChoices_Militia_Elite.xml", "NEW_GunChoices_Militia_Elite.xml", Proc_GunItemChoices),
    Rule("Inventory", "GunChoices_Militia_Green.xml", "NEW_GunChoices_Militia_Green.xml", Proc_GunItemChoices),
    Rule("Inventory", "GunChoices_Militia_Regular.xml", "NEW_GunChoices_Militia_Regular.xml", Proc_GunItemChoices),
    Rule("Inventory", "IMPItemChoices.xml", "NEW_IMPItemChoices.xml", Proc_GunItemChoices),
    Rule("Inventory", "ItemChoices_Enemy_Admin.xml", "NEW_ItemChoices_Enemy_Admin.xml", Proc_GunItemChoices),
    Rule("Inventory", "ItemChoices_Enemy_Elite.xml", "NEW_ItemChoices_Enemy_Elite.xml", Proc_GunItemChoices),
    Rule("Inventory", "ItemChoices_Enemy_Regular.xml", "NEW_ItemChoices_Enemy_Regular.xml", Proc_GunItemChoices),
    Rule("Inventory", "ItemChoices_Militia_Elite.xml", "NEW_ItemChoices_Militia_Elite.xml", Proc_GunItemChoices),
    Rule("Inventory", "ItemChoices_Militia_Green.xml", "NEW_ItemChoices_Militia_Green.xml", Proc_GunItemChoices),
    Rule("Inventory", "ItemChoices_Militia_Regular.xml", "NEW_ItemChoices_Militia_Regular.xml", Proc_GunItemChoices),
    Rule("Inventory", "MercStartingGear.xml", "NEW_MercStartingGear.xml", Proc_MercStartingGear),
    
    Rule("Items", "AttachmentComboMerges.xml", "NEW_AttachmentComboMerges.xml", Proc_AttachmentComboMerges),
    Rule("Items", "AttachmentInfo.xml", "NEW_AttachmentInfo.xml", Proc_AttachmentComboMerges),
    Rule("Items", "Attachments.xml", "NEW_Attachments.xml", Proc_Attachments),
    Rule("Items", "CompatibleFaceItems.xml", "NEW_CompatibleFaceItems.xml", Proc_CompatibleFaceItems),
    Rule("Items", "IncompatibleAttachments.xml", "NEW_IncompatibleAttachments.xml", Proc_IncompatibleAttachments),
    Rule("Items", "IncompatibleAttachments_2.xml", "NEW_IncompatibleAttachments_2.xml", Proc_IncompatibleAttachments),
    Rule("Items", "Item_Transformations.xml", "NEW_Item_Transformations.xml", Proc_Item_Transformations),
    Rule("Items", "Items.xml", "NEW_Items.xml", Proc_Items),
    Rule("Items", "Launchables.xml", "NEW_Launchables.xml", Proc_Launchables),
    Rule("Items", "Merges.xml", "NEW_Merges.xml", Proc_Merges),
    Rule("Items", "StructureConstruct.xml", "NEW_StructureConstruct.xml", Proc_StructureConstruct),
    Rule("Items", "StructureDeconstruct.xml", "NEW_StructureDeconstruct.xml", Proc_StructureConstruct),
    Rule("Items", "Weapons.xml", "NEW_Weapons.xml", Proc_Weapons),
    
    Rule("NPCInventory", "AlbertoInventory.xml","NEW_AlbertoInventory.xml", Proc_NpcInventory),
    Rule("NPCInventory", "ArnieInventory.xml",  "NEW_ArnieInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "CarloInventory.xml",  "NEW_CarloInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "DevinInventory.xml",  "NEW_DevinInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "ElginInventory.xml",  "NEW_ElginInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "FrankInventory.xml",  "NEW_FrankInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "FranzInventory.xml",  "NEW_FranzInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "FredoInventory.xml",  "NEW_FredoInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "GabbyInventory.xml",  "NEW_GabbyInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "HerveInventory.xml",  "NEW_HerveInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "HowardInventory.xml", "NEW_HowardInventory.xml",  Proc_NpcInventory),
    Rule("NPCInventory", "JakeInventory.xml",   "NEW_JakeInventory.xml",    Proc_NpcInventory),
    Rule("NPCInventory", "KeithInventory.xml",  "NEW_KeithInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "MannyInventory.xml",  "NEW_MannyInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "MickeyInventory.xml", "NEW_MickeyInventory.xml",  Proc_NpcInventory),
    Rule("NPCInventory", "PerkoInventory.xml",  "NEW_PerkoInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "PeterInventory.xml",  "NEW_PeterInventory.xml",   Proc_NpcInventory),
    Rule("NPCInventory", "SamInventory.xml",    "NEW_SamInventory.xml",     Proc_NpcInventory),
    Rule("NPCInventory", "TinaInventory.xml",   "NEW_TinaInventory.xml",    Proc_NpcInventory),
    Rule("NPCInventory", "TonyInventory.xml",   "NEW_TonyInventory.xml",    Proc_NpcInventory)
];


class RulesManager():
    IDX_OLD = 0;
    IDX_NEW = 1;
    _rules = g_rules;
    _moveItemIdList = [];

    @classmethod
    def ProcessAll(cls):
        print("Process Move item IDs:");
        for item in cls._moveItemIdList:
            for rule in cls._rules:
                rule.Process(item[cls.IDX_OLD], item[cls.IDX_NEW]);
                print("    {0} -> {1}".format(item[cls.IDX_OLD], item[cls.IDX_NEW]));
        print("");
                
        print("Changed files:");
        for rule in cls._rules:
            if rule.Save():
                print("   {0}".format(rule.GetRelativePath()));
    #end def ProcessAll(cls):

    @classmethod
    def MoveItemId(cls, oldId, newId):
        cls._moveItemIdList.append([oldId, newId]);
#end class RulesManager():


def MoveItemsIds(idListFullPath):
    idListFile = open(idListFullPath, "r");
    idLines = idListFile.readlines();
    idListFile.close();
    
    for line in idLines:
        ids = line.split(" -> ");
        if len(ids) == 2:
            oldIdInt = int(ids[0]);  # convert to int and back to str in order to drop any special characters, i.e. '\n' etc
            newIdInt = int(ids[1]);
            RulesManager.MoveItemId(str(oldIdInt), str(newIdInt));
        else:
            raise Exception("Bad line on input", line);
    
    RulesManager.ProcessAll();
#end def MoveItemsIds(idListFullPath):


#
# Entry point (like Main())
#
MoveItemsIds(MOVE_ITEMS_IDS_LIST);

