#### USAGE ####
# 0. Ensure you have !!! Python 3 !!! installed (version 3.x -- does not matter).
# 1. ???
# 2. ???
# 3. Run this script (i.e. "realistic_attachments.py") in a cmd line window.
#


import os, sys;
import xml.etree.ElementTree as ET;
from imports.xml_manager import XmlManager;
from imports.xml_utils import XmlUtils;

#
# Script setup values
#
SWDIR = os.getcwd();
TABLE_DATA_ROOT = r'{}\..\..\Data-BRAINMOD\TableData'.format(SWDIR);
INVENTORY_DATA_ROOT = os.path.join(TABLE_DATA_ROOT, "Inventory");
ITEMS_DATA_ROOT = os.path.join(TABLE_DATA_ROOT, "Items");

ITEMS_XML = "Items.xml";
ATTACHMENTS_XML = "Attachments.xml";


#
# Globals
#
g_XmlMan = None;


#
# Constants, functions, classes etc
#

def PrintAttachmentItems(args):
    global g_XmlMan;
    itemsRoot = g_XmlMan.GetXml(ITEMS_XML);
    attRoot = g_XmlMan.GetXml(ATTACHMENTS_XML);
    
    attIds = [];
    
    for att in attRoot:
        attId = int(XmlUtils.GetTagValue(att, "attachmentIndex"));
        if (attId in attIds) == False:
            attIds.append(attId);
    
    for att in attIds:
        n = XmlUtils.GetTagValue(itemsRoot[att], "szLongItemName");
        print("[{}] {}".format(att, n));
#end def PrintAttachmentItems(args):


#
# Entry point (like Main())
#

cmdFunc = None;
args = [];

for i in range(1, len(sys.argv)):
    if i == 1 and sys.argv[i] == 'PrintAttachmentItems':
        cmdFunc = PrintAttachmentItems;
    #elif i == 1 and sys.argv[i] == 'f':
    #    cmdFunc = FixGearKitsCost;
    else:  # parse an argument
        dec = 0;
        
        try:
            dec = int(sys.argv[i]);
        except Exception as e:
            #dec = MercTypes.ToType(sys.argv[i]);   -- try other types
            #if dec == None:
            #    dec = sys.argv[i];
            dec = sys.argv[i];  # add this arg as a string
        
        args.append(dec);

if cmdFunc != None:
    g_XmlMan = XmlManager();
    g_XmlMan.AddXml(ITEMS_DATA_ROOT, ITEMS_XML);
    g_XmlMan.AddXml(ITEMS_DATA_ROOT, ATTACHMENTS_XML);
    
    dirty = cmdFunc(args);
else:
    print("Invalid input arguments.");
    print("Valid functions: PrintAttachmentItems");
