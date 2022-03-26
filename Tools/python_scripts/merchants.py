import os, sys;
import xml.etree.ElementTree as ET;
import random;


#
# Script setup values
#
REF_TABLE_DATA_ROOT = r'D:\Programs\JaggedAlliance2\Data-1.13\TableData';
TARGET_TABLE_DATA_ROOT = r'D:\Programs\JaggedAlliance2\Data-BRAINMOD\TableData';

TARGET_RND_ID_RANGE = (range(161, 221), range(243, 270), range(292, 324), range(350, 389));


#
# Constants, functions, classes etc
#
class Item():
    def __init__(self, xml_member):
        self.xml = xml_member;
    
    @classmethod
    def Spawn(cls, elementName):
        return Item(ET.Element(elementName));

    def Get(self, propName):
        result = self.xml.find(propName);
        if result == None:
            result = "0";
        else:
            result = result.text;
        return result;

    def Set(self, propName, value):
        prop = self.xml.find(propName);
        if prop != None:
            prop.text = value;
        else:
            newProp = ET.Element(propName);
            newProp.text = value;
            self.xml.append(newProp);

    def Has(self, propName):
        result = self.xml.find(propName);
        if result == None:
            return False;
        else:
            return True;
#end class Item():


class ItemListElement():
    def __init__(self, name, longName, item):
        self.name = name;
        self.longName = longName;
        self.price = int(item.Get("usPrice"));
        if item.Get("NotBuyable") == "1":
            self.notByable = True;
        else:
            self.notByable = False;
    
    def ForSell(self):
        if int(self.price) > 0 and self.notByable == False:
            return True;
        else:
            return False;
#end class ItemListElement():


def _ListFromItemsXml(rootDir):
    path_tgtItemsXml = open(os.path.join(rootDir, r"Items\Items.xml"), "r");
    tree_tgtItemsXml = ET.parse(path_tgtItemsXml);
    root_tgtItemsXml = tree_tgtItemsXml.getroot();
    
    result = [];
    for xmlItem in root_tgtItemsXml:
        item = Item(xmlItem);
        itemName = item.Get("szItemName");
        itemLName = item.Get("szLongItemName");
        if int(item.Get("uiIndex")) == 0 or itemName.lower().find("placeholder") != -1 or itemLName.lower().find("placeholder") != -1:
            result.append(None);
        else:
            result.append(ItemListElement(itemName, itemLName, item));
    return result;
#end def _ListFromItemsXml(rootDir):


def _ValidateInventory(root, refItemsList, tgtItemsList):
    def __FindItem(name, itemList):
        for i in range(0, len(itemList)):
            if itemList[i] != None:
                if itemList[i].name.lower().find(name.lower()) != -1 and itemList[i].ForSell() == True:
                    return i;
        return -1;
    
    result = 0;
    for xmlInv in root:
        inv = Item(xmlInv);
        itemIdx = int(inv.Get("sItemIndex"));
        itemCnt = int(inv.Get("ubOptimalNumber"));
        if itemIdx != 0 and itemCnt > 0:
            result = result + 1;
            if refItemsList[itemIdx] == None:
                print("    !! Ref item {0} is placeholder".format(itemIdx));
                continue;
            if tgtItemsList[itemIdx] == None:
                newItemIdx = __FindItem(refItemsList[itemIdx].name, tgtItemsList);
                if newItemIdx != -1:
                    inv.Set("sItemIndex", str(newItemIdx));
                    print("    New target item {0} ({1}), pl. Was: {2} ({3})".format(newItemIdx, tgtItemsList[newItemIdx].name, itemIdx, refItemsList[itemIdx].name));
                else:
                    print("    !! Ref item {0} ({1}) is a placeholder in target; not found replacement.".format(itemIdx, refItemsList[itemIdx].name));
                continue;
            if tgtItemsList[itemIdx].name.lower().find(refItemsList[itemIdx].name.lower()) == -1:  # ref and tgt items do not match
                newItemIdx = __FindItem(refItemsList[itemIdx].name, tgtItemsList);
                if newItemIdx != -1:
                    inv.Set("sItemIndex", str(newItemIdx));
                    print("    New target item {0} ({1}). Was: {2} ({3})".format(newItemIdx, tgtItemsList[newItemIdx].name, itemIdx, refItemsList[itemIdx].name));
                else:
                    print("    !! Ref item {0} ({1}) is not found in target.".format(itemIdx, refItemsList[itemIdx].name));
                continue;
            if tgtItemsList[itemIdx].ForSell() == False:
                print("    !! Target item {0} ({1}) is NOT FOR SELL".format(itemIdx, tgtItemsList[itemIdx].name));
    return result;
#end def _ValidateInventory(root, refItemsList, tgtItemsList):


def _GenerateInventory(root, tgtItemsList):
    def __PickItem(tgtItemsList):
        result = 0;
        while result == 0:
            ti = random.randint(0, len(TARGET_RND_ID_RANGE) - 1);
            ri = random.randint(0, len(TARGET_RND_ID_RANGE[ti]) - 1);
            ii = TARGET_RND_ID_RANGE[ti][ri];
            item = tgtItemsList[ii];
            if (item != None) and (item.ForSell() == True) and (item.price <= 300):
                result = ii;
        return str(result);
    
    totalPieces_max = 30;
    totalPieces_min = 10;
    slots_max = 15;
    
    random.seed();
    totalPieces = random.randint(totalPieces_min, totalPieces_max);
    
    leftPieces = totalPieces;
    for slotIdx in range(0, slots_max):
        itemId = __PickItem(tgtItemsList);
        
        if leftPieces > 4:
            itemNum = random.randint(1, 4);
        else:
            itemNum = random.randint(1, leftPieces);
        
        if slotIdx == 0:
            inv = Item(root[slotIdx]);
            inv.Set("sItemIndex", itemId);
            inv.Set("ubOptimalNumber", str(itemNum));
        else:
            inv = Item.Spawn("INVENTORY");
            inv.Set("uiIndex", str(slotIdx));
            inv.Set("sItemIndex", itemId);
            inv.Set("ubOptimalNumber", str(itemNum));
            root.append(inv.xml);
            pass;
        
        leftPieces = leftPieces - itemNum;
        if leftPieces <= 0:
            break;
#end def _GenerateInventory(root, tgtItemsList):


def GenerateAdditionalMerchantsXml(refRootDir, targetRootDir):    
    refItemsList = _ListFromItemsXml(refRootDir);
    tgtItemsList = _ListFromItemsXml(targetRootDir);
    
    #newDirPath = os.path.join(targetRootDir, r"NPCInventory\NEW");
    #if not os.path.exists(newDirPath):
    #    os.makedirs(newDirPath);
    
    for i in range(1, 61):
        xmlRelPath = "NPCInventory\\AdditionalDealer_{0}_Inventory.xml".format(i);
        addMerchantXmlPath = os.path.join(refRootDir, xmlRelPath);
        print("{0}:".format(xmlRelPath));
        tree = ET.parse(addMerchantXmlPath);
        root = tree.getroot();
        
        validItemsCnt = _ValidateInventory(root, refItemsList, tgtItemsList);
        if validItemsCnt == 0:
            _GenerateInventory(root, tgtItemsList);
        
        f = open(os.path.join(targetRootDir, xmlRelPath), "w");
        f.write(r'<?xml version="1.0" encoding="utf-8"?>' + '\n');
        tree.write(f, encoding="utf-8", xml_declaration=None, default_namespace=None, method="xml");
        f.close();
#end def GenerateAdditionalMerchantsXml(refRootDir, targetRootDir):


def EnlistAdditionalMerchantsInventory(rootDir, showEmpty):
    refItemsList = _ListFromItemsXml(rootDir);
    
    for i in range(1, 61):
        xmlRelPath = "NPCInventory\\AdditionalDealer_{0}_Inventory.xml".format(i);
        addMerchantXmlPath = os.path.join(rootDir, xmlRelPath);
        print("{0}:".format(xmlRelPath));
        tree = ET.parse(addMerchantXmlPath);
        root = tree.getroot();
        
        for xmlInv in root:
            inv = Item(xmlInv);
            itemIdx = int(inv.Get("sItemIndex"));
            itemCnt = int(inv.Get("ubOptimalNumber"));
            hasCnt = inv.Has("ubOptimalNumber");

            if refItemsList[itemIdx] != None:
                itemName = refItemsList[itemIdx].name;
            else:
                itemName = "PLACEHOLDER";
            
            if hasCnt == True:
                if (showEmpty == False) and (itemCnt == 0):
                    pass;
                else:
                    print("    {0} ({1});    {2} pcs".format(itemName, itemIdx, itemCnt));
            else:
                print("    !! {0} ({1});    NO pcs ATTRIBUTE".format(itemName, itemIdx));
#end def EnlistAdditionalMerchantsInventory(root, showEmpty):


#
# Entry point (like Main())
#
#GenerateAdditionalMerchantsXml(REF_TABLE_DATA_ROOT, TARGET_TABLE_DATA_ROOT);
EnlistAdditionalMerchantsInventory(TARGET_TABLE_DATA_ROOT, False);
#EnlistAdditionalMerchantsInventory(REF_TABLE_DATA_ROOT);
