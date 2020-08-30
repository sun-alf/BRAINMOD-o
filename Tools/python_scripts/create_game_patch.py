import os, sys, time, datetime
import shutil
import xml.etree.ElementTree as ET;

#
# Script setup values:
# * INPUT_DIR -- the script assumes it is being executed from "Tools\python_scripts\" dir under game root dir, so we don't point INPUT_DIR explicitly.
# * OUTPUT_DIR -- root dir to the patch dir; it will have exactly same dir/files tree as game root dir, so the patch can be applied by simple copying everything with "Replace all" option.
#
INPUT_DIR = r'D:\Programs\JaggedAlliance2';
OUTPUT_DIR = r'E:\Prepare\ja2_BRAINMOD_updates';
PATCH_TIMESTAMP_FILENAME = "patch.timestamp";
PATCH_TIMESTAMP_FORMAT = "%Y %m %d, %H:%M:%S";


#
# Constants, functions, classes etc
#
DEBUG_MODE = False;


class FullTimestamp():
    def __init__(self, struct_time_obj):        
        self.utc_ts = time.mktime(struct_time_obj);
        self.struct_time = struct_time_obj;

    def IsOlderThan(self, ts):
        if self.utc_ts < ts:
            return True;
        else:
            return False;
#end class FullTimestamp(time.struct_time):


class SEFile:  # Self-explanatory file
    def __init__(self, fname, fpath, rpath):        
        self.name = fname;
        self.path = fpath;
        self.rel_path = rpath;
        self.pathchain = [];

    def GetFullPath(self):
        return os.path.join(self.path, self.name);

    def IsInExclusions(self):
        if self.name[len(self.name) - 4:] == ".log":
            return True;
        if self.rel_path[:8] == "Profiles":
            return True;
        if self.rel_path[:5] == "Tools":
            return True;
        return False;
#end class SEFile:


def CreatePatchTimestamp():
    fileFullName = os.path.join(OUTPUT_DIR, PATCH_TIMESTAMP_FILENAME);
    file_ts = open(fileFullName, "w");
    file_ts.write(time.strftime(PATCH_TIMESTAMP_FORMAT));
    file_ts.close();
#end def CreatePatchTimestamp():


def ReadPatchTimestamp():
    result = None;
    fileFullName = os.path.join(OUTPUT_DIR, PATCH_TIMESTAMP_FILENAME);
    if os.path.exists(fileFullName):
        file_ts = open(fileFullName, "r");
        text = file_ts.read();
        print("text: " + text);
        result = time.strptime(text, PATCH_TIMESTAMP_FORMAT);
        file_ts.close();
    return result;
#end def ReadPatchTimestamp():


def CleanupDir(path_to_folder):
    for filename in os.listdir(path_to_folder):
        file_path = os.path.join(path_to_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
#end def CleanupDir(path_to_folder):


def CollectUpdatedFiles(path, base_ts, files_list = None, relative_path = ""):
    if files_list == None:
        files_list = [];
    
    for objectName in os.listdir(path):
        objectPath = os.path.join(path, objectName);
        if os.path.isfile(objectPath):
            mod_ts = os.stat(objectPath).st_mtime;
            if base_ts.IsOlderThan(mod_ts):  # the file is updated, need to take in into account
                files_list.append(SEFile(objectName, path, relative_path));
        elif os.path.isdir(objectPath):
            deeper_relative_path = os.path.join(relative_path, objectName);
            CollectUpdatedFiles(objectPath, base_ts, files_list, deeper_relative_path);
        else:
            print('Bullshit found: %s' % (objectPath));
    return files_list;
#end def CollectUpdatedFiles(path, base_ts, files_list = None):


def EnsurePathExists(path):
    if os.path.exists(path) == False:
        dirChain = path.split(os.path.sep);
        walkPath = "";
        for dirName in dirChain:
            walkPath = os.path.join(walkPath, dirName);
            if os.path.exists(walkPath) == False:
                os.mkdir(walkPath);
#end def EnsurePathExists(path):


def CopyUpdatedFiles(dst_dir, files_list):
    for sef in filesList:
        if sef.IsInExclusions() == False:
            full_dst_path_dir = os.path.join(dst_dir, sef.rel_path);
            EnsurePathExists(full_dst_path_dir);
            shutil.copy2(sef.GetFullPath(), os.path.join(full_dst_path_dir, sef.name));
            print("Copied: {0}{1}{2}".format(sef.rel_path, os.path.sep, sef.name));
#end def CopyUpdatedFiles(dst_dir, files_list):


#
# Entry point, like Main() is
#

# 1. Read TS of previous patch (if any). The TS is base time to compare files' timestamps with:
#    all files newer than this should be copied to the patch dir. If there is no previous patch, timestamp file
#    should be provided anyway (see error message below).
patchBaseTS = ReadPatchTimestamp();
if patchBaseTS == None:
    print("Timestamp file does not exist, so patch cannot be created!");
    print("Example timestamp file ({0}) is just created at:\n    {1}".format(PATCH_TIMESTAMP_FILENAME, OUTPUT_DIR));
    print("Please edit it appropriately and run the script again.");
    CreatePatchTimestamp();
    quit();  # Exit the program
print("Patch base timestamp: " + time.strftime(PATCH_TIMESTAMP_FORMAT, patchBaseTS));
patchBaseTS = FullTimestamp(patchBaseTS);

# 2. Clean-up the patch dir. Then create new patch timestamp.
CleanupDir(OUTPUT_DIR);
CreatePatchTimestamp();

# 3. Walk across everything in INPUT_DIR (JA2 root path) and copy all new stuff to OUTPUT_DIR keeping dir structure.
#    Basically both INPUT_DIR and OUTPUT_DIR must have the same structure.
filesList = CollectUpdatedFiles(INPUT_DIR, patchBaseTS);
CopyUpdatedFiles(OUTPUT_DIR, filesList);
