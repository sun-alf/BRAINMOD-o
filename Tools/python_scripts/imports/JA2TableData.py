#### USAGE ####
# 0. Ensure you have !!! Python 3 !!! installed (version 3.x -- does not matter).
# 1. Import in your script:
#    from imports.JA2TableData import JA2TableData, JA2Workspaces, JA2Xmls;
#    from imports.xml_utils import XmlUtils;
# 2. Call JA2TableData.OpenWorkspace(), then get XML root by JA2TableData.GetXml().
# 3. Parse it using XmlUtils!


import os, sys;
import xml.etree.ElementTree as ET;
from imports.xml_manager import XmlManager;

#
# Script setup values
#
SWDIR = os.getcwd();


#
# Constants, functions, classes etc
#

class JA2Workspaces():
    VANILLA = 0;
    UB = 1;
    V113 = 2;
    AIMNAS = 3;
    BRAINMOD = 4;
#end class JA2Workspaces():


class JA2Xmls():
    # /Inventory
    ENEMY_AMMO_DROPS = "EnemyAmmoDrops.xml";
    ENEMY_ARMOR_DROPS = "EnemyArmourDrops.xml";
    ENEMY_EXPL_DROPS = "EnemyExplosiveDrops.xml";
    ENEMY_MISC_DROPS = "EnemyMiscDrops.xml";
    ENEMY_WEAPON_DROPS = "EnemyWeaponDrops.xml";
    
    ENEMY_GUN_CHOICES = "EnemyGunChoices.xml";
    ENEMY_ITEM_CHOICES = "EnemyItemChoices.xml";
    
    IMP_ITEM_CHOICES = "ImpItemChoices.xml";
    MERC_START_GEAR = "MercStartingGear.xml";
    
    GUNCH_ENEMY_ADMIN = "GunChoices_Enemy_Admin.xml";
    GUNCH_ENEMY_REGULAR = "GunChoices_Enemy_Regular.xml";
    GUNCH_ENEMY_ELITE = "GunChoices_Enemy_Elite.xml";
    GUNCH_MILITIA_GREEN = "GunChoices_Militia_Green.xml";
    GUNCH_MILITIA_REGULAR = "GunChoices_Militia_Regular.xml";
    GUNCH_MILITIA_ELITE = "GunChoices_Militia_Elite.xml";
    
    ITEMCH_ENEMY_ADMIN = "ItemChoices_Enemy_Admin.xml";
    ITEMCH_ENEMY_REGULAR = "ItemChoices_Enemy_Regular.xml";
    ITEMCH_ENEMY_ELITE = "ItemChoices_Enemy_Elite.xml";
    ITEMCH_MILITIA_GREEN = "ItemChoices_Militia_Green.xml";
    ITEMCH_MILITIA_REGULAR = "ItemChoices_Militia_Regular.xml";
    ITEMCH_MILITIA_ELITE = "ItemChoices_Militia_Elite.xml";
    
    # /Items
    AMMO_STRINGS = "AmmoStrings.xml";
    AMMO_TYPES = "AmmoTypes.xml";
    ARMORS = "Armours.xml";
    ATTACHMENT_COMBOS = "AttachmentComboMerges.xml";
    ATTACHMENT_INFO = "AttachmentInfo.xml";
    ATTACHMENTS = "Attachments.xml";
    ATTACHMENT_SLOTS = "AttachmentSlots.xml";
    INCOMPATIBLE_ATTACHMENTS = "IncompatibleAttachments.xml";
    CLOTHES = "Clothes.xml";
    COMPATIBLE_FACE_ITEMS = "CompatibleFaceItems.xml";
    DRUGS = "Drugs.xml";
    EXPLOSION_DATA = "ExplosionData.xml";
    EXPLOSIVES = "Explosives.xml";
    FOOD = "Food.xml";
    FOOD_OPINION = "FoodOpinion.xml";
    ITEM_TRANSFORMATIONS = "Item_Transformations.xml";
    ITEMS = "Items.xml";
    KEYS = "Keys.xml";
    LAUNCHABLES = "Launchables.xml";
    LBE = "LoadBearingEquipment.xml";
    LOCKS = "Locks.xml";
    MAGAZINES = "Magazines.xml";
    MERGES = "Merges.xml";
    POCKET_POPUPS = "PocketPopups.xml";
    POCKETS = "Pockets.xml";
    RANDOM_ITEM = "RandomItem.xml";
    STRUCTURE_CONSTRUCT = "StructureConstruct.xml";
    STRUCTURE_DECONSTRUCT = "StructureDeconstruct.xml";
    STRUCTURE_MOVE = "StructureMove.xml";
    WEAPONS = "Weapons.xml";
    
    # /LogicalBodyTypes
    LOBOT_FILTERS = "Filters.xml";
    
    # /Lookup
    LOOKUP_AMMO_CHOICES = "AmmoChoices.xml";
    LOOKUP_AMMO_FLAG = "AmmoFlag.xml";
    LOOKUP_ARMOR_CLASS = "ArmourClass.xml";
    LOOKUP_ATTACHMENT_CLASS = "AttachmentClass.xml";
    LOOKUP_ATTACHMENT_POINT  = "AttachmentPoint.xml";
    LOOKUP_ATTACHMENT_SYSTEM  = "AttachmentSystem.xml";
    LOOKUP_CURSOR = "Cursor.xml";
    LOOKUP_DRUG_TYPE = "DrugType.xml";
    LOOKUP_EXPL_SIZE = "ExplosionSize.xml";
    LOOKUP_EXPL_TYPE = "ExplosionType.xml";
    LOOKUP_ITEM_CLASS = "ItemClass.xml";
    LOOKUP_ITEM_FLAG = "ItemFlag.xml";
    LOOKUP_LBE_CLASS = "LBEClass.xml";
    LOOKUP_MAGAZINE_TYPE = "MagazineType.xml";
    LOOKUP_MERGE_TYPE = "MergeType.xml";
    LOOKUP_NAS_ATTACHMENT_CLASS = "NasAttachmentClass.xml";
    LOOKUP_NAS_LAYOUT_CLASS = "NasLayoutClass.xml";
    LOOKUP_POCKET_SIZE = "PocketSize.xml";
    LOOKUP_SEPARABILITY = "Separability.xml";
    LOOKUP_SILHOUETTE = "Silhouette.xml";
    LOOKUP_SKILL_CHECK_TYPE = "SkillCheckType.xml";
    LOOKUP_WEAPON_CLASS = "WeaponClass.xml";
    LOOKUP_WEAPON_TYPE = "WeaponType.xml";
    
    # /NPCInventory
    MERCHANTS = "Merchants.xml";
    DEALER_ADDITIONAL = "AdditionalDealer_{}_Inventory.xml";
    DEALER_ALBERTO = "AlbertoInventory.xml";
    DEALER_ARNIE = "ArnieInventory.xml";
    DEALER_CARLO = "CarloInventory.xml";
    DEALER_DEVIN = "DevinInventory.xml";
    DEALER_ELGIN = "ElginInventory.xml";
    DEALER_FRANK = "FrankInventory.xml";
    DEALER_FRANZ = "FranzInventory.xml";
    DEALER_FREDO = "FredoInventory.xml";
    DEALER_GABBY = "GabbyInventory.xml";
    DEALER_HERVE = "HerveInventory.xml";
    DEALER_HOWARD = "HowardInventory.xml";
    DEALER_JAKE = "JakeInventory.xml";
    DEALER_KEITH = "KeithInventory.xml";
    DEALER_MANNY = "MannyInventory.xml";
    DEALER_MICKEY = "MickeyInventory.xml";
    DEALER_PERKO = "PerkoInventory.xml";
    DEALER_PETER = "PeterInventory.xml";
    DEALER_SAM = "SamInventory.xml";
    DEALER_TINA = "TinaInventory.xml";
    DEALER_TONY = "TonyInventory.xml";
    
    __DEALER_ADDITIONAL_IDS = (1, 60);
    __DIRS = {
        "Inventory" : (
            ENEMY_AMMO_DROPS,
            ENEMY_ARMOR_DROPS,
            ENEMY_EXPL_DROPS,
            ENEMY_MISC_DROPS,
            ENEMY_WEAPON_DROPS,
            ENEMY_GUN_CHOICES,
            ENEMY_ITEM_CHOICES,
            IMP_ITEM_CHOICES,
            MERC_START_GEAR,
            GUNCH_ENEMY_ADMIN,
            GUNCH_ENEMY_REGULAR,
            GUNCH_ENEMY_ELITE,
            GUNCH_MILITIA_GREEN,
            GUNCH_MILITIA_REGULAR,
            GUNCH_MILITIA_ELITE,
            ITEMCH_ENEMY_ADMIN,
            ITEMCH_ENEMY_REGULAR,
            ITEMCH_ENEMY_ELITE,
            ITEMCH_MILITIA_GREEN,
            ITEMCH_MILITIA_REGULAR,
            ITEMCH_MILITIA_ELITE),
        "Items" : (
            AMMO_STRINGS,
            AMMO_TYPES,
            ARMORS,
            ATTACHMENT_COMBOS,
            ATTACHMENT_INFO,
            ATTACHMENTS,
            ATTACHMENT_SLOTS,
            INCOMPATIBLE_ATTACHMENTS,
            CLOTHES,
            COMPATIBLE_FACE_ITEMS,
            DRUGS,
            EXPLOSION_DATA,
            EXPLOSIVES,
            FOOD,
            FOOD_OPINION,
            ITEM_TRANSFORMATIONS,
            ITEMS,
            KEYS,
            LAUNCHABLES,
            LBE,
            LOCKS,
            MAGAZINES,
            MERGES,
            POCKET_POPUPS,
            POCKETS,
            RANDOM_ITEM,
            STRUCTURE_CONSTRUCT,
            STRUCTURE_DECONSTRUCT,
            STRUCTURE_MOVE,
            WEAPONS),
    };
    
    @classmethod
    def GetDirectoryOf(cls, filename):
        for key in cls.__DIRS:
            if filename in cls.__DIRS[key]:
                return key;
        return None;  # return nullptr instead of dir name in case of unknown filename
    
    @classmethod
    def IsValidDealerId(cls, i):
        return cls.__DEALER_ADDITIONAL_IDS[0] <= i and i <= cls.__DEALER_ADDITIONAL_IDS[1];
    
#end class JA2Xmls():


class Workspace():
    def __init__(self, name, dirname):
        self.name = str(name);
        self.dirname = dirname;
        self.root = r'{}\..\..\{}\TableData'.format(SWDIR, dirname);
        self.xmlMan = XmlManager();
    
    def IsItYou(self, name):
        strname = str(name);
        return self.name == strname;
    
    def GetXmlPath(self, name):
        dirname = JA2Xmls.GetDirectoryOf(name);
        return os.path.join(self.root, dirname);
    
    def GetXml(self, name, additionalDealerNum = None):
        path = self.GetXmlPath(name);
        if name == JA2Xmls.DEALER_ADDITIONAL and additionalDealerNum != None:
            if JA2Xmls.IsValidDealerId(additionalDealerNum):
                name = JA2Xmls.DEALER_ADDITIONAL.format(additionalDealerNum);
            else:
                raise Exception("Unknown Additional Dealer ID");
        return self.xmlMan.AddXml(path, name);
    
#end class Workspace():


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
#end class Singleton(type):


class JA2TableData(metaclass=Singleton):
    _workspacesList = [];
    
    @classmethod
    def OpenWorkspace(cls, name):
        dirname = None;
        if type(name) is str:
            raise Exception("Custom workspace name is not supported yet");
        elif type(name) is int:
            if name == JA2Workspaces.VANILLA:
                dirname = "Data";
            elif name == JA2Workspaces.UB:
                dirname = "Data-UB";
            elif name == JA2Workspaces.V113:
                dirname = "Data-1.13";
            elif name == JA2Workspaces.AIMNAS:
                dirname = "Data-AIMNAS";
            elif name == JA2Workspaces.BRAINMOD:
                dirname = "Data-BRAINMOD";
            else:
                pass;
        else:
            pass;
        
        if dirname != None:
            if cls.GetWorkspace(name) == None:  # if this workspace is not open yet, open it; nothing to do otherwise
                cls._workspacesList.append(Workspace(name, dirname));
        else:
            raise Exception("Unknown workspace \'{0}\'".format(name));
    #def OpenWorkspace(name):

    @classmethod
    def GetWorkspace(cls, name):
        for ws in cls._workspacesList:
            if ws.IsItYou(name):
                return ws;
        return None;
    #end def GetWorkspace(cls, name):
    
    @classmethod
    def GetXml(cls, name, dealerNum = None, wsName = None):
        result = None;
        ja2xmls = [getattr(JA2Xmls, field) for field in dir(JA2Xmls) if not callable(getattr(JA2Xmls, field)) and not field.startswith("__")];
        if name in ja2xmls:
            if len(cls._workspacesList) > 0:
                ws = cls._workspacesList[0];  # use default workspace
                if wsName != None:
                    ws = cls.GetWorkspace(wsName);
                    if ws == None:
                        raise Exception("Workspace \'{0}\' is not open".format(wsName));
                result = ws.GetXml(name, dealerNum);
            else:
                raise Exception("No workspace is open");
        else:
            raise Exception("Unknown file \'{0}\'".format(name));
        return result;
    #end def GetXml(cls, name, dealerNum = None, wsName = None):
#end class JA2TableData(metaclass=Singleton):


#
# Entry point (like Main())
#

