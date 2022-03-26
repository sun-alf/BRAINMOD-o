import os, sys;
import xml.etree.ElementTree as ET;

#
# Script setup values
#
SOURCE_ITEMS_XML = r'D:\Programs\JaggedAlliance2\Data-BRAINMOD\TableData\Items\Items.xml';
NEW_ITEMS_XML = r'D:\Programs\JaggedAlliance2\Data-BRAINMOD\TableData\Items\New_Items.xml';
#SOURCE_ITEMS_XML = r'E:\Items.xml';
#NEW_ITEMS_XML = r'E:\New_Items.xml';


ITEM_CLASS = 268435456;  # for all types of aiming attachments: iron/reflex/laser sights, scopes
LASER_ATTACHMENT_CLASS = 4;
SIGHT_ATTACHMENT_CLASS = 8;
SCOPE_ATTACHMENT_CLASS = 16;
SCOPE_NAS_ATTACHMENT_CLASS = 32;
REFLEX_NAS_ATTACHMENT_CLASS = 64;
LASER_NAS_ATTACHMENT_CLASS = 128;


#
# Constants, functions, classes etc
#
class Item():
    def __init__(self, xml_member):
        self.xml = xml_member;
    
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
#end class Item():


def _MergeLists(list1, list2):
    for el in list2:
    	list1.append(el);
#end def _MergeLists(list1, list2):


def _FetchPrintItems(root, itemC, attC, nasAttC, printTotal):
    totalItems = 0;
    print("ID    Name          MagFactor  %AP_reduct");
    for xml_item in root:
        item = Item(xml_item);
        if int(item.Get("usItemClass")) == itemC and \
                int(item.Get("AttachmentClass")) == attC and \
                int(item.Get("nasAttachmentClass")) == nasAttC:
            totalItems = totalItems + 1;
            print("{0}  {1}  {2}  {3}%".format( \
                    item.Get("uiIndex"), \
                    item.Get("szLongItemName"), \
                    item.Get("ScopeMagFactor"), \
                    item.Get("PercentAPReduction")));
    if printTotal == True:
        print("TOTAL: " + str(totalItems));
    return totalItems;
#end def _FetchPrintItems(root, itemC, attC, nasAttC):


def _PrintItems(items, printTotal):
    print("ID    Name          MagFactor  %AP_reduct");
    for item in items:
        print("{0}  {1}  {2}  {3}%".format( \
                item.Get("uiIndex"), \
                item.Get("szLongItemName"), \
                item.Get("ScopeMagFactor"), \
                item.Get("PercentAPReduction")));
    if printTotal == True:
        print("TOTAL: " + str(len(items)));
    return len(items);
#end def _PrintItems(items, printTotal):


def _FetchItems(root, itemC, attC, nasAttC):
    result = [];
    for xml_item in root:
        item = Item(xml_item);
        if int(item.Get("usItemClass")) == itemC and \
                int(item.Get("AttachmentClass")) == attC and \
                int(item.Get("nasAttachmentClass")) == nasAttC:
            result.append(item);
    return result;
#end def _FetchItems(root, itemC, attC, nasAttC):


def EnlistAllScopes(root):
    _FetchPrintItems(root, ITEM_CLASS, SCOPE_ATTACHMENT_CLASS, SCOPE_NAS_ATTACHMENT_CLASS, True);
    return False;
#end def EnlistAllScopes(root):


def EnlistAllReflexSights(root):
    t = _FetchPrintItems(root, ITEM_CLASS, SIGHT_ATTACHMENT_CLASS, SCOPE_NAS_ATTACHMENT_CLASS, False);
    t = _FetchPrintItems(root, ITEM_CLASS, SIGHT_ATTACHMENT_CLASS, REFLEX_NAS_ATTACHMENT_CLASS, False) + t;
    print("TOTAL: " + str(t));
    return False;
#end def EnlistAllReflexSights(root):

def EnlistAllLasers(root):
    _FetchPrintItems(root, ITEM_CLASS, LASER_ATTACHMENT_CLASS, LASER_NAS_ATTACHMENT_CLASS, True);
    return False;
#end def EnlistAllLasers(root):


def ChangeVisionRangeBonus(root, change_percents):
	def __ChangeBonus(item, prop, change):
		propValue = item.Get(prop);
		if propValue != "0":  # if the property exists and it is not 0; otherwise just don't touch it
			currentValue = int(propValue);
			newValue = int(currentValue * change / 100);
			item.Set(prop, str(newValue));
	#end def __ChangeBonus(item, prop, change):

	all_sights = _FetchItems(root, ITEM_CLASS, SIGHT_ATTACHMENT_CLASS, SCOPE_NAS_ATTACHMENT_CLASS);
	_MergeLists(all_sights, _FetchItems(root, ITEM_CLASS, SIGHT_ATTACHMENT_CLASS, REFLEX_NAS_ATTACHMENT_CLASS));
	_MergeLists(all_sights, _FetchItems(root, ITEM_CLASS, SCOPE_ATTACHMENT_CLASS, SCOPE_NAS_ATTACHMENT_CLASS));
	
	#_PrintItems(all_sights, True);
	
	for item in all_sights:
		for key in change_percents:
			__ChangeBonus(item, key, change_percents[key]);
	
	return True;
#end def ChangeVisionRangeBonus(root):

#
# Entry point (like Main())
#
tree = ET.parse(SOURCE_ITEMS_XML);
root = tree.getroot();

modified = False;
#print("\nSCOPES (optical and red dot):");
#modified = EnlistAllScopes(root) or modified;
#print("\nREFLEX:");
#modified = EnlistAllReflexSights(root) or modified;
#print("\nLASERS:");
#modified = EnlistAllLasers(root) or modified;
change_percents = dict();
for arg in sys.argv[1:]:
    if arg.lower().find("night=") == 0:
        val = int(arg[len("night=") : ]);
        change_percents["NightVisionRangeBonus"] = val;
    elif arg.lower().find("day=") == 0:
        val = int(arg[len("day=") : ]);
        change_percents["DayVisionRangeBonus"] = val;
    elif arg.lower().find("cave=") == 0:
        val = int(arg[len("cave=") : ]);
        change_percents["CaveVisionRangeBonus"] = val;
    elif arg.lower().find("bright=") == 0:
        val = int(arg[len("bright=") : ]);
        change_percents["BrightLightVisionRangeBonus"] = val;
    elif arg.lower().find("tohit=") == 0:
        val = int(arg[len("tohit=") : ]);
        change_percents["ToHitBonus"] = val;
    elif arg.lower().find("list=") == 0:
        val = arg[len("list=") : ];
        val = val.strip().lower();
        if val == "scope" or val == "scopes" or val == "s":
            EnlistAllScopes(root);
        elif val == "reflex" or val == "refl" or val == "r" or val == "sight":
            EnlistAllReflexSights(root);
        elif val == "laser" or val == "lasers" or val == "l" or val == "las":
            EnlistAllLasers(root);
    else:
        print("Unknown argument: {0}".format(arg));

modified = ChangeVisionRangeBonus(root, change_percents);

if modified:
    tree.write(NEW_ITEMS_XML);

