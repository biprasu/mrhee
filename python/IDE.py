#encoding=UTF8
#!/bin/env python

# import inspect
# import sys, os, os.path

# from wx.stc import *

# import Prefs
# import About
# import Help


from RheeVariables import *


#*********************************************************************************************************************
#Utility function for Call Tips

def GetRightMostText(lineoftext):
    x = len(lineoftext) - 1
    start = -1
    end = -1
    while (x >= 0):
        if (not lineoftext[x].isspace()) and (end == -1):
            end = x + 1
        if lineoftext[x].isspace() and (not end == -1):
            start = x + 1
            x = 0
        x = x - 1
    if end == -1:
        return None
    if start == -1:
        start = 0
    return lineoftext[start:end]

#*********************************************************************************************************************



#*********************************************************************************************************************


#*********************************************************************************************************************

from GUI.RheeFrame import RheeFrame

#*********************************************************************************************************************

class RheeApp(App):
    def OnInit(self):

        frame = RheeFrame(None, ID_APP, u"ऋ - नया फाइल")

        frame.Show(True)

        self.SetTopWindow(frame)

        return True

# Set the dot path here... if set in system path, then it is unnecessary.
import os
os.environ["PATH"] += r";C:\Program Files (x86)\Graphviz2.38\bin"

app = RheeApp(0)
app.MainLoop()
