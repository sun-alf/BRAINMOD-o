#### USAGE ####
# 0. Ensure you have !!! Python 3 !!! installed (version 3.x -- does not matter).
# 1. ???
# 2. ???
# 3. Run this script (i.e. "realistic_attachments.py") in a cmd line window.
#


import os, sys;
import copy;
import xml.etree.ElementTree as ET;
from imports.JA2TableData import JA2TableData, JA2Workspaces, JA2Xmls, SWDIR;
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


def PrintAttachmentInfo(args):
    itemsRoot = JA2TableData.GetXml(JA2Xmls.ITEMS);
    itemClassRoot = JA2TableData.GetXml(JA2Xmls.LOOKUP_ITEM_CLASS);
    attInfoRoot = JA2TableData.GetXml(JA2Xmls.ATTACHMENT_INFO);
    
    index = 0;
    
    for attInfo in attInfoRoot:
        attId = int(XmlUtils.GetTagValue(attInfo, "usItem"));
        attClass = XmlUtils.GetTagValue(attInfo, "uiItemClass");
        attSkillCheck = XmlUtils.GetTagValue(attInfo, "bAttachmentSkillCheck");
        attSkillCheckMod = XmlUtils.GetTagValue(attInfo, "bAttachmentSkillCheckMod");
        
        for itemClass in itemClassRoot:
            if XmlUtils.GetTagValue(itemClass, "id") == attClass:
                attClass = XmlUtils.GetTagValue(itemClass, "name");
                break;
        
        print("[{}] {} / {}  | min skill = {}, skill bonus = {}".format(index, XmlUtils.GetTagValue(itemsRoot[attId], "szLongItemName"), attClass, attSkillCheck, attSkillCheckMod));
        index = index + 1;
#end def PrintAttachmentInfo(args):


def TestFunc(args):
    def _HasCompatibleSlot(descr, mountMethod, givenSpace):
        intGivenSpace = int(givenSpace);
        for slot in descr:
            if slot.attrib["system"] == mountMethod and int(slot.attrib["space"]) <= intGivenSpace:
                return True;
        return False;
    #end def _HasCompatibleSlot(descr, mountMethod, givenSpace):
    
    # This should work only with copies of elements of AttachmentsDescriptors.xml tree (original tree should stay intact)
    def _MarkCompatibleSlot(descr, mountMethod, givenSpace):
        intGivenSpace = int(givenSpace);
        for slot in descr:
            if slot.attrib["system"] == mountMethod and int(slot.attrib["space"]) <= intGivenSpace:
                slot.attrib["useThis"] = "True";
                return;
        # We should never reach this point, this func must find a slot.
        raise Exception("Slot system = {} space = {} was not found.\ndescr = {}".format(mountMethod, givenSpace, _DoSomePythonPorn(descr)));
    #end def _MarkCompatibleSlot(descr, mountMethod, givenSpace):

    def _GetCompatibleSlot(descr):
        for slot in descr:
            if "useThis" in slot.attrib and slot.attrib["useThis"] == "True":
                return slot;
        return None;
    #end def _GetCompatibleSlot(descr):

    def _FindCompatibleAttachment(attachmentsList, attachmentId):
        result = None;
        for att in attachmentsList:
            if att.attrib["attachment_id"] == attachmentId:
                result = att;
                break;
        return result;
    #end def _FindCompatibleAttachment(attachmentsList, attachmentId):

    def _DoSomePythonPorn(xxx):
        d = xxx.attrib;
        slots = list();
        for slot in xxx:
            slots.append(slot.attrib);
        d["slots"] = slots;
        return d;
    #end def _DoSomePythonPorn(xxx):

    def _FormatDbgText(gunId, gunName, compatibleAttachments, compatibleAttachment):
        compatibleAttachment = __DoMorePythonPorn(compatibleAttachment);
        for i in range(0, len(compatibleAttachments)):
            compatibleAttachments[i] = __DoMorePythonPorn(compatibleAttachments[i]);
        return "gunId = {}\ngunName = {}\ncompatibleAttachments = {}\ncompatibleAttachment = {}\n".format(gunId, gunName, compatibleAttachments, compatibleAttachment);
    #end def _FormatDbgText(gunId, gunName, compatibleAttachments, compatibleAttachment):

    JA2TableData.OpenWorkspace(os.path.join(SWDIR, "input"));
    mountSystems = JA2TableData.GetXml("MountSystems.xml", wsName="input");
    attachmentsDesc = JA2TableData.GetXml("AttachmentsDescriptors.xml", wsName="input");
    gunsDesc = JA2TableData.GetXml("GunsDescriptors.xml", wsName="input");
    attachments = JA2TableData.GetXml(JA2Xmls.ATTACHMENTS);
    
    for gunDesc in gunsDesc:
        if gunDesc.attrib["weapon_id"] == "0":  # exit on "NULL-TERMINATOR" spot, for script debug purposes only.
            break;
        
        # Main part of this task: form a list of attachments in accordance to rules provided by "/input" XMLs.
        # The list will be in var 'compatibleAttachments'.
        gunId = gunDesc.attrib["weapon_id"];
        gunName = gunDesc.attrib["name"];
        compatibleAttachments = list();
        for interface in gunDesc:
            for attachmentDesc in attachmentsDesc:
                if attachmentDesc.attrib["attachment_id"] == "0":  # exit on "NULL-TERMINATOR" spot, for script debug purposes only.
                    break;
                if _HasCompatibleSlot(attachmentDesc, interface.attrib["system"], interface.attrib["space"]):
                    attachmentDescCopy = copy.deepcopy(attachmentDesc);
                    _MarkCompatibleSlot(attachmentDescCopy, interface.attrib["system"], interface.attrib["space"]);
                    compatibleAttachments.append(attachmentDescCopy);

        # Sometimes the same attachment can fit multiple interfaces on a gun, i.e. Picatinny compatible laser can be mounted onto
        # under-barrel or side-barrel rail. In this case we will have entries for this attachment in 'compatibleAttachments'. We
        # have to get rid of redundant entries as the game does not those mount positions; also, multiple entries will spam
        # Attachments.xml what is not good.
        filteredList = list();
        for item in compatibleAttachments:
            if item not in filteredList:
                filteredList.append(item);
        compatibleAttachments = filteredList;
        
        # Print the resulting list, mostly for debug purposes.
        print("Gun [{}] \'{}\' real.attachments:".format(gunId, gunName));
        for att in compatibleAttachments:
            print("    [{}] {}".format(att.attrib["attachment_id"], att.attrib["name"]));
        
        # Now it is time to edit Attachments.xml so that unrealistic attachment combinations will be removed, the only allowed
        # combinations (which correspond to 'compatibleAttachments' list) will be kept, and additional allowed combinations
        # (if any) will be added. To do so, we assume that current Attachments.xml allows too much possible attachments, much
        # more than it in real life is.
        for attachment in attachments:
            if XmlUtils.GetTagValue(attachment, "itemIndex") == gunId:  # found an attachment for a gun in question
                compatibleAttachment = _FindCompatibleAttachment(compatibleAttachments, XmlUtils.GetTagValue(attachment, "attachmentIndex"));
                if compatibleAttachment != None:  # if the 'attachment' is in allowed list
                    compatibleSlot = _GetCompatibleSlot(compatibleAttachment);
                    if compatibleSlot == None:  # at this point _GetCompatibleSlot() must return an object, not None
                        exceptionDbgText = _FormatDbgText(gunId, gunName, compatibleAttachments, compatibleAttachment);
                        raise Exception(exceptionDbgText);
                    XmlUtils.SetTagValue(attachment, "APCost", compatibleSlot.attrib["timeAP"]);  # then update APCost and leave it
                    compatibleAttachments.remove(compatibleAttachment);  # we don't need it anymore as there is no sence to put the same element into Attachments.xml more than once
                else:  # otherwise remove it from Attachments.xml
                    attachments.remove(attachment);
        
        # Check if something is left in 'compatibleAttachments', and if it is, that means we have some new attachments for Attachments.xml
        # in our realistic attachments update.
        if len(compatibleAttachments) > 0:
            for att in compatibleAttachments:
                attId = att.attrib["attachment_id"];
                attName = att.attrib["name"];
                print("ACHTUNG! Add a new entry to Attachments.xml: [{}] {} --> [{}] {}".format(attId, attName, gunId, gunName));
                
                compatibleSlot = _GetCompatibleSlot(att);
                newAttachment = copy.deepcopy(attachments[0]);  # take a copy of the first element of the tree as it is much easier than create&fill a new element object
                XmlUtils.SetTagValue(newAttachment, "attachmentIndex", attId);
                XmlUtils.SetTagValue(newAttachment, "itemIndex", gunId);
                XmlUtils.SetTagValue(newAttachment, "APCost", compatibleSlot.attrib["timeAP"]);
                attachments.append(newAttachment);
    
    JA2TableData.GetWorkspace(JA2Workspaces.BRAINMOD).SaveXml(JA2Xmls.ATTACHMENTS);
#end def TestFunc(args):


def GenerateTemplateAttachmentsXml(args):
    idListFile = open("C:\\Temp\\gun_attachments.txt", "r");
    idLines = idListFile.readlines();
    idListFile.close();
    
    newXML = open("C:\\Temp\\new.xml", "w");
    newXML.write(r'<?xml version="1.0" encoding="utf-8"?>' + "\n");
    newXML.write(r'<AttachmentsDescriptors>' + "\n");
    
    for line in idLines:
        if line.find("[") == 0:
            itemId = line[1 : line.find("]")];
            itemName = line.split("] ")[1].strip();
            newXML.write("\t" + r'<Descriptor attachment_id="{}" name="{}">'.format(itemId, itemName) + "\n");
            newXML.write("\t\t" + r'<Slot system="0" space="1" timeAP="60"/>' + "\n");
            newXML.write("\t" + r'</Descriptor>' + "\n");

    newXML.write(r'</AttachmentsDescriptors>' + "\n");
    newXML.close();
#end GenerateTemplateAttachmentsXml(args):


def GenerateTemplateGunsXml(args):
    itemsRoot = JA2TableData.GetXml(JA2Xmls.ITEMS);
    weaponsRoot = JA2TableData.GetXml(JA2Xmls.WEAPONS);
    weaponClassRoot = JA2TableData.GetXml(JA2Xmls.LOOKUP_WEAPON_CLASS);
    weaponTypeRoot = JA2TableData.GetXml(JA2Xmls.LOOKUP_WEAPON_TYPE);
    
    weaponClasses = XmlUtils.LoadToList(weaponClassRoot);
    weaponTypes = XmlUtils.LoadToList(weaponTypeRoot);
    
    newXML = open("C:\\Temp\\new.xml", "w", encoding='utf-8');
    newXML.write(r'<?xml version="1.0" encoding="utf-8"?>' + "\n");
    newXML.write(r'<GunsDescriptors>' + "\n");
    
    for weapon in weaponsRoot:
        weaponClassId = XmlUtils.GetTagValue(weapon, "ubWeaponClass");
        if weaponClassId != None:
            weaponClass = weaponClasses[int(weaponClassId)]["name"];
        else:  # skip throwing and different stuff
            continue;
        weaponTypeId = XmlUtils.GetTagValue(weapon, "ubWeaponType");
        if weaponTypeId != None:
            weaponType = weaponTypes[int(weaponTypeId)]["name"];
        
        if weaponClass != "None" and weaponClass != "Knife" and weaponClass != "Monster":  # if it is a firearm
            itemId = XmlUtils.GetTagValue(weapon, "uiIndex");
            itemName = XmlUtils.SanitizeString(XmlUtils.GetTagValue(weapon, "szWeaponName"));
            itemLongName = XmlUtils.SanitizeString(XmlUtils.GetTagValue(itemsRoot[int(itemId)], "szLongItemName"));
            newXML.write("\t" + r'<Descriptor weapon_id="{}" name="{}" longname="{}">'.format(itemId, itemName, itemLongName) + "\n");
            newXML.write("\t\t" + r'<Interface system="0" space="1"/>' + "\n");
            newXML.write("\t" + r'</Descriptor>' + "\n");

    newXML.write(r'</GunsDescriptors>' + "\n");
    newXML.close();
#end GenerateTemplateGunsXml(args):


#
# Entry point (like Main())
#
JA2TableData.OpenWorkspace(JA2Workspaces.BRAINMOD);

cmd_map = { "PrintAttachmentItems" : PrintAttachmentItems, "PrintAttachmentInfo" : PrintAttachmentInfo,
            "Test" : TestFunc, "GenGuns" : GenerateTemplateGunsXml, "GenAtts" : GenerateTemplateAttachmentsXml };
cmd_line = CmdLineProcessor(cmd_map);
cmd_line.Execute(sys.argv);
