#### USAGE ####
# 0. Ensure you have !!! Python 3 !!! installed (version 3.x -- does not matter).
# 1. import in your script:
#    from imports.cmd_line import CmdLineProcessor;


import os, sys, time, datetime;
import shutil;


#
# Constants, functions, classes etc
#

class CmdLineProcessor():
    def __init__(self, cmdMap):
        self._cmdMap = cmdMap;
    
    def Execute(self, argv, isFromCmdLine = True):
        result = None;
        cmdFunc = None;
        args = [];
        startArg = 1 if isFromCmdLine == True else 0;  # argv origins from command line, argv[0] is always path/name to the file being executed. In this case we have to skip it.
        for i in range(startArg, len(argv)):
            if i == startArg and argv[i] in self._cmdMap:
                cmdFunc = self._cmdMap[argv[i]];
            else:  # parse an argument
                argVal = 0;
                
                if CmdLineProcessor.RepresentsInt(argv[i]):
                    argVal = int(argv[i]);
                elif CmdLineProcessor.RepresentsNamedArg(argv[i]):
                    argVal = CmdLineProcessor.GetNamedArg(argv[i]);
                else:
                    argVal = argv[i];  # add this arg as a string
                
                args.append(argVal);

        if cmdFunc != None:
            result = cmdFunc(args);
        else:
            print("Invalid input.");
            print("Valid input format: function_name arg0 arg1=a arg2=b arg3 ...");
            print("Valid functions: {}".format(list(self._cmdMap.keys())));
        
        return result;
    #end def Execute(self, argv):
    
    def ExecuteInteractively(self, argv):
        if argv != None and len(argv) > 1: 
            self.Execute(argv);
        cmd = "";
        while cmd != "quit" and cmd != "q":
            print("Enter command (\"quit\" or \"q\" for exit):");
            cmd = input();
            if cmd == "quit" or cmd == "q":
                break;
            cmd = cmd.split(' ');
            self.Execute(cmd, False);
    
    @classmethod
    def RepresentsInt(cls, s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
    #def RepresentsInt(s):

    @classmethod
    def RepresentsFloat(cls, s):
        try: 
            float(s)
            return True
        except ValueError:
            return False
    #def RepresentsFloat(s):

    @classmethod
    def GetNamedArg(cls, s):
        result = None;
        if s.find("--") == 0:  # if starts with "--", i.e. "--my_arg=value".
            s = s[2:];  # trim that "--", now have "my_arg=value"
            pair = s.split('=');
            if len(pair) == 2:
                result = {"name" : pair[0], "value" : pair[1]};
            elif len(pair) == 1:
                result = {"name" : pair[0]};
        return result;
    #def GetNamedArg(s):

    @classmethod
    def RepresentsNamedArg(cls, s):
        result = False;
        if type(s) == dict and len(s) == 2 and "name" in s.keys() and "value" in s.keys():
            result = True;
        elif type(s) == str:
            result = CmdLineProcessor.GetNamedArg(s) != None;
        return result;
    #def RepresentsNamedArg(s):

    @classmethod
    def FetchNamedArgs(cls, args):
        result = [];
        for arg in args:
            if CmdLineProcessor.RepresentsNamedArg(arg):
                result.append(arg);
        return result;
    #def FetchNamedArgs(cls, args):

    @classmethod
    def FetchSimpleArgs(cls, args):
        result = [];
        for arg in args:
            if CmdLineProcessor.RepresentsNamedArg(arg) == False:
                result.append(arg);
        return result;
    #def FetchSimpleArgs(s):

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
#end class CmdLineProcessor():
