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
    def RepresentsInt(s):
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
#end class XmlUtils():



#
# Entry point (like Main())
#

