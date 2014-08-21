#encoding=utf8
import os, sys
from wx import *

#Maximum Number of Commands to Keep Track of in Prompt
MAX_PROMPT_COMMANDS = 25

#File Types
wildcard = u"ऋ कोड|*.rhee|All files (*)|*"

#Constant messages for file format checking.
FFMESSAGE = ["Unix Mode ('\\n')", "DOS/Windows Mode ('\\r\\n')", "Mac Mode ('\\r')"]

#Application ID Constants
ID_APP = 101
ID_NEW = 102
ID_OPEN = 103
ID_OPEN_RECENT = 104
ID_RELOAD = 105
ID_CLOSE = 106
ID_CLEAR_RECENT = 107
ID_SAVE = 108
ID_SAVE_AS = 109
ID_CLEAN_UP_TABS = 1010
ID_EXIT = 1014

ID_FORMATMENU = 2000
ID_UNIXMODE = 2001
ID_WINMODE = 2002
ID_MACMODE = 2003

ID_FIND = 111
ID_FIND_AGAIN = 112
ID_REPLACE = 113
ID_SWITCHEROO = 114
ID_GOTO = 115

ID_RUN = 121
ID_SET_ARGS = 122
ID_PYTHON = 123
ID_PYTHON_DEBUGGER = 124
ID_END = 125
ID_ADD_BREAKPOINT = 126
ID_REMOVE_BREAKPOINT = 127
ID_REMOVE_ALL_BREAKPOINTS = 128

ID_PREFS = 131
ID_TOGGLE_PROMPT = 132
ID_TOGGLE_VIEWWHITESPACE = 133
ID_CLEAR_PROMPT = 134
ID_COMMENT_REGION = 135
ID_UNCOMMENT_REGION = 136

ID_HELP = 141
ID_ABOUT = 142
ID_RECENT_FILES_BASE = 9930

#Style Constants
STYLE_DEFAULT = 1001

MARKER_BREAKPOINT = 1
MARKER_LINE = 4
#Font, System constants
#If homedirectory does not work correctly on your platform,
#comment it out, and set the variable to your homedirectory.
#pdbstring = sys.prefix + "/lib/python" + sys.version[:3] + "/pdb.py "
#This does not work on all platforms, especially if you fiddled with directory names.
#So, I will use the messier (but more accurate) method below:

#Just in case you don't check this code, and
#homedirectory does not work, drpython will plop
#its stuff in your root directory.
hdirbase = os.path.expanduser("~")
if (not os.path.exists(hdirbase)):
    if (Platform == '__WXMSW__'):
        try:
            hdirbase = os.environ["APPDATA"].replace("\\", "/") + "/"
        except:
            hdirbase = "c:/"
    else:
        hdirbase = "/"

if (Platform == '__WXMSW__'):
    pdbstring = sys.prefix.replace("\\", "/") + "/lib"
    pythexec = sys.prefix.replace("\\", "/") + "/python.exe"
    pythexecw = sys.prefix.replace("\\", "/") + "/pythonw.exe"
    homedirectory = os.path.expanduser("~").replace("\\", "/") + "/drpython"
else:
    pdbstring = sys.prefix + "/lib"
    pythexec = sys.executable
    homedirectory = os.path.expanduser("~") + "/.drpython"

if (os.path.exists(pdbstring + "/pdb.py")):
    pdbstring = pdbstring + "/pdb.py"
elif (os.path.exists(pdbstring + "/python" + sys.version[:3] + "/pdb.py")):
    pdbstring = pdbstring + "/python" + sys.version[:3] + "/pdb.py"
else:
    pdbstring = ""

#Thanks to Mark Rees.
#Thanks to Guillermo Fernandez.
programdirectory = os.path.dirname(os.path.abspath(sys.argv[0])) + "/"
bitmapdirectory = programdirectory + "bitmaps"

#*********************************************************************************************************************