#### USAGE ####
# 0. Ensure you have !!! Python 3 !!! installed (version 3.x -- does not matter).
# 1. Set environment variables if need:
#    set JA2_SRC_DIR -- set specific SRC_DIR. Check "Script setup values" below for details.
#    set JA2_TARGET_DIR -- set specific TARGET_DIR. Check "Script setup values" below for details.
# 2. There named arguments which can be used with any function:
#    src (or SRC_DIR) -- override SRC_DIR to specific one. It overrides env var JA2_SRC_DIR, if any.
#    target (or TARGET_DIR) -- override TARGET_DIR to specific one. It overrides env var JA2_TARGET_DIR, if any.
# 2. Available functions to execute:
#    CreatePatch -- create path (a bunch of files to override in your game dir). Possible arguments:
#        src_ts -- use "patch.timestamp" in SRC_DIR; timestamp in TARGET_DIR is used by default.
#    ApplyPatch -- copy and override patch files from SRC_DIR to TARGET_DIR (JA2 game dir). Possible arguments:
#        force -- ignore "patch.timestamp" in TARGET_DIR and copy all the files anyway.
# 3. Run this script (i.e. "game_updates.py") in a cmd line window using the following format:
#    >python game_updates.py FunctionName arg0 arg1 arg2 --src=C:\XXX ...
#        FunctionName -- mandatory, see available functions in step 1.
#        arg0 arg1... -- all arguments are non-mandatory in general, it depends on desired function to execute. 
#


import os, sys, time, datetime;
import shutil;
import re;
from imports.cmd_line import CmdLineProcessor;

#
# Script setup values:
# * SWDIR -- current working directory, obtained programmatically, no need to touch it.
# * SRC_DIR -- the script assumes it is being executed from "Tools\python_scripts\" dir under root dir of development game copy. It compares "last edit" timestamps of
#       files under this dir with timestamp of "patch.timestamp". If it is supposed to take the newest game files from elsewhere, SRC_DIR shall be overridden by env var
#       "SRC_DIR" or by cmd line argument #0
# * TARGET_DIR -- root dir to the patch dir; it will have exactly same dir/files tree as game root dir, so the patch can be applied by simple copying everything with "Replace all" option.
#
SWDIR = os.getcwd();
SRC_DIR = r'{}\..\..'.format(SWDIR);
TARGET_DIR = None;

#
# Constants, functions, classes etc
#
DEBUG_MODE = False;
PATCH_TIMESTAMP_FILENAME = "patch.timestamp";
PATCH_TIMESTAMP_FORMAT = "%Y %m %d, %H:%M:%S";
PATCH_TIMESTAMP_DIR = None;


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
    global PATCH_TIMESTAMP_DIR;
    fileFullName = os.path.join(PATCH_TIMESTAMP_DIR, PATCH_TIMESTAMP_FILENAME);
    file_ts = open(fileFullName, "w");
    file_ts.write(time.strftime(PATCH_TIMESTAMP_FORMAT));
    file_ts.close();
#end def CreatePatchTimestamp():


def ReadPatchTimestamp():
    global PATCH_TIMESTAMP_DIR;
    result = None;
    fileFullName = os.path.join(PATCH_TIMESTAMP_DIR, PATCH_TIMESTAMP_FILENAME);
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
        elif os.path.islink(objectPath):
            pass;  # nothing to do with symlinks to files
        else:
            print('Unknown file system object is found: %s' % (objectPath));
    return files_list;
#end def CollectUpdatedFiles(path, base_ts, files_list = None):


def CollectUpdatedFiles1(dest_path, src_path, ignore_ts, files_list = None, relative_path = ""):
    if files_list == None:
        files_list = [];
    
    for objectName in os.listdir(src_path):
        srcObjectPath = os.path.join(src_path, objectName);
        destObjectPath = os.path.join(dest_path, objectName);
        if os.path.isfile(srcObjectPath):
            srcTS = os.stat(srcObjectPath).st_mtime;
            destTS = 0;                                 # exact object (file/dir) may not be existing in dest dir;
            if os.path.exists(destObjectPath) == True:  # if it exists, get its' "modified" timestamp, or leave timestamp = 0 otherwise.
                destTS = os.stat(destObjectPath).st_mtime;
            if ignore_ts == True or destTS < srcTS:  # the file is updated, need to take in into account
                files_list.append(SEFile(objectName, src_path, relative_path));
        elif os.path.isdir(srcObjectPath):
            deeper_relative_path = os.path.join(relative_path, objectName);
            CollectUpdatedFiles1(destObjectPath, srcObjectPath, ignore_ts, files_list, deeper_relative_path);
        elif os.path.islink(srcObjectPath):
            pass;  # nothing to do with symlinks to files
        else:
            print('Unknown file system object is found: %s' % (srcObjectPath));
    return files_list;
#end def CollectUpdatedFiles1(dest_path, src_path, ignore_ts, files_list = None, relative_path = ""):


def EnsurePathExists(path):
    if os.path.exists(path) == False:
        dirChain = path.split(os.path.sep);
        walkPath = "";
        if path.startswith(os.path.sep):  # if it's a Linux absolute path (starts from FS root),
            walkPath = os.path.sep;       # return the root back as we just lost it by doing split().
        elif re.match("^[a-zA-Z]:", path):            # if it's a Windows absolute path (this piece of shit includes a drive letter),
            dirChain[0] = dirChain[0] + os.path.sep;  # append dir separator manually as os.path.join() doesn't do it.
        
        for dirName in dirChain:
            walkPath = os.path.join(walkPath, dirName);
            if os.path.exists(walkPath) == False:
                os.mkdir(walkPath);
#end def EnsurePathExists(path):


def CopyUpdatedFiles(dst_dir, files_list):
    for sef in files_list:
        if sef.IsInExclusions() == False:
            full_dst_path_dir = os.path.join(dst_dir, sef.rel_path);
            EnsurePathExists(full_dst_path_dir);
            shutil.copy2(sef.GetFullPath(), os.path.join(full_dst_path_dir, sef.name));
            print("Copied: {0}{1}{2}".format(sef.rel_path, os.path.sep, sef.name));
#end def CopyUpdatedFiles(dst_dir, files_list):


def ApplyNamedArguments(args):
    global SRC_DIR;
    global TARGET_DIR;
    
    simpleArgs = [];
    for arg in args:
        if CmdLineProcessor.RepresentsNamedArg(arg):
            if arg["name"] == "src" or arg["name"] == "SRC_DIR":
                SRC_DIR = arg["value"];
            elif arg["name"] == "target" or arg["name"] == "TARGET_DIR":
                TARGET_DIR = arg["value"];
        else:
            simpleArgs.append(arg);
    print("SRC_DIR = {}".format(SRC_DIR));
    print("TARGET_DIR = {}".format(TARGET_DIR));
    return simpleArgs;
#end def ApplyNamedArguments(args):


def CreateGamePatch(args):
    global PATCH_TIMESTAMP_DIR;
    
    simpleArgs = ApplyNamedArguments(args);
    if "src_ts" in simpleArgs:
        PATCH_TIMESTAMP_DIR = SRC_DIR;
    else:
        PATCH_TIMESTAMP_DIR = TARGET_DIR;
    
    # 1. Read TS of previous patch (if any). The TS is base time to compare files' timestamps with:
    #    all files newer than this should be copied to the patch dir. If there is no previous patch, timestamp file
    #    should be provided anyway (see error message below).
    patchBaseTS = ReadPatchTimestamp();
    if patchBaseTS == None:
        print("Timestamp file does not exist, so patch cannot be created!");
        print("Example timestamp file ({0}) is just created at ({2}):\n    {1}".format(PATCH_TIMESTAMP_FILENAME, PATCH_TIMESTAMP_DIR, "SRC_DIR" if "src_ts" in simpleArgs else "TARGET_DIR"));
        print("Please edit it appropriately and run the script again.");
        CreatePatchTimestamp();
        quit();  # Exit the program
    print("Patch base timestamp: " + time.strftime(PATCH_TIMESTAMP_FORMAT, patchBaseTS));
    patchBaseTS = FullTimestamp(patchBaseTS);

    # 2. Clean-up the patch dir.
    CleanupDir(TARGET_DIR);

    # 3. Walk across everything in SRC_DIR (JA2 root path) and copy all new stuff to TARGET_DIR keeping dir structure.
    #    Basically both SRC_DIR and TARGET_DIR must have the same structure.
    filesList = CollectUpdatedFiles(SRC_DIR, patchBaseTS);
    CopyUpdatedFiles(TARGET_DIR, filesList);
    
    # 4. If we are at this point, it is most likely everything is done successfully. Now create new patch timestamp,
    #    so that next time patch files will be collected from this point of time.
    CreatePatchTimestamp();
#end def CreateGamePatch():


def ApplyGamePatch(args):
    simpleArgs = ApplyNamedArguments(args);
    if "force" in simpleArgs:
        byForce = True;
    else:
        byForce = False;

    # 1. Walk across everything in SRC_DIR (must be patch dir) and collect all modified files (i.e. "modified" timestamp of a patched file > 
    #    "modified" timestamp of a current game file). Here we need to use overloaded CollectUpdatedFiles(path, path, flag) function.
    filesList = CollectUpdatedFiles1(TARGET_DIR, SRC_DIR, byForce);
    
    # 2. Now copy the collected list of modified (i.e. patched) files, that's simple.
    CopyUpdatedFiles(TARGET_DIR, filesList);
#end def ApplyGamePatch():


def Fun1(args):
    print("Task: create dir ", args[0]);
    #EnsurePathExists(args[0])
    path = args[0];
    if os.path.exists(path) == False:
        print("does not exist");
        dirChain = path.split(os.path.sep);
        print("dirChain: ", dirChain);
        walkPath = "";
        if path.startswith(os.path.sep):  # if it's a Linux absolute path (starts from FS root),
            walkPath = os.path.sep;       # return the root back as we just lost it by doing split().
        elif re.match("^[a-zA-Z]:", path):            # if it's a Windows absolute path (this piece of shit includes a drive letter),
            dirChain[0] = dirChain[0] + os.path.sep;  # append dir separator manually as os.path.join() doesn't do it.
            
        for dirName in dirChain:
            walkPath = os.path.join(walkPath, dirName);
            if os.path.exists(walkPath) == False:
                print("part \'{0}\' does not exist".format(walkPath));
                os.mkdir(walkPath);
            else:
                print("part \'{0}\' exists".format(walkPath));
    else:
        print("already exists");

#
# Entry point, like Main() is
#
env_SRC_DIR = os.getenv('JA2_SRC_DIR');
env_TARGET_DIR = os.getenv('JA2_TARGET_DIR');
if env_SRC_DIR != None:
    SRC_DIR = env_SRC_DIR;
if env_TARGET_DIR != None:
    TARGET_DIR = env_TARGET_DIR;

cmd_map = {"CreatePatch" : CreateGamePatch, "ApplyPatch" : ApplyGamePatch, "Fun1" : Fun1};
cmd_line = CmdLineProcessor(cmd_map);
cmd_line.Execute(sys.argv);
print("Done!");
