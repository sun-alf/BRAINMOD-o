#### USAGE ####
# 0. Ensure you have !!! Python 3 !!! installed (version 3.x -- does not matter).
# 1. import in your script:
#    from imports.xml_manager import XmlManager;


import os, sys;
import xml.etree.ElementTree as ET;


#
# Constants, functions, classes etc
#

class XmlFile():
    def __init__(self, filePath, fileName, newFilePath = None, newFileName = None):
        self._filePath = filePath;
        self._fileName = fileName;
        self._newFilePath = newFilePath;
        self._newFileName = newFileName;
        self._xmlTree = None;
        self._dirty = False;

    @property
    def Path(self):
        return self._filePath;

    @property
    def Name(self):
        return self._fileName;

    @property
    def NewPath(self):
        return self._newFilePath;
    @NewPath.setter
    def NewPath(self, value):
        self._newFilePath = value;
    
    @property
    def NewName(self):
        return self._newFileName;
    @NewName.setter
    def NewName(self, value):
        self._newFileName = value;
        
    @property
    def TreeRoot(self):
        if self._xmlTree == None:
            self._xmlTree = ET.parse(os.path.join(self._filePath, self._fileName));
        return self._xmlTree.getroot();
    
    @property
    def Dirty(self):
        return self._dirty;
    @Dirty.setter
    def Dirty(self, value):
        self._dirty = value if type(value) == bool else True;
    
    def Save(self, newFilePath = None, newFileName = None):
        if newFilePath != None:
            self.NewPath = newFilePath;
        if newFileName != None:
            self.NewName = newFileName;
        
        result = self._dirty;
        if self._dirty:
            filePath = self._newFilePath if self._newFilePath != None else self._filePath;
            fileName = self._newFileName if self._newFileName != None else self._fileName;
            fullpath = os.path.join(filePath, fileName);
            if not os.path.exists(filePath):
                os.makedirs(filePath);
            
            f = open(fullpath, "wb");
            f.write(bytearray(r'<?xml version="1.0" encoding="utf-8"?>' + '\n', "utf-8"));
            self.xmlTree.write(f, encoding="utf-8", xml_declaration=None, default_namespace=None, method="xml");
            f.close();
            
            self.dirty = False;  # starting from this point, it should work with newly saved XML data (see 'fullpath')
            self._xmlTree = None;
            self._filePath = filePath;
            self._fileName = fileName;
            self._newFilePath = None;
            self._newFileName = None;
            
        return result;
#end class XmlFile():


class XmlManager():
    def __init__(self):
        self._fileList = [];

    def AddXml(self, filePath, fileName, newFilePath = None, newFileName = None):
        xmlRoot = self.GetXml(filePath, fileName);  # try to find among opened items first
        if xmlRoot == None:  # if this file is not open yet, open it
            newXml = XmlFile(filePath, fileName, newFilePath, newFileName);
            self._fileList.append(newXml);
            xmlRoot = newXml.TreeRoot;
        return xmlRoot;

    def GetXml(self, filePath, fileName):
        targetXml = None;
        for xml in self._fileList:
            if xml.Name == fileName and xml.Path == filePath:
                targetXml = xml.TreeRoot;
                break;
        
        return targetXml;
        
    def SaveAll(self):
        for xml in self._fileList:
            xml.Save();

#end class XmlManager():
