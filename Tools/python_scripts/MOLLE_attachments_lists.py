import xml.etree.ElementTree as ET;

#
# Script setup values
#
SOURCE_ITEMS_XML = r'D:\Programs\JaggedAlliance2\Data-AIM\TableData\Items\Items.xml';
SOURCE_ATTACHMENTS_XML = r'D:\Programs\JaggedAlliance2\Data-AIM\TableData\Items\Attachments.xml';
OUTPUT_FILE_TXT = r'D:\MOLLE_attachments.txt';


#
# Constants, functions, classes etc
#
DEBUG_MODE = False;
MOLLE_CARRIERS_START_ID = 916;
MOLLE_CARRIERS_END_ID =   930;
MOLLE_CARRIERS_IDS =      [853, 866, 879, 892, 905];
MOLLE_MODULES_START_ID =  931;
MOLLE_MODULES_END_ID =    1000;



class Item:
    def __init__(self):
        self.name = "";
        self.id_ = -1;
        self.attachments = [];
    
    def IsInUse(self):
        return True if len(self.attachments) > 0 else False;

    def InUseCount(self):
        return len(self.attachments);
        
    def AddUse(self, use):
        self.attachments.append(use);
#end class Item:


def GenItemObjects(root, start_id, end_id, id_list = None):
    result = [];
    for item in root:
        itemObj = Item();
        for prop in item:
            if prop.tag == "uiIndex":
                itemObj.id_ = int(prop.text);
            elif prop.tag == "szLongItemName":
                itemObj.name = prop.text;
        
        if start_id <= itemObj.id_ and itemObj.id_ <= end_id and itemObj.name != "Placeholder":
            result.append(itemObj);
        elif id_list != None and itemObj.id_ in id_list and itemObj.name != "Placeholder":
            result.append(itemObj);
    #end for item in root:
    return result;
#end def GenItemObjects(root, start_id, end_id):


def CopyItemObject(item):
    result = None;
    if item != None:
        result = Item();
        result.id_ = item.id_;
        result.name = item.name;
    return result;
#end def CopyItemObject(item):


def FindItemObject(items, target_id):
    result = None;
    for item in items:
        if item.id_ == target_id:
            result = item;
            break;
    return result;
#end def FindItemObject(items, target_id):


def AssignPossibleAttachments(carriers, modules, root_attachments):
    i = -1;
    for att in root_attachments:
        i = i + 1;
        attachmentIndex = -1;
        itemIndex = -1;
        for prop in att:
            if prop.tag == "attachmentIndex":
                attachmentIndex = int(prop.text);
            elif prop.tag == "itemIndex":
                itemIndex = int(prop.text);
        #end for prop in att:
        
        if attachmentIndex == -1 or itemIndex == -1:
            print("Bad <ATTACHMENT> element at #{0}".format(i));
            continue;
        
        carrier = FindItemObject(carriers, itemIndex);
        module = FindItemObject(modules, attachmentIndex);
        
        if carrier != None:  # this attachment rule is about one of our carriers
            moduleToAppend = module;  # avoid overriding value of 'module'
            if moduleToAppend == None:  # an unknown attachment (non-MOLLE) is specified!
                moduleToAppend = Item();
                moduleToAppend.id_ = attachmentIndex;
                moduleToAppend.name = "UNKNOWN ATTACHMENT";
            carrier.AddUse(moduleToAppend);
        
        if module != None:  # this attachment rule is about one of our modules
            carrierToAppend = carrier;  # avoid overriding value of 'carrier'
            if carrierToAppend == None:  # an unknown carrier (non-MOLLE item) is specified!
                carrierToAppend = Item();
                carrierToAppend.id_ = itemIndex;
                carrierToAppend.name = "UNKNOWN CARRIER";
            module.AddUse(carrierToAppend);
#end def AssignPossibleAttachments(carriers, modules, root_attachments):


def PrintShortList(f, items):
    for item in items:
        f.write("[{0}] {1}\t|  {2}\n".format(item.id_, item.name, item.InUseCount() if item.IsInUse() else "NOT IN USE"));
#end def PrintShortList(f, items):


def PrintLongList(f, items):
    for item in items:
        if item.IsInUse():
            f.write("[{0}] {1}:\n".format(item.id_, item.name));
            for att in item.attachments:
                f.write("    [{0}] {1}\n".format(att.id_, att.name));
            f.write("\n");
#end def PrintLongList(f, items):


#
# Entry point, like Main()
#
treeAttachments = ET.parse(SOURCE_ATTACHMENTS_XML);
treeItems = ET.parse(SOURCE_ITEMS_XML);
rootAttachments = treeAttachments.getroot();
rootItems = treeItems.getroot();
out_file = open(OUTPUT_FILE_TXT, "w");

carriers = GenItemObjects(rootItems, MOLLE_CARRIERS_START_ID, MOLLE_CARRIERS_END_ID, MOLLE_CARRIERS_IDS);
modules = GenItemObjects(rootItems, MOLLE_MODULES_START_ID, MOLLE_MODULES_END_ID);

AssignPossibleAttachments(carriers, modules, rootAttachments);  # main analysis logic is here

out_file.write("Short MOLLE carriers list ([id] name | possible modules count)\n");
PrintShortList(out_file, carriers);
out_file.write("\n");
out_file.write("Short MOLLE modules list ([id] name | compatible carriers count)\n");
PrintShortList(out_file, modules);
out_file.write("\n");

out_file.write("Long MOLLE carriers list (with possible modules)\n");
PrintLongList(out_file, carriers);
out_file.write("\n");
out_file.write("Long MOLLE modules list (with compatible carriers)\n");
PrintLongList(out_file, modules);
out_file.write("\n");

out_file.close();
#end Main()
