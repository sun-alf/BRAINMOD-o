#### USAGE ####
# 0. Ensure you have !!! Python 3 !!! installed (version 3.x -- does not matter).
# 1. Run this script (i.e. "gen_crafting_roadmap.py") in a cmd line window with the following arguments format:
#    gen_crafting_roadmap.py  <cmd>  <arg1>  <arg2> ...
#    <cmd>  :
#      csv - generate CSV file.
#      txt - generate TXT file.
# 


import os, sys;
import xml.etree.ElementTree as ET;

#
# Script setup values
#
SWDIR = os.getcwd();
TABLE_DATA_ROOT = r'{}\..\..\Data-BRAINMOD\TableData'.format(SWDIR);
SOURCE_ITEMS_XML = r'{}\Items\Items.xml'.format(TABLE_DATA_ROOT);
SOURCE_MERGES_XML = r'{}\Items\Merges.xml'.format(TABLE_DATA_ROOT);
SOURCE_ATTACH_MERGES_XML = r'{}\Items\AttachmentComboMerges.xml'.format(TABLE_DATA_ROOT);
OUTPUT_FILE_CSV = r'C:\Temp\recipes.csv';
OUTPUT_FILE_TXT = r'C:\Temp\recipes.txt';


#
# Constants, functions, classes etc
#
DEBUG_MODE = False;
CSV_SEPARATOR = ';';
CSV_AGGREGATOR = '\"';


def ToAggregatedString(s):
    if s.find(CSV_SEPARATOR) != -1:
        return CSV_AGGREGATOR + str(s) + CSV_AGGREGATOR;  # enquote (aggregate)
    else:
        return str(s);  # no need to aggregate
#end def ToAggregatedString(s):


class Item:
    name = "";
    id_ = -1;
    
    def __init__(self):
        pass;
    
#    def __init__(self, arg_id, arg_name):
#        self.id_ = arg_id;
#        self.name = arg_name;
#end class Item:


class MergeType:
    SIMPLE = 0;  # this merge is an usual merging of two same consumables (some kit + some kit, some drink + some drink, etc)
    MERGE  = 1;
    COMBO  = 2;  # attachment combo merge
#end class MergeType:


class Merge:
    #name = "";
    isValid = False;
    mergeType = None;
    item1 = None;
    item2 = None;
    result1 = None;
    result2 = None;
    
    def __init__(self, item1_id, item2_id, result1_id, result2_id, items):
        if type(item2_id) == int:
            self.mergeType = MergeType.MERGE;
            if item1_id == item2_id and result1_id == item1_id and result2_id == 0:  # check for simple merge
                self.mergeType = MergeType.SIMPLE;
            elif item1_id > 0 and item2_id > 0 and result1_id > 0:
                self.item1 = items[item1_id];
                self.item2 = items[item2_id];
                self.result1 = items[result1_id];
                if result2_id > 0:
                    self.result2 = items[result2_id];
                self.isValid = True;

        elif type(item2_id) == list:
            att_ids = item2_id;  # just rename it as this arg is a list actually
            self.mergeType = MergeType.COMBO;
            if item1_id > 0 and len(att_ids) > 0 and result1_id > 0:
                self.item1 = items[item1_id];
                self.result1 = items[result1_id];
                self.item2 = [];
                for att_id in att_ids:
                    if att_id > 0:
                        self.item2.append(items[att_id]);
                self.isValid = len(self.item2) > 0;

    def TryToString(self, id_list, items):
        result = "";
        for _id in id_list:
            if _id > 0:
                result += items[_id].name + "  ";
        return result;
        
    def ToCsvString(self):
        result = str(self.result1.id_) + CSV_SEPARATOR + ToAggregatedString(self.result1.name);
        if self.mergeType == MergeType.MERGE:
            if self.result2 != None:
                result += " + " + ToAggregatedString(self.result2.name);
            result += CSV_SEPARATOR + ToAggregatedString(self.item1.name) + " + " + ToAggregatedString(self.item2.name) + '\n';
        else:  # attachment combo merge
            result += CSV_SEPARATOR + ToAggregatedString(self.item1.name);
            for item in self.item2:
                result += " + " + ToAggregatedString(item.name);
            result += '\n';
        return result;

    # Should output a line in the following format (considering tab == 4 spaces):
    # "Name (id)\t\t= [Ingredient1 + Ingredient2 + ...]  // 2nd out Name (id)\n"
    def ToTxtString(self, dbg):
        result = self.result1.name;
        if dbg:
            result = "{} ({})".format(self.result1.name, self.result1.id_);
        
        tableHeader1stColumnLength = len("Name (id)") + 8;  # +2 tabs
        if len(result) < tableHeader1stColumnLength:
            diff = tableHeader1stColumnLength - len(result);
            if diff > 4:
                result += "\t\t";
            else:
                result += "\t";
        
        recipe_format = "{}= [{}]";  # Name = [ingredients]
        ingredients_str = "";
        
        if self.mergeType == MergeType.MERGE:
            ingredients_format = "{0}  +  {2}";
            if dbg:
                ingredients_format = "{0} ({1}) + {2} ({3})";
            ingredients_str = ingredients_format.format(self.item1.name, self.item1.id_, self.item2.name, self.item2.id_);
        else:
            ingredients_str += self.item1.name;
            if dbg:
                ingredients_str += ' (' + str(self.item1.id_) + ')';
            for item in self.item2:
                ingredients_str += " + " + item.name;
                if dbg:
                    ingredients_str += ' (' + str(item.id_) + ')';
        
        result2_format = "{0}  // {1}";
        if dbg:
            result2_format = "{0}  // {1} ({2})";
        
        result = recipe_format.format(result, ingredients_str);
        if self.result2 != None:
            result = result2_format.format(result, self.result2.name, self.result2.id_);
        
        result += "\n";
        return result;
#end class Merge:


def GenItemObjects(root):
    result = [];
    for item in root:
        itemObj = Item();
        for prop in item:
            if prop.tag == "uiIndex":
                itemObj.id_ = int(prop.text);
            if prop.tag == "szLongItemName":
                itemObj.name = prop.text;
        
        result.append(itemObj);
    #end for item in root:
    return result;
#end def GenItemObjects(root):


def GenMergeObjects(rootMerges, rootCombos, items):
    result = [];
    
    for merge in rootMerges:
        break;  #TEMP:
        item1_id = -1;
        item2_id = -1;
        result1_id = -1;
        result2_id = -1;
        for prop in merge:
            if prop.tag == "firstItemIndex":
                item1_id = int(prop.text);
            elif prop.tag == "secondItemIndex":
                item2_id = int(prop.text);
            elif prop.tag == "firstResultingItemIndex":
                result1_id = int(prop.text);
            elif prop.tag == "secondResultingItemIndex":
                result2_id = int(prop.text);
        
        mergeObj = Merge(item1_id, item2_id, result1_id, result2_id, items);
        if mergeObj.isValid:
            result.append(mergeObj);
        elif mergeObj.mergeType != MergeType.SIMPLE:
            id_list = [item1_id, item2_id, result1_id, result2_id];
            print("Skip invalid merge: " + str(id_list));
            if DEBUG_MODE:
                print("    " + mergeObj.TryToString(id_list, items));
    #end for merge in rootMerges:
    
    for combo in rootCombos:
        item_id = -1;  # tag <usItem>
        attachment_ids = [];
        result_id = -1;  # tag <usResult>
        for prop in combo:
            if prop.tag == "usItem":
                item_id = int(prop.text);
            elif prop.tag == "usResult":
                result_id = int(prop.text);
            elif prop.tag.find("usAttachment") != -1:
                attachment_ids.append(int(prop.text));
        
        mergeObj = Merge(item_id, attachment_ids, result_id, None, items);
        if mergeObj.isValid:
            result.append(mergeObj);
        elif mergeObj.mergeType != MergeType.SIMPLE:
            id_list = [item1_id, item2_id, result1_id, result2_id];
            print("Skip invalid merge: " + str(id_list));
            if DEBUG_MODE:
                print("    " + mergeObj.TryToString(id_list, items));
    #end for combo in rootCombos:
    
    return result;
#end def GenMergeObjects(rootMerges, items):


def ValidateItemsList(items):
    for i in range(len(items)):
        if items[i].id_ != i:
            return False;

    return True;
#end def ValidateItemsList(items):


def GenRecipes(items, merges):
    # I threw away idea of a full roadmap until I have any idea on how to represent it in a handy way.
    # For now, just sort list of merges by result1 item id:
    merges.sort(key = lambda x: x.result1.id_);
    return merges;
#end def GenRecipes(items, merges):


def GenCsvFile(recipes, fname):
    file_recipes = open(fname, "w");
    file_recipes.write("Index" + CSV_SEPARATOR + "Name" + CSV_SEPARATOR + "Ingredients\n");
    
    for recipe in recipes:
        file_recipes.write(recipe.ToCsvString());
    
    file_recipes.close();
    return True;
#end def GenCsvFile(recipes, fname):


def GenTxtFile(recipes, fname, dbg):
    file_recipes = open(fname, "w");
    file_recipes.write("Name (id)\t\t= [Ingredients]  // 2nd out Name (id)\n");
    
    for recipe in recipes:
        file_recipes.write(recipe.ToTxtString(dbg));
    
    file_recipes.close();
    return True;
#end def GenTxtFile(recipes, fname, dbg):


#
# Entry point, like Main()
#
treeMerges = ET.parse(SOURCE_MERGES_XML);
treeItems = ET.parse(SOURCE_ITEMS_XML);
treeCombos = ET.parse(SOURCE_ATTACH_MERGES_XML);
rootMerges = treeMerges.getroot();
rootItems = treeItems.getroot();
rootCombos = treeCombos.getroot();

items = GenItemObjects(rootItems);
if ValidateItemsList(items):
    merges = GenMergeObjects(rootMerges, rootCombos, items);
    recipes = GenRecipes(items, merges);
    if (len(sys.argv) > 1) and (sys.argv[1] == "csv"):
        GenCsvFile(recipes, OUTPUT_FILE_CSV);
    else:
        dbg = False;
        if (len(sys.argv) > 2) and (sys.argv[2] == "dbg"):
            dbg = True;
        GenTxtFile(recipes, OUTPUT_FILE_TXT, dbg);
else:
    print("Bad indices in Items list");
