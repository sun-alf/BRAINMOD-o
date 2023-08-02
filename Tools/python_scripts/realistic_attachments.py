#### USAGE ####
# 0. Ensure you have !!! Python 3 !!! installed (version 3.x -- does not matter).
# 1. ???
# 2. ???
# 3. Run this script (i.e. "realistic_attachments.py") in a cmd line window.
#


import os, sys;
import xml.etree.ElementTree as ET;
from imports.JA2TableData import JA2TableData, JA2Workspaces, JA2Xmls;
from imports.xml_utils import XmlUtils;
from imports.cmd_line import CmdLineProcessor;

#
# Script setup values
#


#
# Globals
#


#
# Constants, functions, classes etc
#

def PrintAttachmentItems(args):
    itemsRoot = JA2TableData.GetXml(JA2Xmls.ITEMS);
    attRoot = JA2TableData.GetXml(JA2Xmls.ATTACHMENTS);
    
    attIds = [];
    
    for att in attRoot:
        attId = int(XmlUtils.GetTagValue(att, "attachmentIndex"));
        if (attId in attIds) == False:
            attIds.append(attId);
    
    for att in attIds:
        n = XmlUtils.GetTagValue(itemsRoot[att], "szLongItemName");
        print("[{}] {}".format(att, n));
#end def PrintAttachmentItems(args):


def TestFunc(args):
    JA2TableData.OpenWorkspace(JA2Workspaces.BRAINMOD);
    a  = [getattr(JA2Xmls, field) for field in dir(JA2Xmls) if not callable(getattr(JA2Xmls, field)) and not field.startswith("__")];
    print(a);
    #b = [JA2Xmls.field for field]
    if JA2Xmls.ITEMS in a:
        print("good");
    else:
        print("bad");
    print([field for field in dir(JA2Xmls) if not callable(getattr(JA2Xmls, field)) and not field.startswith("__")]);
    print([field for field in dir(JA2Workspaces) if not callable(getattr(JA2Workspaces, field)) and not field.startswith("__")]);
#end def TestFunc(args):


#
# Entry point (like Main())
#
JA2TableData.OpenWorkspace(JA2Workspaces.BRAINMOD);

cmd_map = {"PrintAttachmentItems" : PrintAttachmentItems, "Test" : TestFunc};
cmd_line = CmdLineProcessor(cmd_map);
cmd_line.Execute(sys.argv);
