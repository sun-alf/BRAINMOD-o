import xml.etree.ElementTree as ET;

#
# Script setup values
#
SOURCE_ITEMS_XML = r'D:\Programs\JaggedAlliance2\Data-AIM\TableData\Items\Items.xml';
SOURCE_MERGES_XML = r'D:\Programs\JaggedAlliance2\Data-AIM\TableData\Items\Merges.xml';
SOURCE_ATTACHMENTS_XML = r'D:\Programs\JaggedAlliance2\Data-AIM\TableData\Items\Attachments.xml';
OUTPUT_FILE_CSV = r'D:\recipes.csv';


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
#end class Item:


class Merge:
    #name = "";
    isValid = False;
    item1 = None;
    item2 = None;
    result1 = None;
    result2 = None;
    
    def __init__(self, item1_id, item2_id, result1_id, result2_id, items):        
        if item1_id > 0 and item2_id > 0 and result1_id > 0:
            self.item1 = items[item1_id];
            self.item2 = items[item2_id];
            self.result1 = items[result1_id];
            if result2_id > 0:
                self.result2 = items[result2_id];
            self.isValid = True;

    def TryToString(self, id_list, items):
        result = "";
        for _id in id_list:
            if _id > 0:
                result += items[_id].name + "  ";
        return result;
        
    def ToCsvString(self):
        result = str(self.result1.id_) + CSV_SEPARATOR + ToAggregatedString(self.result1.name);
        if self.result2 != None:
            result += " + " + ToAggregatedString(self.result2.name);
        result += CSV_SEPARATOR + ToAggregatedString(self.item1.name) + " + " + ToAggregatedString(self.item2.name) + '\n';
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


def GenMergeObjects(root, items):
    result = [];
    for merge in root:
        item1_id = -1;
        item2_id = -1;
        result1_id = -1;
        result2_id = -1;
        for prop in merge:
            if prop.tag == "firstItemIndex":
                item1_id = int(prop.text);
            if prop.tag == "secondItemIndex":
                item2_id = int(prop.text);
            if prop.tag == "firstResultingItemIndex":
                result1_id = int(prop.text);
            if prop.tag == "secondResultingItemIndex":
                result2_id = int(prop.text);
        
        mergeObj = Merge(item1_id, item2_id, result1_id, result2_id, items);
        if mergeObj.isValid:
            result.append(mergeObj);
        else:
            id_list = [item1_id, item2_id, result1_id, result2_id];
            print("Skip invalid merge: " + str(id_list));
            if DEBUG_MODE:
                print("    " + mergeObj.TryToString(id_list, items));
    #end for merge in root:
    return result;
#end def GenMergeObjects(root, items):


def ValidateItemsList(items):
    for i in range(len(items)):
        if items[i].id_ != i:
            return False;

    return True;
#end def ValidateItemsList(items):


def GenRecipes(items, merges):
    # I threw away idea of a full roadmap until I have any idea on how to represent it in a handy way
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


#
# Entry point, like Main()
#
treeAtt = ET.parse(SOURCE_ATTACHMENTS_XML);
#treeItems = ET.parse(SOURCE_ITEMS_XML);
rootAtt = treeAtt.getroot();
#rootItems = treeItems.getroot();

cnt = 0;
for att in rootAtt:
    cnt += 1;
#end for item in root:

print("Count of att: ", cnt);

