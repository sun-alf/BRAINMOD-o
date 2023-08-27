#### USAGE ####
# 0. Ensure you have !!! Python 3 !!! installed (version 3.x -- does not matter).
# 1. import in your script:
#    from imports.xml_utils import XmlUtils;


import os, sys;
import xml.etree.ElementTree as ET;


#
# Constants, functions, classes etc
#

class XmlUtils():
    @classmethod
    def RepresentsInt(cls, s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
    #def RepresentsInt(s):

    @classmethod
    def GetTagValue(cls, item, tagName):
        for tagObj in item:
            if tagObj.tag == tagName:
                return tagObj.text;
        return None;
    #end def GetTagValue(item, tagName):
    
    @classmethod
    def SetTagValue(cls, item, tagName, tagValue):
        for tagObj in item:
            if tagObj.tag == tagName:
                tagObj.text = tagValue;
                return True;
        return False;
    #end def SetTagValue(item, tagName, tagValue):
    
    @classmethod
    def LoadToList(cls, root):
        result = [];
        for xmlEl in root:
            el = dict();
            for tagObj in xmlEl:
                el[tagObj.tag] = tagObj.text;
            result.append(el);
        return result;
    #end def LoadToList(cls, root):
    
    @classmethod
    def SanitizeString(cls, text):
        text = text.replace("&", "&amp;");
        text = text.replace("\"", "&quot;");
        return text.strip();
    #end def GetTagValue(item, tagName):
#end class XmlUtils():
