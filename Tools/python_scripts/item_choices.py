#### USAGE ####
# 0. Ensure you have !!! Python 3 !!! installed (version 3.x -- does not matter).
# 1. Run this script (i.e. "item_choices.py") in a cmd line window with the following arguments format:
#    item_choices.py  <what>  <who>  <rank>
#    or
#    item_choices.py  imp
#    <what> : g - guns, i - items
#    <who>  : e - enemies, m - militia
#    <rank> : 1 - admin/green, 2 - regular, 3 - elite
# X. More commonly used examples:
#    "> python item_choices.py imp"     - will print IMPItemChoices.xml in readable form.
#    "> python item_choices.py g e 2"   - will print GunChoices_Enemy_Regular.xml in readable form, and so on.


import os, sys;
import xml.etree.ElementTree as ET;

#
# Script setup values
#
SWDIR = os.getcwd();
TABLE_DATA_ROOT = r'{}\..\..\Data-BRAINMOD\TableData'.format(SWDIR);
INVENTORY_DATA_ROOT = os.path.join(TABLE_DATA_ROOT, "Inventory");
ITEMS_DATA_ROOT = os.path.join(TABLE_DATA_ROOT, "Items");


#
# Constants, functions, classes etc
#

def PrintItemChoises(root, itemsRoot, isIMP):
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
        result = "?None?";
        for tagObj in itemXmlObj:
            if tagObj.tag == "usPrice":
                result = tagObj.text;
                break;
        if result == None:
            result = "0";
        return result;
    #end def _GetItemCost(itemXmlObj):
    
    for choice in root:
        index = choice[0].text;
        name = choice[1].text;
        itemsNum = int(choice[2].text);
        itemsStartIdx = 3;
        
        impPart = "";
        if isIMP == True:
            impPart = ", amount to pick = {}".format(choice[3].text);
            itemsStartIdx = 4;
        
        print("[{}] {} ({} items{}):".format(index, name, itemsNum, impPart));
        
        for itemIdx in range(itemsStartIdx, itemsStartIdx + itemsNum):
            itemId = int(choice[itemIdx].text);
            itemName = _GetItemName(itemsRoot[itemId]);
            itemCost = _GetItemCost(itemsRoot[itemId]);
            print("  Item {} =  {} ({}, ${})".format(itemIdx - itemsStartIdx + 1, itemName, itemId, itemCost));
        
        # check for unused items, i.e. declared out of "itemsNum" bound
        for itemIdx in range(itemsStartIdx + itemsNum, itemsStartIdx + 50):
            itemId = int(choice[itemIdx].text);
            if itemId != 0:
                itemName = _GetItemName(itemsRoot[itemId]);
                itemCost = _GetItemCost(itemsRoot[itemId]);
                print("  ! Unused Item {} =  {} ({}, ${})".format(itemIdx - itemsStartIdx + 1, itemName, itemId, itemCost));
        
        print("");
    #end for choice in root:
#end PrintItemChoises(root, itemsRoot):


#
# Entry point (like Main())
#

fileName = None;
isIMP = False;

if sys.argv[1].lower() == "imp":
    fileName = "IMPItemChoices.xml";
    isIMP = True;
elif len(sys.argv) == 4:
    what = None;
    who = None;
    rank = None;
    
    if sys.argv[1] == 'g':
        what = "Gun";
    elif sys.argv[1] == 'i':
        what = "Item";
    
    if sys.argv[2] == 'e':
        who = "Enemy";
    elif sys.argv[2] == 'm':
        who = "Militia";
    
    if sys.argv[3] == '1':
        if who == "Enemy":
            rank = "Admin";
        else:
            rank = "Green";
    elif sys.argv[3] == '2':
        rank = "Regular";
    elif sys.argv[3] == '3':
        rank = "Elite";
    
    if (what != None) and (who != None) and (rank != None):
        fileName = "{}Choices_{}_{}.xml".format(what, who, rank);

if fileName != None:
    itemsTree = ET.parse(os.path.join(ITEMS_DATA_ROOT, "Items.xml"));
    itemsRoot = itemsTree.getroot();
    
    tree = ET.parse(os.path.join(INVENTORY_DATA_ROOT, fileName));
    root = tree.getroot();
    
    PrintItemChoises(root, itemsRoot, isIMP);
else:
    print("Invalid input arguments.");
