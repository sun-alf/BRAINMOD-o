#### USAGE ####
# 0. Ensure you have !!! Python 3 !!! installed (version 3.x -- does not matter).
# 1. ???
# 2. ???
# 3. Run this script (i.e. "realistic_attachments.py") in a cmd line window:
#    > python realistic_attachments.py MakeRealisticAttachments
#    > python realistic_attachments.py MakeRealisticAttachments 1 2 3  -- will process only guns with the given IDs (Glock 17, Glock 18 and Beretta 92F in this example)


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
    
    namedArgs = CmdLineProcessor.FetchNamedArgs(args);
    if len(namedArgs) == 1:
        if namedArgs[0]["name"].lower() == "itemid":  # look-up for all attachments to this item
            itemId = int(namedArgs[0]["value"]);
            print("All attachments for [{}] {}:".format(itemId, XmlUtils.GetTagValue(itemsRoot[itemId], "szLongItemName")));
            for att in attRoot:
                if int(XmlUtils.GetTagValue(att, "itemIndex")) == itemId:
                    attId = int(XmlUtils.GetTagValue(att, "attachmentIndex"));
                    print("[{}] {}".format(attId, XmlUtils.GetTagValue(itemsRoot[attId], "szLongItemName")));
        elif namedArgs[0]["name"].lower() == "attid":  # look-up for all items compatible with this attachment
            attId = int(namedArgs[0]["value"]);
            print("All items for [{}] {}:".format(attId, XmlUtils.GetTagValue(itemsRoot[attId], "szLongItemName")));
            for att in attRoot:
                if int(XmlUtils.GetTagValue(att, "attachmentIndex")) == attId:
                    itemId = int(XmlUtils.GetTagValue(att, "itemIndex"));
                    print("[{}] {}".format(itemId, XmlUtils.GetTagValue(itemsRoot[itemId], "szLongItemName")));
        else:  # just list all attachments
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


def MakeRealisticAttachments(args):
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
        # __DoMorePythonPorn() is not defined yet =(
        compatibleAttachment = __DoMorePythonPorn(compatibleAttachment);
        for i in range(0, len(compatibleAttachments)):
            compatibleAttachments[i] = __DoMorePythonPorn(compatibleAttachments[i]);
        return "gunId = {}\ngunName = {}\ncompatibleAttachments = {}\ncompatibleAttachment = {}\n".format(gunId, gunName, compatibleAttachments, compatibleAttachment);
    #end def _FormatDbgText(gunId, gunName, compatibleAttachments, compatibleAttachment):

    def _LoadIgnoredAttachments(attachmentsDesc):
        result = list();
        foundNull = False;
        for desc in attachmentsDesc:
            if desc.attrib["attachment_id"] == "0":  # "NULL-TERMINATOR" is found
                foundNull = True;
                continue;
            if foundNull:
                result.append(desc.attrib["attachment_id"]);
        return result;
    #end _LoadIgnoredAttachments(attachmentsDesc):

    def _RemoveIgnoredItems(filteringList, ignoreList):
        for item in filteringList:
            if item in ignoreList:
                filteringList.remove(item);
        return filteringList;
    #end def _RemoveIgnoredItems(filteringList, ignoreList):

    # Removes all <DefaultAttachment> tags which are in wrongList from item, then put <DefaultAttachment> tags which are in correctList instead.
    # So this func is assumed to keep all rest (ignored) <DefaultAttachment> tags as is.
    # item -- XML object in Items.xml, shall be of reference type.
    # wrongList -- list of [current] attachment IDs to delete; each ID is of string type.
    # correctList -- list of attachment IDs to insert instead; each ID is of string type.
    def _FixDefaultAttachments(item, wrongList, correctList):
        # find the first place where <DefaultAttachment> tag is
        idxToInsertAt = 11;  # this default index corresponds to <ubWeight> tag of a normal/valid item
        for tagIdx in range(0, len(item)):
            if item[tagIdx].tag == "DefaultAttachment":
                idxToInsertAt = tagIdx;
                break;
        
        # delete wrong attachments
        defAttList = item.findall("DefaultAttachment");
        for el in wrongList:
            for defAtt in defAttList:
                if defAtt.text == el:
                    item.remove(defAtt);
                    break;
        # insert right attachments
        newElementTemplate = ET.Element("DefaultAttachment");
        for el in correctList:
            newEl = copy.deepcopy(newElementTemplate);
            newEl.text = el;
            item.insert(idxToInsertAt, newEl);
    #def _FixDefaultAttachments(item, wrongList, correctList):

    def _Log(f, text):
        f.write(text);
        f.write("\n");
    #end _Log(f, text):

    log = open(os.path.join(SWDIR, "output", "realistic_attachments_changes.log"), "w");
    JA2TableData.OpenWorkspace(os.path.join(SWDIR, "input"));
    mountSystems = JA2TableData.GetXml("MountSystems.xml", wsName="input");
    attachmentsDesc = JA2TableData.GetXml("AttachmentsDescriptors.xml", wsName="input");
    gunsDesc = JA2TableData.GetXml("GunsDescriptors.xml", wsName="input");
    attachments = JA2TableData.GetXml(JA2Xmls.ATTACHMENTS);
    items = JA2TableData.GetXml(JA2Xmls.ITEMS);
    itemsFileChanged = False;
    
    # I decided to use "NULL-TERMINATOR" for not only debug purposes, but for cutting unnecessary elements also. For AttachmentsDescriptors.xml
    # means all attachments after the NULL should be kept intact in Attachments.xml (i.e. completely ignored).
    ignoredAttList = _LoadIgnoredAttachments(attachmentsDesc);  # contains IDs only
    
    for gunDesc in gunsDesc:
        gunId = gunDesc.attrib["weapon_id"];
        
        if gunId == "0":  # exit on "NULL-TERMINATOR" spot.
            break;
        
        if "skip" in gunDesc.attrib:  # "skip" property means skip this gun, that's it.
            continue;
        
        if len(args) > 0 and int(gunId) not in args:  # also skip if this gun is not among given IDs (if any).
            continue;
        
        # Main part of this task: form a list of attachments in accordance to rules provided by "/input" XMLs.
        # The list will be in var 'compatibleAttachments'.
        gunName = gunDesc.attrib["name"];
        compatibleAttachments = list();
        defaultAttachments = list();  # contains IDs only
        
        _Log(log, "Gun [{}] \'{}\' changes:".format(gunId, gunName));
        for interface in gunDesc:
            defaultAttachment = None;
            defaultAttachmentIsCompatible = False;
            if "default" in interface.attrib:  # directly pointed default attachment ID should be considered (for later check-up) disregarding compatibilites
                defaultAttachment = interface.attrib["default"];  # remember the fact there is a defult one, we will check it a bit later
                defaultAttachments.append(defaultAttachment);
            
            for attachmentDesc in attachmentsDesc:
                if attachmentDesc.attrib["attachment_id"] == "0":  # exit on "NULL-TERMINATOR" spot.
                    break;
                if _HasCompatibleSlot(attachmentDesc, interface.attrib["system"], interface.attrib["space"]):
                    attachmentDescCopy = copy.deepcopy(attachmentDesc);
                    _MarkCompatibleSlot(attachmentDescCopy, interface.attrib["system"], interface.attrib["space"]);
                    compatibleAttachments.append(attachmentDescCopy);
                    if defaultAttachment != None and defaultAttachment == attachmentDesc.attrib["attachment_id"]:
                        defaultAttachmentIsCompatible = True;
                    if int(interface.attrib["system"]) < 0:  # if the compatible attachment is of built-in type, remember it as default attachment
                        defaultAttachments.append(attachmentDesc.attrib["attachment_id"]);
            
            # Now check that default attachment (if any) for this interface: it should be compatible with the interface.
            # If not, it is a bold warning! (Default attachments will not appear in the game, if they are not mapped in Attachments.xml)
            if defaultAttachment != None and defaultAttachmentIsCompatible == False:
                _Log(log, "!! Default attachment [{}] is not compatible with this gun!".format(defaultAttachment));

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
        
        # Process default attachments -- check for equality only: if ID set in defaultAttachments != <DefaultAttachment> set then vomit a warning with details
        tagList = items[int(gunId)].findall("DefaultAttachment");
        actualDefaultAttachments = list();
        for tag in tagList:
            actualDefaultAttachments.append(tag.text);
        _RemoveIgnoredItems(actualDefaultAttachments, ignoredAttList);  # remove ignored attachments from current list to avoid false warnings
        defaultAttachments.sort();        # 2 lists of strings could be equal only if order of strings and the strings itself are equal, so
        actualDefaultAttachments.sort();  # let's sort both lists of IDs
        if defaultAttachments != actualDefaultAttachments:
            _Log(log, "!! actual default attachments {} != realistic default attachments {}".format(actualDefaultAttachments, defaultAttachments));
            _FixDefaultAttachments(items[int(gunId)], actualDefaultAttachments, defaultAttachments);
            itemsFileChanged = True;
        
        # Now it is time to edit Attachments.xml so that unrealistic attachment combinations will be removed, the only allowed
        # combinations (which correspond to 'compatibleAttachments' list) will be kept, and additional allowed combinations
        # (if any) will be added. To do so, we assume that current Attachments.xml allows too much possible attachments, much
        # more than it in real life is.
        for attachment in attachments:
            if XmlUtils.GetTagValue(attachment, "itemIndex") == gunId:  # found an attachment for a gun in question
                attachmentId = XmlUtils.GetTagValue(attachment, "attachmentIndex");
                attachmentName = XmlUtils.GetTagValue(items[int(attachmentId)], "szLongItemName");
                compatibleAttachment = _FindCompatibleAttachment(compatibleAttachments, attachmentId);
                if compatibleAttachment != None:  # if the 'attachment' is in allowed list
                    compatibleSlot = _GetCompatibleSlot(compatibleAttachment);
                    if compatibleSlot == None:  # at this point _GetCompatibleSlot() must return an object, not None
                        exceptionDbgText = _FormatDbgText(gunId, gunName, compatibleAttachments, compatibleAttachment);
                        _Log(log, "Script aborted at: " + exceptionDbgText);
                        raise Exception(exceptionDbgText);
                    prevApCost = XmlUtils.GetTagValue(attachment, "APCost");
                    newApCost = compatibleSlot.attrib["timeAP"];
                    if prevApCost != newApCost:
                        XmlUtils.SetTagValue(attachment, "APCost", newApCost);  # then update APCost and leave it
                        _Log(log, "~  \'{}\' ({}) APCost: {} --> {}".format(attachmentName, attachmentId, prevApCost, newApCost));
                    compatibleAttachments.remove(compatibleAttachment);  # we don't need it anymore as there is no sence to put the same element into Attachments.xml more than once
                elif attachmentId not in ignoredAttList:  # otherwise remove it from Attachments.xml (if not an ignored attachment, of course)
                    _Log(log, "-  \'{}\' ({})".format(attachmentName, attachmentId));
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
                _Log(log, "+  \'{}\' ({})".format(attName, attId));
        
        _Log(log, "");  # append new line
    
    JA2TableData.GetWorkspace(JA2Workspaces.BRAINMOD).SaveXml(JA2Xmls.ATTACHMENTS);
    if itemsFileChanged:
        JA2TableData.GetWorkspace(JA2Workspaces.BRAINMOD).SaveXml(JA2Xmls.ITEMS);
    log.close();
#end def MakeRealisticAttachments(args):


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


def TestFunc(args):
    def _AllAreIgnored(attachments):
        result = True;
        ignoreList = ["1034", "1024", "1025"];
        for att in attachments:
            if att.text not in ignoreList:
                result = False;
                break;
        return result;
    
    itemsRoot = JA2TableData.GetXml(JA2Xmls.ITEMS);
    for item in itemsRoot:
        defaults = item.findall("DefaultAttachment");
        itemClass = XmlUtils.GetTagValue(item, "usItemClass");
        if len(defaults) > 0 and (itemClass == "2" or itemClass == "16"):
            if _AllAreIgnored(defaults) == True:
                continue;
            print("[{}] {}:".format(XmlUtils.GetTagValue(item, "uiIndex"), XmlUtils.GetTagValue(item, "szLongItemName")));
            for default in defaults:
                print("    [{}] \'{}\'".format(default.text, XmlUtils.GetTagValue(itemsRoot[int(default.text)], "szLongItemName")));
            print();
#end def TestFunc(args):

#
# Entry point (like Main())
#
JA2TableData.OpenWorkspace(JA2Workspaces.BRAINMOD);

cmd_map = { "PrintAttachmentItems" : PrintAttachmentItems, "PrintAttachmentInfo" : PrintAttachmentInfo,
            "GenGuns" : GenerateTemplateGunsXml, "GenAtts" : GenerateTemplateAttachmentsXml,
            "MakeRealisticAttachments" : MakeRealisticAttachments,
            "Test" : TestFunc, };
cmd_line = CmdLineProcessor(cmd_map);
cmd_line.Execute(sys.argv);
