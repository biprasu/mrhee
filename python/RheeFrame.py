#encoding=utf8

from wx import *
from wx.stc import *
from RheeVariables import *
from RheePrompt import RheePrompt
from RheeText import RheeText
from wx.lib.dialogs import ScrolledMessageDialog
from compiler import compile_file
import RheeAutoComplete
from RheeUtils import MapBreakPoints
import re
import time
from RheeFindReplace import RheeFindReplaceDialog
from RheeWatch import RheeWatch, to_uni
from RheeErrors import error_map
from RheeDrawFlowchart import draw_file
from RheeFlowChart import FlowChart

if (Platform == '__WXMSW__'):
    import win32api
else:
    import signal


def killProcess(pid):
    if (Platform == '__WXMSW__'):
        handle = win32api.OpenProcess(1, 0, pid)
        win32api.TerminateProcess(handle, 0)
    else:
        os.kill(pid, signal.SIGKILL)




#*********************************************************************************************************************



class RheeFrame(Frame):
    def __init__(self, parent, id, title, fn=""):

        self.filename = fn

        self.lastprogargs = ""

        Frame.__init__(self, parent, id, title, Point(0, 0), Size(640, 480))

        if (not os.path.exists(bitmapdirectory)):
            d = ScrolledMessageDialog(self, (
            "Bitmap Directory (" + bitmapdirectory + ") Does Not Exist.\nThis is either a bug with Rhee,\n an error with your installation,\nor the bitmap directory was simply removed."),
                                      "Rhee Fatal Error")
            d.ShowModal()
            d.Destroy()
            sys.exit(1)
        if (len(pdbstring) == 0):
            d = ScrolledMessageDialog(self, (
            "Cannot Find Python Debugger.\nThis means that pdb.py was not found.\nThis means it was not in <Python Installation Directory>/lib\n or <Python Installation Directory>/lib/python<VersionNumber>\n\nYou will not be able use the debugger.\n"),
                                      "Rhee Error")
            d.ShowModal()
            d.Destroy()

        self.process = None
        self.needToUpdatePos = False
        self.pid = -1

        self.breakpoints = []

        self.findpos = 0
        self.findtext = ""
        self.findflags = 0
        self.replacetext = ""
        self.wordwrap = 0

        self.autoindent = 1

        self.pythonargs = ""

        self.txtFileStyleArray = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        self.txtPromptStyleArray = ["", ""]

        self.DebugActive = False
        self.Go = False

        self.WaitingForDebugInput = False

        #Used for homedirectory
        self.defaultdirectory = ""
        #Used for current directory with open/save
        self.ddirectory = ""

        self.iconsize = 16

        self.whitespaceisvisible = False

        self.recentfileslimit = 10

        self.promptisvisible = False
        self.txtPromptSize = 40

        self.tabwidth = 8

        self.checkeol = False
        self.eolmode = STC_EOL_LF

        self.LoadPreferences()

        self.promptvisiblefile = self.promptisvisible

        if (Platform == '__WXMSW__'):
            self.SetIcon(Icon((bitmapdirectory + "/rhee.ico"), BITMAP_TYPE_ICO))
        else:
            self.SetIcon(Icon((bitmapdirectory + "/drpython.xpm"), BITMAP_TYPE_XPM))

        self.WatchWindow = RheeWatch(self)



        self.bSizer = BoxSizer(VERTICAL)
        self.txtFile = RheeText(self, ID_APP)
        self.txtFile.MarkerDefine(MARKER_LINE,STC_MARK_ARROW | STC_MARK_BACKGROUND,'#FF0000','#00FF00')
        self.txtFile.MarkerDefine(MARKER_LINE_ERROR,STC_MARK_ARROW | STC_MARK_BACKGROUND,'#FF0000','#F00000')
        self.txtFile.MarkerSetBackground(MARKER_BREAKPOINT, '#FF0000')
        self.Go = False

        self.txtPrompt = RheePrompt(self, ID_APP)
        if (self.txtPromptSize == 100):
            self.bSizer.Add(self.txtFile, 1, EXPAND)
        else:
            self.bSizer.Add(self.txtFile, (100 - self.txtPromptSize), EXPAND)
        if (self.txtPromptSize == 100):
            self.bSizer.Add(self.txtPrompt, 1, EXPAND)
        else:
            self.bSizer.Add(self.txtPrompt, self.txtPromptSize, EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(self.bSizer)

        if (not self.promptisvisible):
            self.bSizer.Show(self.txtPrompt, False)
            self.bSizer.Layout()
        elif (self.txtPromptSize == 100):
            self.bSizer.Show(self.txtFile, False)
            self.bSizer.Layout()

        self.toolbar = self.CreateToolBar(TB_HORIZONTAL)

        self.SetupToolBar()

        self.ID_RECENT_FILES = []
        self.recentfiles = []

        self.LoadRecentFiles()

        self.filemenu = Menu()
        self.filemenu.Append(ID_NEW, "&New (Ctrl + N)", " Open a new window")
        self.filemenu.Append(ID_OPEN, "&Open (Ctrl + O)", " Open a File")
        self.recentmenu = Menu()
        self.CreateRecentFileMenu()
        self.filemenu.AppendMenu(ID_OPEN_RECENT, "Open &Recent", self.recentmenu)
        self.filemenu.Append(ID_RELOAD, "&Reload File", " Reload the current file")
        self.filemenu.AppendSeparator()
        self.filemenu.Append(ID_CLOSE, "&Close", "Close the file")
        self.filemenu.AppendSeparator()
        self.filemenu.Append(ID_CLEAR_RECENT, "Clear Recent File List", "Clear Recent File List")
        self.filemenu.AppendSeparator()
        self.filemenu.Append(ID_SAVE, "&Save (Ctrl + S)", " Save the file")
        self.filemenu.Append(ID_SAVE_AS, "Save &As", " Save a file as ... another file")
        self.filemenu.AppendSeparator()
        self.filemenu.Append(ID_CLEAN_UP_TABS, "&Clean Up Tabs", " Replace-All: 8 Spaces -> Tab")
        self.formatmenu = Menu()
        self.formatmenu.Append(ID_UNIXMODE, "Unix Mode", " Set Line Endings to '\\n'", ITEM_RADIO)
        self.formatmenu.Append(ID_WINMODE, "DOS/Windows Mode", " Set Line Endings to '\\r\\n'", ITEM_RADIO)
        self.formatmenu.Append(ID_MACMODE, "Mac Mode", " Set Line Endings to '\\r'", ITEM_RADIO)
        self.filemenu.AppendMenu(ID_FORMATMENU, "File Format", self.formatmenu)
        self.filemenu.AppendSeparator()
        self.filemenu.Append(ID_EXIT, "E&xit", " Exit Rhee")
        self.filemenu.Enable(ID_RELOAD, False)

        searchmenu = Menu()
        searchmenu.Append(ID_FIND, "&Find (Ctrl + F)", " Find text")
        searchmenu.Append(ID_FIND_AGAIN, "&Find Again (F3)", " Find text again")
        searchmenu.Append(ID_REPLACE, "&Replace", " Find text, replace it with new text")
        searchmenu.Append(ID_SWITCHEROO, "&Switcheroo",
                          " Switch all occurences of text A with text B, and text B with text A")
        searchmenu.Append(ID_GOTO, "&Go To (Ctrl + G)", " Got To Line #")

        self.programmenu = Menu()
        self.programmenu.Append(ID_RUN, "&Run (Ctrl + R)", " Run the program")
        self.programmenu.Append(ID_SET_ARGS, "Set &Arguments", " Set program arguments.")
        self.programmenu.Append(ID_PYTHON, "Open a Python &Interpreter (Ctrl + P)", " Run the python interpreter")
        self.programmenu.Append(ID_PYTHON_DEBUGGER, "Run using Python Debugger (pdb) (Ctrl + D)",
                                " Run the program using Python's debugger")
        self.programmenu.Append(ID_END, "&End (Ctrl + E)", " End Current Program")
        self.programmenu.Append(ID_ADD_BREAKPOINT, "&Add Breakpoint", " Add a breakpoint to the current program")
        self.programmenu.Append(ID_REMOVE_BREAKPOINT, "Remove &Breakpoint",
                                " Remove a breakpoint from the current program")
        self.programmenu.Append(ID_REMOVE_ALL_BREAKPOINTS, "Remove &All Breakpoints",
                                " Remove all breakpoints from the current program")
        self.programmenu.Append(ID_FLOWCHART, "Flowchart",
                                " Show Flowchart")
        self.programmenu.Enable(ID_RUN, False)
        self.programmenu.Enable(ID_SET_ARGS, False)
        self.programmenu.Enable(ID_END, False)
        self.programmenu.Enable(ID_PYTHON_DEBUGGER, False)

        optionsmenu = Menu()
        optionsmenu.Append(ID_PREFS, "&Preferences", " Customize Rhee")
        optionsmenu.Append(ID_TOGGLE_PROMPT, "&Toggle Prompt (F6)", " View/Hide Prompt")
        optionsmenu.Append(ID_TOGGLE_VIEWWHITESPACE, "&Toggle View Whitespace", " View Whitespace")
        optionsmenu.Append(ID_CLEAR_PROMPT, "C&lear Prompt", " Clear the prompt of all text")
        optionsmenu.Append(ID_COMMENT_REGION, "&Comment", " Comments out the selected region.")
        optionsmenu.Append(ID_UNCOMMENT_REGION, "&UnComment", " UnComments out the selected region.")

        helpmenu = Menu()
        helpmenu.Append(ID_HELP, "&Help", " Documentation")
        helpmenu.Append(ID_ABOUT, "&About", " About Rhee")

        menuBar = MenuBar()
        menuBar.Append(self.filemenu, "&File")
        menuBar.Append(searchmenu, "&Search")
        menuBar.Append(self.programmenu, "&Program")
        menuBar.Append(optionsmenu, "&Options")
        menuBar.Append(helpmenu, "&Help")

        #TODO: check
        # self.SetMenuBar(menuBar)


        EVT_MENU(self, ID_NEW, self.OnNew)
        EVT_MENU(self, ID_OPEN, self.OnOpen)
        EVT_MENU(self, ID_CLOSE, self.OnClose)
        EVT_MENU(self, ID_RELOAD, self.OnReload)
        EVT_MENU(self, ID_CLEAR_RECENT, self.OnClearRecent)
        EVT_MENU(self, ID_SAVE, self.OnSave)
        EVT_MENU(self, ID_SAVE_AS, self.OnSaveAs)
        EVT_MENU(self, ID_CLEAN_UP_TABS, self.OnCleanUpTabs)
        EVT_MENU(self, ID_EXIT, self.OnExit)

        EVT_MENU(self, ID_UNIXMODE, self.OnFormatUnixMode)
        EVT_MENU(self, ID_WINMODE, self.OnFormatWinMode)
        EVT_MENU(self, ID_MACMODE, self.OnFormatMacMode)

        EVT_MENU(self, ID_FIND, self.OnMenuFind)
        EVT_MENU(self, ID_FIND_AGAIN, self.OnMenuFindNext)
        EVT_MENU(self, ID_REPLACE, self.OnMenuReplace)
        EVT_MENU(self, ID_SWITCHEROO, self.OnMenuSwitcheroo)

        EVT_COMMAND_FIND(self, -1, self.OnFind)
        EVT_COMMAND_FIND_NEXT(self, -1, self.OnFind)
        EVT_COMMAND_FIND_REPLACE(self, -1, self.OnFind)
        EVT_COMMAND_FIND_REPLACE_ALL(self, -1, self.OnFind)
        EVT_COMMAND_FIND_CLOSE(self, -1, self.OnFindClose)

        EVT_MENU(self, ID_GOTO, self.OnGoTo)

        EVT_MENU(self, ID_RUN, self.OnRun)
        EVT_MENU(self, ID_SET_ARGS, self.OnSetArgs)
        EVT_MENU(self, ID_PYTHON, self.OnPython)
        EVT_MENU(self, ID_PYTHON_DEBUGGER, self.OnRunWithDebugger)
        EVT_MENU(self, ID_END, self.OnEnd)
        EVT_MENU(self, ID_ADD_BREAKPOINT, self.OnAddBreakpoint)
        EVT_MENU(self, ID_FLOWCHART, self.OnFlowchart)
        # EVT_MENU(self, ID_REMOVE_BREAKPOINT, self.OnRemoveBreakpoint)
        # EVT_MENU(self, ID_REMOVE_ALL_BREAKPOINTS, self.OnRemoveAllBreakpoints)

        # EVT_MENU(self, ID_PREFS, self.OnPrefs)
        EVT_MENU(self, ID_TOGGLE_PROMPT, self.OnTogglePrompt)
        EVT_MENU(self, ID_TOGGLE_VIEWWHITESPACE, self.OnToggleViewWhiteSpace)
        EVT_MENU(self, ID_CLEAR_PROMPT, self.OnClearPrompt)
        EVT_MENU(self, ID_COMMENT_REGION, self.OnCommentRegion)
        EVT_MENU(self, ID_UNCOMMENT_REGION, self.OnUnCommentRegion)

        # EVT_MENU(self, ID_ABOUT, self.OnAbout)
        # EVT_MENU(self, ID_HELP, self.OnHelp)

        self.CreateStatusBar()

        self.SetStatusText(u"ऋ मा स्वागत छ")

        self.txtFile.SetLexer(STC_LEX_CPP)
        self.txtFile.SetKeyWords(0, u' '.join(RheeAutoComplete.keywords))

        self.SetupPrefsFile()

        self.txtFile.SetFocus()
        self.txtPrompt.SetReadOnly(1)
        self.writeposition = 0

        self.SetupPrefsPrompt()

        EVT_END_PROCESS(self, -1, self.OnProcessEnded)
        EVT_IDLE(self, self.OnIdle)

        #Arguments To Program
        if (len(sys.argv) > 1) and (len(self.filename) == 0):
            self.filename = sys.argv[1]
        #Arguments to Program or RheeFrame.
        if (len(self.filename) > 0):
            #Make sure the path is absolute
            self.filename = os.path.abspath(self.filename)
            #Convert Filename to correct format. (Only needed when called from the command line)
            #When called from function, already converted.
            if (Platform == '__WXMSW__'):
                self.filename = self.filename.replace("\\", "/")
            # self.DestroyRecentFileMenu()
            self.OpenFile(False)
            # self.CreateRecentFileMenu()

        EVT_CHAR(self, self.OnChar)
        EVT_CLOSE(self, self.OnCloseW)

    def CreateRecentFileMenu(self):
        x = 0
        numfiles = len(self.recentfiles)
        while (x < numfiles):
            self.recentmenu.Append(self.ID_RECENT_FILES[x], self.recentfiles[x], ("Open " + self.recentfiles[x]))
            EVT_MENU(self, self.ID_RECENT_FILES[x], self.OnOpenRecentFile)
            x = x + 1

    def DestroyRecentFileMenu(self):
        #You need to call this function BEFORE you update the list of recent files.
        x = 0
        mnuitems = self.recentmenu.GetMenuItems()
        num = len(mnuitems)
        while (x < num):
            self.recentmenu.Remove(self.ID_RECENT_FILES[x])
            mnuitems[x].Destroy()
            x = x + 1

    def DestroyToolBar(self):
        x = 0
        while (x < self.toolbarsize):
            self.toolbar.DeleteToolByPos(0)
            x = x + 1

    def Finder(self, event_type):
        if (event_type == EVT_COMMAND_FIND.typeId):
            self.findpos = self.txtFile.GetCurrentPos()
            p = self.txtFile.FindText(0, self.txtFile.GetLength(), self.findtext, self.findflags)
            if (p == -1):
                d = ScrolledMessageDialog(self, (u"खोजिएको शब्द (" + self.findtext + u") भेटिएन"), u"ऋ खोज")
                d.ShowModal()
                d.Destroy()
            p = self.txtFile.FindText(self.txtFile.GetCurrentPos(), self.txtFile.GetLength(), self.findtext,
                                      self.findflags)
            if (p == -1):
                p = self.txtFile.FindText(0, self.txtFile.GetLength(), self.findtext, self.findflags)
            else:
                self.txtFile.GotoPos(p)
                self.txtFile.SetSelectionStart(p)
                self.findpos = p
                self.txtFile.SetSelectionEnd(p + len(self.findtext.encode('utf8')))
        elif (event_type == EVT_COMMAND_FIND_NEXT.typeId):

            self.findpos = self.txtFile.GetCurrentPos()
            p = self.txtFile.FindText(self.txtFile.GetCurrentPos(), self.txtFile.GetLength(), self.findtext,
                                      self.findflags)
            if (p == -1):
                p = self.txtFile.FindText(0, self.txtFile.GetLength(), self.findtext, self.findflags)
                if (p == -1):
                    d = ScrolledMessageDialog(self, (u"खोजिएको शब्द (" + self.findtext + u") भेटिएन"), u"ऋ खोज")
                    d.ShowModal()
                    d.Destroy()
                    return
            self.txtFile.GotoPos(p)
            self.txtFile.SetSelectionStart(p)
            self.findpos = p
            self.txtFile.SetSelectionEnd(p + len(self.findtext.encode('utf8')))
        elif (event_type == EVT_COMMAND_FIND_REPLACE.typeId):
            if (len(self.replacetext) > 0):
                if (self.txtFile.GetCurrentPos() == (self.findpos + len(self.findtext.encode('utf8')))):
                    self.txtFile.SetTargetStart(self.findpos)
                    self.txtFile.SetTargetEnd(self.findpos + len(self.findtext.encode('utf8')))
                    self.txtFile.ReplaceTarget(self.replacetext)
        elif (event_type == EVT_COMMAND_FIND_REPLACE_ALL.typeId):
            if (len(self.replacetext) > 0):
                p = self.txtFile.FindText(0, self.txtFile.GetLength(), self.findtext, self.findflags)
                x = 0
                while (p is not -1):
                    self.txtFile.GotoPos(p)
                    self.txtFile.SetTargetStart(p)
                    self.txtFile.SetTargetEnd(p + len(self.findtext))
                    self.txtFile.ReplaceTarget(self.replacetext)
                    p = self.txtFile.FindText((p + len(self.replacetext.encode('utf8'))), self.txtFile.GetLength(), self.findtext,
                                              self.findflags)
                    x = x + 1
                d = ScrolledMessageDialog(self, (
                str(x) + " occurances of " + self.findtext + " replaced with " + self.replacetext), "Replace All")
                d.ShowModal()
                d.Destroy()

    def isvalidbreakpoint(self, text):
        if (len(text) <= 0):
            return False
        elif (text.isspace()):
            return False
        else:
            ind = text.find('#')
            if not (ind == -1):
                if (text[:ind].isspace()):
                    return False
                elif (ind == 0):
                    return False
        return True

    def LoadPreferences(self, UseDefault=False):
        #check for preferences file in user homedirectory
        if (os.path.exists(homedirectory + "/preferences.dat")) and (not UseDefault):
            usingdefault = False
            f = homedirectory + "/preferences.dat"
        else:
            usingdefault = True
            if (Platform == '__WXMSW__'):
                f = programdirectory + "preferences.windows.dat"
            else:
                f = programdirectory + "preferences.unix.dat"
        try:
            fin = open(f, 'r')
            s = fin.readline().rstrip()
            self.autoindent = int(s)
            s = fin.readline().rstrip()
            self.wordwrap = int(s)
            s = fin.readline().rstrip()
            self.whitespaceisvisible = int(s)
            s = fin.readline().rstrip()
            self.iconsize = int(s)
            s = fin.readline().rstrip()
            self.recentfileslimit = int(s)
            s = fin.readline().rstrip()
            self.tabwidth = int(s)
            s = fin.readline().rstrip()
            if (s is not "0"):
                self.pythonargs = s
            else:
                self.pythonargs = ""
            s = fin.readline().rstrip()
            if (s is not "0"):
                self.defaultdirectory = s
                self.ddirectory = s
            else:
                self.defaultdirectory = ""
            l = len(self.txtFileStyleArray)
            x = 0
            while (x < l):
                s = fin.readline().rstrip()
                self.txtFileStyleArray[x] = s
                x = x + 1
            s = fin.readline().rstrip()
            self.promptisvisible = int(s)
            s = fin.readline().rstrip()
            self.txtPromptSize = int(s)
            l = len(self.txtPromptStyleArray)
            x = 0
            while (x < l):
                s = fin.readline().rstrip()
                self.txtPromptStyleArray[x] = s
                x = x + 1
            #version update, and error here means the user may just
            #have an old preferences file.  Leave these at default, and warn the user if there is an error.
            try:
                s = fin.readline().rstrip()
                self.checkeol = int(s)
                s = fin.readline().rstrip()
                eolmode = int(s)
                if (eolmode == 0):
                    self.eolmode = STC_EOL_LF
                elif (eolmode == 1):
                    self.eolmode = STC_EOL_CRLF
                else:
                    self.eolmode = STC_EOL_CR
            except:
                d = ScrolledMessageDialog(self, (
                "Error with: " + f + "\nThis error is with the File Format Preferences, the rest are fine.\nJust save the preferences again, and you should be fine."),
                                          "Preferences Error")
                d.ShowModal()
                d.Destroy()
            fin.close()
        except:
            if (not usingdefault):
                d = ScrolledMessageDialog(self, ("Error with: " + f + "\nRhee will load the program defaults."),
                                          "Preferences Error")
                d.ShowModal()
                d.Destroy()
                self.LoadPreferences(True)
            else:
                d = ScrolledMessageDialog(self, ("Gross Error with: " + f), "Preferences Error")
                d.ShowModal()
                d.Destroy()

    def LoadRecentFiles(self):
        if (not os.path.exists(homedirectory)):
            os.mkdir(homedirectory)
        f = homedirectory + "/recent_files.log"
        if (not os.path.exists(f)):
            try:
                t = open(f, 'w')
                t.close()
            except IOError:
                d = ScrolledMessageDialog(self, ("Error Creating: " + f), "Recent Files Error")
                d.ShowModal()
                d.Destroy()
        try:
            fin = open(f, 'r')
            s = fin.readline()
            last = ID_RECENT_FILES_BASE
            x = 0
            while (len(s) > 0) and (x < self.recentfileslimit):
                s = s.rstrip()
                if (len(s) > 0):
                    self.ID_RECENT_FILES.append(last)
                    self.recentfiles.append(s)
                last = last + 1
                x = x + 1
                s = fin.readline()
            fin.close()
        except IOError:
            d = ScrolledMessageDialog(self, ("Error Reading: " + f), "Recent Files Error")
            d.ShowModal()
            d.Destroy()

    # def OnAbout(self, event):
    #     e = About.AboutDialog(self, "About Rhee", programdirectory)
    #     e.ShowModal()
    #     e.Destroy()

    def OnAddBreakpoint(self, event):
        # d = TextEntryDialog(self, "Line Number for the breakpoint:", "Add Breakpoint",
        #                     str(self.txtFile.GetCurrentLine() + 1))
        # if d.ShowModal() == ID_OK:
        #     try:
        #         x = int(d.GetValue()) - 1
        #     except:
        #         d = ScrolledMessageDialog(self, "You must enter an integer (number, eg 1,2,128)", "Rhee")
        #         d.ShowModal()
        #         d.Destroy()
        #         return
        x = self.txtFile.GetCurrentLine()



        if x in self.breakpoints:
            # Remove Breakpoint
            self.breakpoints.pop(self.breakpoints.index(x))
            self.txtFile.MarkerDelete(x, MARKER_BREAKPOINT)
        elif (x > -1) and (x < self.txtFile.GetLineCount()):
            if (self.isvalidbreakpoint(self.txtFile.GetLine(x))):
                self.txtFile.MarkerAdd(x, MARKER_BREAKPOINT)
                # self.txtFile.MarkerAdd(x, 0)

                self.breakpoints.append(x)
            # else:
            #     d = ScrolledMessageDialog(self,
            #                               ("Line number: " + str(x + 1) + "\nIs either a comment, or whitespace"),
            #                               "Rhee")
            #     d.ShowModal()
            #     d.Destroy()
        #     else:
        #         d = ScrolledMessageDialog(self, "Line number does not exist", "Rhee")
        #         d.ShowModal()
        #         d.Destroy()
        #         return
        # d.Destroy()

    def OnChar(self, event):
        self.RunShortcuts(event)

        event.Skip()

    def OnCleanUpTabs(self, event):
        d = TextEntryDialog(self, "Number of spaces to replace with a Tab:", "Clean Up Tabs", "8")
        if d.ShowModal() == ID_OK:
            try:
                x = int(d.GetValue()) - 1
            except:
                d = ScrolledMessageDialog(self, "You must enter an integer (number, eg 1,2,128)", "Rhee")
                d.ShowModal()
                d.Destroy()
                return
            if (x > -1) and (x <= 128):
                y = 0
                oof = " "
                while (y < x):
                    oof = oof + " "
                    y = y + 1
                self.replace_all(oof, "\t", 0)
            else:
                d = ScrolledMessageDialog(self,
                                          "That number seems WAY too high.  Just what are you doing, replacing more than 128 spaces with a tab?",
                                          "Rhee Foolish Error")
                d.ShowModal()
                d.Destroy()
                return
        d.Destroy()

    def OnClearPrompt(self, event):
        d = MessageDialog(self, "This will clear all text from the prompt.\nAre you sure you want to do this?",
                          "Rhee", YES_NO | ICON_QUESTION)
        answer = d.ShowModal()
        d.Destroy()
        if (answer == ID_YES):
            iii = self.txtPrompt.GetReadOnly()
            self.txtPrompt.SetReadOnly(0)
            self.txtPrompt.editpoint = 0
            self.writeposition = 0
            self.txtPrompt.ClearAll()
            self.txtPrompt.SetReadOnly(iii)

    def OnClearRecent(self, event):
        d = MessageDialog(self, "This will clear all recent files\nAre you sure you want to do this?", "Rhee",
                          YES_NO | ICON_QUESTION)
        answer = d.ShowModal()
        d.Destroy()
        if (answer == ID_YES):
            self.recentfiles = []
            self.DestroyRecentFileMenu()
            self.WriteRecentFiles()

    def OnClose(self, event):
        if (self.txtFile.GetModify()):
            d = MessageDialog(self, u"के फाइल सेव गर्न चाहनुहुन्छ?   ", u"ऋ", YES_NO | CANCEL | ICON_QUESTION)
            answer = d.ShowModal()
            d.Destroy()
            if (answer == ID_YES):
                self.OnSave(event)
            elif (answer == ID_CANCEL):
                return
        self.txtFile.SetText("")
        self.filename = ""
        self.SetTitle(u"ऋ - नया फाइल")
        self.txtFile.EmptyUndoBuffer()
        self.txtFile.SetSavePoint()
        self.toolbar.EnableTool(ID_RUN, False)
        self.toolbar.EnableTool(ID_FLOWCHART, False)
        self.toolbar.EnableTool(ID_SET_ARGS, False)
        self.programmenu.Enable(ID_RUN, False)
        self.programmenu.Enable(ID_SET_ARGS, False)
        self.toolbar.EnableTool(ID_PYTHON_DEBUGGER, False)
        self.programmenu.Enable(ID_PYTHON_DEBUGGER, False)
        self.toolbar.EnableTool(ID_RELOAD, False)
        self.filemenu.Enable(ID_RELOAD, False)

    def OnCloseW(self, event):
        if (event.CanVeto() and self.txtFile.GetModify()):
            d = MessageDialog(self, u"के तपाई सेव गर्न चाहनुहुन्छ?    ", u"ऋ", YES_NO | CANCEL | ICON_QUESTION)
            answer = d.ShowModal()
            d.Destroy()
            if (answer == ID_YES):
                self.OnSave(event)
            elif (answer == ID_CANCEL):
                return
        event.Skip()

    def OnCommentRegion(self, event):
        selstart, selend = self.txtFile.GetSelection()
        #From the start of the first line selected
        start = self.txtFile.LineFromPosition(selstart)
        start = self.txtFile.GetLineIndentPosition(start) - self.txtFile.GetLineIndentation(start)
        #To the end of the last line selected
        end = self.txtFile.GetLineEndPosition(self.txtFile.LineFromPosition(selend))
        self.txtFile.SetSelection(start, end)
        text = "#" + self.txtFile.GetSelectedText()
        text = text.replace('\n', "\n#")
        self.txtFile.ReplaceSelection(text)

    def OnEnd(self, event):
        if (self.pid is not -1):
            if (len(self.filename) > 0):
                self.toolbar.EnableTool(ID_RUN, True)
                self.toolbar.EnableTool(ID_FLOWCHART, True)
                self.toolbar.EnableTool(ID_SET_ARGS, True)
                self.programmenu.Enable(ID_RUN, True)
                self.programmenu.Enable(ID_SET_ARGS, True)
                self.toolbar.EnableTool(ID_PYTHON_DEBUGGER, True)
                self.programmenu.Enable(ID_PYTHON_DEBUGGER, True)
            self.toolbar.EnableTool(ID_PYTHON, True)
            self.toolbar.EnableTool(ID_END, False)
            self.programmenu.Enable(ID_PYTHON, True)
            self.programmenu.Enable(ID_END, False)
            killProcess(self.pid)
            self.txtPrompt.SetReadOnly(1)
            self.needToUpdatePos = False
            self.DebugActive = False
            self.Go = False

    def OnExit(self, event):
        self.Close(False)

    def OnFind(self, event):
        map = {EVT_COMMAND_FIND.typeId: "FIND", EVT_COMMAND_FIND_NEXT.typeId: "FIND_NEXT", EVT_COMMAND_FIND_REPLACE.typeId: "REPLACE",
               EVT_COMMAND_FIND_REPLACE_ALL.typeId: "REPLACE_ALL"}
        et = event.GetEventType()
        try:
            eventType = map[et]
        except KeyError:
            d = ScrolledMessageDialog(self, "FindReplace Dialog Event Type Error", "Rhee Internal Error!")
            d.ShowModal()
            d.Destroy()
        if (et == EVT_COMMAND_FIND_REPLACE.typeId):
            self.findtext = event.GetFindString()
            self.findflags = event.GetFlags()
            self.replacetext = event.GetReplaceString()
        elif (et == EVT_COMMAND_FIND.typeId or et==EVT_COMMAND_FIND_NEXT.typeId):
            self.findtext = event.GetFindString()
            self.findflags = event.GetFlags()
        elif (et == EVT_COMMAND_FIND_REPLACE_ALL.typeId):
            self.replacetext = event.GetReplaceString()
            self.findtext = event.GetFindString()
            self.findflags = event.GetFlags()

        self.Finder(et)

    def OnFindClose(self, event):
        event.GetDialog().Destroy()

    def OnFormatMacMode(self, event):
        self.txtFile.SetEOLMode(STC_EOL_CR)
        self.txtFile.ConvertEOLs(STC_EOL_CR)

    def OnFormatUnixMode(self, event):
        self.txtFile.SetEOLMode(STC_EOL_LF)
        self.txtFile.ConvertEOLs(STC_EOL_LF)

    def OnFormatWinMode(self, event):
        self.txtFile.SetEOLMode(STC_EOL_CRLF)
        self.txtFile.ConvertEOLs(STC_EOL_CRLF)

    def OnGoTo(self, event):
        d = TextEntryDialog(self, 'Go To Line Number:', 'Rhee - Go To', '')
        if (d.ShowModal() == ID_OK):
            v = d.GetValue()
            try:
                v = int(v) - 1
                if (v >= 0) and (v < self.txtFile.GetLineCount()):
                    self.txtFile.ScrollToLine(v)
                    self.txtFile.GotoLine(v)
                else:
                    e = ScrolledMessageDialog(self, "That line does not exist", "Rhee Error")
                    e.ShowModal()
                    e.Destroy()
            except StandardError:
                e = ScrolledMessageDialog(self, "You must enter an integer (1, 2, 3, etc)", "Rhee Error")
                e.ShowModal()
                e.Destroy()
        d.Destroy()

    # def OnHelp(self, event):
    #     e = Help.HelpDialog(self, "Rhee Help", programdirectory)
    #     e.ShowModal()
    #     e.Destroy()

    def WriteDebugString(self, string):
        if not self.pid == -1:
            self.process.GetOutputStream().write(string)
            self.WaitingForDebugInput = False
            self.txtFile.MarkerDeleteAll(MARKER_LINE)

    def ReadImmediateStream(self):
        istream = self.process.GetInputStream()
        i = 0
        while not istream.CanRead(): pass
        _ = istream.read()
        print _
        return _

    def UpdateWatch(self):
        # return
        if not self.WaitingForDebugInput: return

        ostream = self.process.GetOutputStream()
        if self.process.GetInputStream().CanRead(): return
        ostream.write('dir()\n')
        varlist = eval(self.ReadImmediateStream().split('\n')[0])[3:]   #Remove the first three variables out
        vardict = {}
        for v in varlist:
            ostream.write('p '+ str(v) + '\n')
            value = self.ReadImmediateStream().split('\n')[0]
            vardict[str(v)] = value
        self.WatchWindow.restart(vardict)

    def ProcessError(self, errorstring):
        #get the line number first
        print errorstring
        ln = re.findall(r"File \"(.+)\", line (\d+)", errorstring)

        for path, line in ln:
            if os.path.abspath(path) == os.path.abspath(self.outfile):
                error_line = self.pytorhee[int(line)-1]
                self.txtFile.MarkerDeleteAll(MARKER_LINE)
                self.txtFile.MarkerAdd(error_line, MARKER_LINE_ERROR)
                # self.txtFile.Marker
                self.txtFile.GotoLine(error_line)
                rhee_error_text = ''
                for pythonerror in error_map.keys():
                    if pythonerror in errorstring:
                        rhee_error_text = error_map[pythonerror]
                        break
                else:
                    rhee_error_text = u"कोडमा समस्या भेटियो"

                rhee_error = u"लाइन %s मा: \n "% to_uni(str(error_line)) + rhee_error_text
                d = MessageDialog(self, rhee_error,
                                              u"गल्ति भेटियो", OK | ICON_ERROR)
                d.ShowModal()
                d.Destroy()
                self.txtFile.MarkerDeleteAll(MARKER_LINE_ERROR)

        if self.DebugActive: self.OnEnd(None)



        # os.path.samefile()
        pass

    def OnIdle(self, event):
        if not self.Go: return
        stillreadinginput = False
        stillreadingoutput = False
        lineno = 0
        if (self.process is not None):
            stream = self.process.GetInputStream()
            if (stream.CanRead()):
                stillreadinginput = True
                self.needToUpdatePos = True
                t = stream.read()

                for text in t.split('\n'):
                    print text
                    if text[:5] == '(Pdb)':
                        self.WaitingForDebugInput = True
                        if "Breakpoint" in text:
                            lineno = self.pytorhee[int(re.findall('(\d+)$',text)[0])-1]

                        #Highlight the currentline
                        self.txtFile.MarkerDeleteAll(MARKER_LINE)
                        self.txtFile.MarkerAdd(lineno, MARKER_LINE)
                        self.UpdateWatch()

                    elif len(text)>0 and text[0] == '>' or len(text)>=2 and text[:2] == '->':
                        if text[:2]=='->': lineno = int(re.findall('(\d+)$',text)[0])-1
                    elif text == "The program finished and will be restarted" or text == '--Return--':
                        self.WriteDebugString('q\n')
                        return
                    else:
                        #TODO: Check out the prompt here
                        if all(text.isalphanum()): continue
                        self.txtPrompt.SetReadOnly(0)
                        if len(text)>0 and text[:-1]!='\n': text+='\n'

                        self.txtPrompt.GotoPos(self.txtPrompt.GetLength())

                        self.txtPrompt.AddText(text.decode('utf-8'))

                        self.writeposition = self.txtPrompt.GetLength()
                        self.txtPrompt.EmptyUndoBuffer()
                        self.txtPrompt.SetSavePoint()
                        self.txtPrompt.editpoint = self.txtPrompt.GetLength()

            stream = self.process.GetErrorStream()
            if (stream.CanRead()):

                error = stream.read()
                self.ProcessError(error)

                stillreadingerror = True
                self.needToUpdatePos = True
                text = stream.read()
                self.txtPrompt.GotoPos(self.txtPrompt.GetLength())
                self.txtPrompt.AddText(text)
                self.writeposition = self.txtPrompt.GetLength()
                self.txtPrompt.EmptyUndoBuffer()
                self.txtPrompt.SetSavePoint()
                self.txtPrompt.editpoint = self.txtPrompt.GetLength()
        if (not (stillreadinginput or stillreadingoutput) and self.needToUpdatePos):
            self.txtPrompt.GotoPos(self.txtPrompt.GetLength())
            self.needToUpdatePos = False

    def OnMenuFind(self, event):
        data = FindReplaceData()
        if (self.txtFile.GetSelectionStart() < self.txtFile.GetSelectionEnd()):
            data.SetFindString(
                self.txtFile.GetTextRange(self.txtFile.GetSelectionStart(), self.txtFile.GetSelectionEnd()))
        else:
            data.SetFindString(self.findtext)

        # if False:
        #     d = FindReplaceDialog(self, data, "Find", FR_NOUPDOWN)
        #     d.data = data
        # else:
        d = RheeFindReplaceDialog(self, -1, "Find", data.GetFindString(), findreplace = False)
        # d = RheeFindReplaceDialog(self)
        d.Show(True)


    def OnMenuFindNext(self, event):
        if (self.txtFile.GetSelectionStart() < self.txtFile.GetSelectionEnd()):
            self.findtext = self.txtFile.GetTextRange(self.txtFile.GetSelectionStart(), self.txtFile.GetSelectionEnd())
        self.Finder(EVT_COMMAND_FIND_NEXT)

    def OnMenuReplace(self, event):
        data = FindReplaceData()
        if (self.txtFile.GetSelectionStart() < self.txtFile.GetSelectionEnd()):
            data.SetFindString(
                self.txtFile.GetTextRange(self.txtFile.GetSelectionStart(), self.txtFile.GetSelectionEnd()))
        else:
            data.SetFindString(self.findtext)
        # d = FindReplaceDialog(self, data, "Replace", FR_NOUPDOWN | FR_REPLACEDIALOG)
        # d.data = data
        d = RheeFindReplaceDialog(self, -1, "Find", data.GetFindString(), findreplace = True)
        d.Show(True)

    def OnMenuSwitcheroo(self, event):
        d = RheeFindReplace(self, -1, "Switcheroo")
        d.ShowModal()
        a = d.textA
        b = d.textB
        temp = "DRPYTHONTEMPSWITCHEROO"
        if (d.IsValidText()):
            self.replace_all(a, temp, d.flags)
            self.replace_all(b, a, d.flags)
            self.replace_all(temp, b, d.flags)


    def OnNew(self, event):
        f = RheeFrame(None, -1, u"ऋ - नया फाइल")
        f.Show(True)

    def OnOpen(self, event):
        dlg = FileDialog(self, "Open", "", "", wildcard, OPEN)
        if (len(self.ddirectory) > 0):
            try:
                dlg.SetDirectory(self.ddirectory)
            except:
                d = ScrolledMessageDialog(self, ("Error Setting Default Directory To: " + self.lastdirectory),
                                          "Rhee Error")
                d.ShowModal()
                d.Destroy()
        if (dlg.ShowModal() == ID_OK):
            old = self.filename
            self.filename = dlg.GetPath().replace("\\", "/")
            # self.DestroyRecentFileMenu()
            if (len(old) > 0) or (self.txtFile.GetModify()):
                self.OpenFile(True)
                self.filename = old
            else:
                self.OpenFile(False)
            # self.CreateRecentFileMenu()
        dlg.Destroy()

    def OnOpenRecentFile(self, event):
        recentmenuindex = event.GetId() - ID_RECENT_FILES_BASE
        old = self.filename
        self.filename = self.recentfiles[recentmenuindex]
        self.DestroyRecentFileMenu()
        if (len(old) > 0) or (self.txtFile.GetModify()):
            self.OpenFile(True)
            self.filename = old
        else:
            self.OpenFile(False)
        # self.CreateRecentFileMenu()

    # def OnPrefs(self, event):
    #     eolmodes = [STC_EOL_LF, STC_EOL_CRLF, STC_EOL_CR]
    #     d = Prefs.drPrefsDialog(self, -1, "Rhee - Preferences", programdirectory, homedirectory,
    #                               self.txtFileStyleArray, self.txtPromptStyleArray, self.promptvisiblefile,
    #                               self.txtPromptSize, self.autoindent, self.wordwrap, self.whitespaceisvisible,
    #                               self.iconsize, self.recentfileslimit, self.tabwidth, self.pythonargs,
    #                               self.defaultdirectory, self.checkeol, self.eolmode, eolmodes)
    #
    #     oldiconsize = self.iconsize
    #     oldrfl = self.recentfileslimit
    #
    #     d.ShowModal()
    #
    #     if (d.NeedToUpdate()):
    #         self.txtFileStyleArray, self.txtPromptStyleArray, self.promptisvisible, self.txtPromptSize, self.autoindent, self.wordwrap, self.whitespaceisvisible, self.iconsize, self.recentfileslimit, self.tabwidth, self.pythonargs, self.defaultdirectory, self.checkeol, self.eolmode = d.GetPreferences()
    #         self.promptvisiblefile = self.promptisvisible
    #         self.DestroyToolBar()
    #         self.SetupToolBar()
    #         self.SetupPrefsFile()
    #         self.SetupPrefsPrompt()
    #         self.bSizer.Remove(self.txtFile)
    #         self.bSizer.Remove(self.txtPrompt)
    #         if (not oldrfl is self.recentfileslimit):
    #             self.DestroyRecentFileMenu()
    #             self.ID_RECENT_FILES = []
    #             self.recentfiles = []
    #
    #             # self.LoadRecentFiles()
    #             # self.CreateRecentFileMenu()
    #         if (self.txtPromptSize == 100):
    #             self.bSizer.Add(self.txtFile, 1, EXPAND)
    #         else:
    #             self.bSizer.Add(self.txtFile, (100 - self.txtPromptSize), EXPAND)
    #             self.bSizer.Show(self.txtFile, True)
    #         if (self.txtPromptSize == 100):
    #             self.bSizer.Add(self.txtPrompt, 1, EXPAND)
    #         else:
    #             self.bSizer.Add(self.txtPrompt, self.txtPromptSize, EXPAND)
    #         if (not self.promptisvisible):
    #             self.bSizer.Show(self.txtPrompt, False)
    #         elif (self.txtPromptSize == 100):
    #             self.bSizer.Show(self.txtFile, False)
    #             self.bSizer.Show(self.txtPrompt, True)
    #         else:
    #             self.bSizer.Show(self.txtPrompt, True)
    #         self.Layout()
    #         #A Really Odd Way of making sure the toolbar is sized correctly.
    #         #Update(), Layout(), SendSizeEvent(), Refresh(), and probably others did not
    #         #Do what I wanted.  This works, ergo... (This was also the only method consistent on windows and linux)
    #         #Plus, only execute this mess if the user changes the iconsize.
    #         if (self.iconsize is not oldiconsize):
    #             x = self.GetSizeTuple()
    #             if (self.IsMaximized()):
    #                 self.Maximize(False)
    #                 self.SetSize(Size((x[0] + 5), (x[1] + 5)))
    #                 self.SetSize(Size(x[0], x[1]))
    #                 self.Maximize(True)
    #             else:
    #                 self.SetSize(Size((x[0] + 5), (x[1] + 5)))
    #                 self.SetSize(Size(x[0], x[1]))

    def OnProcessEnded(self, event):
        #First, check for any leftover output.
        self.OnIdle(event)
        #Now, destroy the process.
        self.process.Destroy()
        self.process = None
        self.SetStatusText(" ")
        self.DebugActive = False
        self.Go = False
        if self.WatchWindow.Shown: self.WatchWindow.Show(False)
        self.txtFile.MarkerDeleteAll(MARKER_LINE)

        self.pid = -1
        # self.txtPrompt.SetReadOnly(0)
        txt = self.txtPrompt.GetText()+u"\n\nप्रोग्राम सकियो"
        self.txtPrompt.SetText(txt)
        # print type(txt)

        self.txtPrompt.SetReadOnly(1)
        if (len(self.filename) > 0):
            self.toolbar.EnableTool(ID_RUN, True)
            self.toolbar.EnableTool(ID_FLOWCHART, False)
            self.toolbar.EnableTool(ID_SET_ARGS, True)
            self.programmenu.Enable(ID_RUN, True)
            self.programmenu.Enable(ID_SET_ARGS, True)
            self.toolbar.EnableTool(ID_PYTHON_DEBUGGER, True)
            self.programmenu.Enable(ID_PYTHON_DEBUGGER, True)
        self.toolbar.EnableTool(ID_PYTHON, True)
        self.toolbar.EnableTool(ID_END, False)
        self.programmenu.Enable(ID_PYTHON, True)
        self.programmenu.Enable(ID_END, False)

    def OnPython(self, event):
        if (self.pid is -1):
            self.toolbar.EnableTool(ID_RUN, False)
            self.toolbar.EnableTool(ID_FLOWCHART, False)
            self.toolbar.EnableTool(ID_SET_ARGS, False)
            self.toolbar.EnableTool(ID_PYTHON, False)
            self.toolbar.EnableTool(ID_END, True)
            self.programmenu.Enable(ID_RUN, False)
            self.programmenu.Enable(ID_SET_ARGS, False)
            self.programmenu.Enable(ID_PYTHON, False)
            self.programmenu.Enable(ID_END, True)
            self.toolbar.ToggleTool(ID_TOGGLE_PROMPT, True)
            self.toolbar.EnableTool(ID_PYTHON_DEBUGGER, False)
            self.programmenu.Enable(ID_PYTHON_DEBUGGER, False)
            if (not self.promptisvisible):
                self.promptisvisible = True
                if (self.txtPromptSize == 100):
                    self.bSizer.Show(self.txtFile, False)
                self.bSizer.Show(self.txtPrompt, True)
                self.bSizer.Layout()
            self.txtPrompt.SetReadOnly(0)
            self.txtPrompt.ClearAll()
            self.txtPrompt.editpoint = 0
            self.needToUpdatePos = True
            if (len(self.filename) > 0):
                try:
                    cdir = self.filename[0:self.filename.rindex('/')]
                    os.chdir(cdir)
                except:
                    d = ScrolledMessageDialog(self, "Error Setting current directory for Python.", "Rhee RunError")
                    d.ShowModal()
                    d.Destroy()
            self.SetStatusText("Running Python Interpreter")
            self.process = Process(self)
            self.process.Redirect()
            self.pid = Execute((pythexec + " -i " + self.pythonargs), EXEC_ASYNC, self.process)
            self.txtPrompt.SetFocus()

    def OnReload(self, event):
        d = MessageDialog(self,
                          "This will reload the current file.\nAny changes will be lost.\nAre you sure you want to do this?",
                          "Rhee", YES_NO | ICON_QUESTION)
        answer = d.ShowModal()
        d.Destroy()
        if (answer == ID_YES):
            if (len(self.filename) > 0):
                self.txtFile.EmptyUndoBuffer()
                self.txtFile.SetSavePoint()
                self.OpenFile(False)
                self.txtFile.EmptyUndoBuffer()
                self.txtFile.SetSavePoint()
        event.Skip()

    # def OnRemoveAllBreakpoints(self, event):
    #     l = len(self.breakpoints)
    #     if (l > 0):
    #         d = MessageDialog(self, "This will remove all breakpoints\nAre you sure you want to do this?", "Rhee",
    #                           YES_NO | ICON_QUESTION)
    #         answer = d.ShowModal()
    #         d.Destroy()
    #         if (answer == ID_YES):
    #             l = self.txtFile.GetLineCount()
    #             x = 0
    #             while (x < l):
    #                 i = self.breakpoints.count(x)
    #                 if (i > 0):
    #                     i = self.breakpoints.index(x)
    #                     self.breakpoints.pop(i)
    #                 self.txtFile.MarkerDelete(x, 0)
    #                 x = x + 1
    #
    # def OnRemoveBreakpoint(self, event):
    #     l = len(self.breakpoints)
    #     if (l > 0):
    #         d = TextEntryDialog(self, "Line Number for the breakpoint:", "Add Breakpoint",
    #                             str(self.txtFile.GetCurrentLine() + 1))
    #         if d.ShowModal() == ID_OK:
    #             try:
    #                 x = int(d.GetValue()) - 1
    #             except:
    #                 d = ScrolledMessageDialog(self, "You must enter an integer (number, eg 1,2,128)", "Rhee")
    #                 d.ShowModal()
    #                 d.Destroy()
    #                 return
    #             try:
    #                 i = self.breakpoints.index(x)
    #             except:
    #                 d = ScrolledMessageDialog(self, "Breakpoint(" + str(x + 1) + ") does not exist", "Rhee")
    #                 d.ShowModal()
    #                 d.Destroy()
    #                 return
    #             self.breakpoints.pop(i)
    #             self.txtFile.MarkerDelete(x, 0)

    def OnRun(self, event):
        if (self.txtFile.GetModify()):
            d = MessageDialog(self,
                              u"फाइलमा बदलाव आएको छ\nकृपया फाइल सेव गरेर मात्रै चलाउनु होला\nफाइल सेव गर्न चाहनुहुन्छ ?",
                              u"ऋ", YES_NO | ICON_QUESTION)
            answer = d.ShowModal()
            d.Destroy()
            if (answer == ID_YES):
                self.OnSave(event)
            else:
                return
        largs = ""
        if (len(self.lastprogargs) > 0):
            largs = "\" " + self.lastprogargs


        self.outfile = os.path.join(os.path.split(self.filename)[0],'temp.py')
        compile_file(self.filename, self.outfile)
        # return

        if (Platform == '__WXMSW__'):
            cmd = pythexecw + " -u " + self.pythonargs + " \"" + self.outfile.replace("\\", "/") + largs
            self.runcommand((cmd),
                            event)
        else:
            cmd = pythexec + " -u " + self.pythonargs + " \"" + self.outfile.filename + largs
            self.runcommand((cmd), event)
        self.pytorhee, self.rheetopy = MapBreakPoints(self.breakpoints, self.outfile)
        self.Go = True

    def OnRunWithDebugger(self, event):

        if (self.txtFile.GetModify()):
            d = MessageDialog(self,
                              u"फाइलमा बदलाव आएको छ\nकृपया फाइल सेव गरेर मात्रै चलाउनु होला\nफाइल सेव गर्न चाहनुहुन्छ ?",
                              u"ऋ", YES_NO | ICON_QUESTION)
            answer = d.ShowModal()
            d.Destroy()
            if (answer == ID_YES):
                self.OnSave(event)
            else:
                return
        largs = ""
        if (len(self.lastprogargs) > 0):
            largs = "\" " + self.lastprogargs


        self.outfile = os.path.join(os.path.split(self.filename)[0],'temp.py')
        compile_file(self.filename, self.outfile)
        if (Platform == '__WXMSW__'):
            self.runcommand((pythexecw + " -u " + self.pythonargs + " \"" + pdbstring + "\" \"" + self.outfile.replace(
                "\\", "/") + largs), event)
        else:
            self.runcommand((pythexec + " -u " + self.pythonargs + " \"" + pdbstring + "\" \"" + self.outfile + largs),
                            event)

        self.DebugActive = True
        self.WatchWindow.Show()
        self.WatchWindow.restart(None)

        #TODO: smth
        self.pytorhee, self.rheetopy = MapBreakPoints(self.breakpoints, self.outfile)

        l = len(self.breakpoints)
        if (l > 0):
            x = 0
            while (x < l):
                if self.breakpoints[x] in self.rheetopy:
                    self.process.GetOutputStream().write("break " + str(self.rheetopy[self.breakpoints[x]] + 1) + '\n')
                x = x + 1

        time.sleep(1)
        print self.ReadImmediateStream()
        #Continue
        self.process.GetOutputStream().write('c\n')

        self.Go = True


    def OnSave(self, event):
        if (self.txtFile.GetModify()):
            if (len(self.filename) <= 0):
                self.OnSaveAs(event)
            else:
                self.SaveFile()
                self.txtFile.SetSavePoint()
            self.SetTitle(u"ऋ - " + self.filename)

    def OnSaveAs(self, event):
        dlg = FileDialog(self, "Save File As", "", "", wildcard, SAVE | OVERWRITE_PROMPT)
        if (len(self.ddirectory) > 0):
            try:
                dlg.SetDirectory(self.ddirectory)
            except:
                d = ScrolledMessageDialog(self, ("Error Setting Default Directory To: " + self.lastdirectory),
                                          "Rhee Error")
                d.ShowModal()
                d.Destroy()
        if (dlg.ShowModal() == ID_OK):
            self.filename = dlg.GetPath().replace("\\", "/")
            self.ddirectory = os.path.dirname(self.filename)
            # self.DestroyRecentFileMenu()
            self.SaveFile()
            #Update Recent Files
            self.toolbar.EnableTool(ID_RUN, True)
            self.toolbar.EnableTool(ID_FLOWCHART, True)
            self.toolbar.EnableTool(ID_SET_ARGS, True)
            self.programmenu.Enable(ID_RUN, True)
            self.programmenu.Enable(ID_SET_ARGS, True)
            if (self.recentfiles.count(self.filename) is not 0):
                self.ID_RECENT_FILES.pop(self.recentfiles.index(self.filename))
                self.recentfiles.remove(self.filename)
            if (len(self.recentfiles) is self.recentfileslimit):
                self.recentfiles.pop()
                self.ID_RECENT_FILES.pop()
            ti = len(self.ID_RECENT_FILES) - 1
            if (ti > -1):
                self.ID_RECENT_FILES.append(self.ID_RECENT_FILES[ti] + 1)
            else:
                self.ID_RECENT_FILES.append(ID_RECENT_FILES_BASE)
            self.recentfiles.insert(0, self.filename)
            # self.WriteRecentFiles()
            # self.CreateRecentFileMenu()
            self.txtFile.EmptyUndoBuffer()
            self.txtFile.SetSavePoint()
        dlg.Destroy()
        self.SetTitle(u"ऋ - " + self.filename)

    def OnSetArgs(self, event):
        if (len(self.filename) > 0):
            d = TextEntryDialog(self, 'Arguments:', 'Rhee - Set Arguments', self.lastprogargs)
        if (d.ShowModal() == ID_OK):
            self.lastprogargs = d.GetValue()
        d.Destroy()

    def OnTogglePrompt(self, event):
        if (self.promptisvisible):
            self.promptisvisible = False
            self.toolbar.ToggleTool(ID_TOGGLE_PROMPT, False)
            self.bSizer.Show(self.txtPrompt, False)
            if (self.txtPromptSize == 100):
                self.bSizer.Show(self.txtFile, True)
            self.bSizer.Layout()
        else:
            self.promptisvisible = True
            self.toolbar.ToggleTool(ID_TOGGLE_PROMPT, True)
            self.bSizer.Show(self.txtPrompt, True)
            if (self.txtPromptSize == 100):
                self.bSizer.Show(self.txtFile, False)
            self.bSizer.Layout()

    def OnToggleViewWhiteSpace(self, event):
        c = self.txtFile.GetViewWhiteSpace()
        if (c):
            self.txtFile.SetViewWhiteSpace(False)
            self.toolbar.ToggleTool(ID_TOGGLE_VIEWWHITESPACE, False)
        else:
            self.txtFile.SetViewWhiteSpace(True)
            self.toolbar.ToggleTool(ID_TOGGLE_VIEWWHITESPACE, True)

    def OnFlowchart(self, event):
        if (self.txtFile.GetModify()):
            d = MessageDialog(self,
                              u"फाइलमा बदलाव आएको छ\nकृपया फाइल सेव गरेर मात्रै चलाउनु होला\nफाइल सेव गर्न चाहनुहुन्छ ?",
                              u"ऋ", YES_NO | ICON_QUESTION)
            answer = d.ShowModal()
            d.Destroy()
            if (answer == ID_YES):
                self.OnSave(event)
            else:
                return
        # try:
        draw_file(self.filename, 'flowcharts')
        FlowChart(flowchartdir = 'flowcharts').Show()
        # except Exception, e:
            # pass


    def OnUnCommentRegion(self, event):
        selstart, selend = self.txtFile.GetSelection()
        #From the start of the first line selected
        start = self.txtFile.LineFromPosition(selstart)
        start = self.txtFile.GetLineIndentPosition(start) - self.txtFile.GetLineIndentation(start)
        #To the end of the last line selected
        end = self.txtFile.GetLineEndPosition(self.txtFile.LineFromPosition(selend))
        self.txtFile.SetSelection(start, end)
        text = self.txtFile.GetSelectedText()
        #Remove comments at the beginning of the line only.
        x = 1
        l = len(text)
        newtext = ""
        if not (text[0] == '#'):
            newtext = text[0]
        while (x < l):
            if (text[x] == '#'):
                style = self.txtFile.GetStyleAt(start + x)
                if not (text[x - 1] == '\n') or (
                    not (style == STC_P_COMMENTLINE) and not (style == STC_P_COMMENTBLOCK)):
                    newtext = newtext + text[x]
            else:
                newtext = newtext + text[x]
            x = x + 1
        self.txtFile.ReplaceSelection(newtext)

    def OpenFile(self, OpenInNewWindow):
        if (not os.path.exists(self.filename)):
            d = ScrolledMessageDialog(self, ("Error Opening: " + self.filename), "Rhee Error")
            d.ShowModal()
            d.Destroy()
            return
        if (self.recentfiles.count(self.filename) is not 0):
            self.ID_RECENT_FILES.pop()
            self.recentfiles.remove(self.filename)
        if (len(self.recentfiles) is self.recentfileslimit):
            self.recentfiles.pop()
            self.ID_RECENT_FILES.pop()
        ti = len(self.ID_RECENT_FILES) - 1
        if (ti > -1):
            self.ID_RECENT_FILES.append(self.ID_RECENT_FILES[ti] + 1)
        else:
            self.ID_RECENT_FILES.append(ID_RECENT_FILES_BASE)
        self.recentfiles.insert(0, self.filename)
        self.WriteRecentFiles()
        if (self.txtFile.GetModify()) or OpenInNewWindow:
            if (Platform == '__WXMSW__'):
                t = self.filename.replace("\\", "/")
            else:
                t = self.filename
            f = RheeFrame(None, -1, (u"ऋ - " + t), t)
            f.Show(True)
        else:
            try:
                cfile = file(self.filename, 'rb')
                oof = cfile.read().decode('utf-8')
                self.txtFile.SetText(oof+'\n')
                self.txtFile.EmptyUndoBuffer()
                self.txtFile.SetSavePoint()
                cfile.close()
                self.txtFile.SetScrollWidth(1)
                # return()
                #Check to see if scroll length is appropriate:

                counter = 0
                length = self.txtFile.GetLineCount()
                ll = self.txtFile.TextWidth(STC_STYLE_DEFAULT, "OOO")
                x = 0
                spaces = ""
                while (x < self.tabwidth):
                    spaces = spaces + " "
                    x = x + 1
                while (counter < length):
                    current_width = self.txtFile.GetScrollWidth()
                    line = self.txtFile.GetLine(counter).replace('\t', spaces)
                    actual_width = self.txtFile.TextWidth(STC_STYLE_DEFAULT, line)
                    if (current_width < actual_width):
                        self.txtFile.SetScrollWidth(actual_width + ll)
                    counter = counter + 1

                self.txtFile.SetXOffset(0)

                if (self.process is None):
                    self.toolbar.EnableTool(ID_RUN, True)
                    # self.toolbar.EnableTool(ID_FLOWCHART, True)
                    self.toolbar.EnableTool(ID_SET_ARGS, True)
                    self.programmenu.Enable(ID_RUN, True)
                    self.programmenu.Enable(ID_SET_ARGS, True)
                    self.toolbar.EnableTool(ID_PYTHON_DEBUGGER, True)
                    self.programmenu.Enable(ID_PYTHON_DEBUGGER, True)
                    self.toolbar.EnableTool(ID_RELOAD, True)
                    self.filemenu.Enable(ID_RELOAD, True)
                self.SetTitle(u"ऋ - " + self.filename)
                if (oof.find("\r\n") > -1):
                    emode = STC_EOL_CRLF
                    emodenum = 1
                elif (oof.find("\n") > -1):
                    emode = STC_EOL_LF
                    emodenum = 0
                elif (oof.find("\r") > -1):
                    emode = STC_EOL_CR
                    emodenum = 2
                else:
                    emode = self.eolmode

                if (self.eolmode == STC_EOL_LF):
                    dmodenum = 0
                elif (self.eolmode == STC_EOL_CRLF):
                    dmodenum = 1
                else:
                    dmodenum = 2

                if (emode == self.eolmode):
                    emodenum = dmodenum

                if (self.checkeol):
                    if (not emode == self.eolmode):
                        d = MessageDialog(self, (self.filename + " is currently " + FFMESSAGE[
                            emodenum] + ".\nWould you like to change it to the default?  The Default is: " + FFMESSAGE[
                                                     dmodenum]), "File Format", YES_NO | ICON_QUESTION)
                        answer = d.ShowModal()
                        d.Destroy()
                        if (answer == ID_YES):
                            self.txtFile.SetEOLMode(self.eolmode)
                            self.txtFile.ConvertEOLs(self.eolmode)
                            emodenum = dmodenum
                self.formatmenu.Check((ID_UNIXMODE + emodenum), True)
                self.ddirectory = os.path.dirname(self.filename)
            except IOError:
                d = ScrolledMessageDialog(self, ("Error Opening: " + self.filename), "Rhee Error")
                d.ShowModal()
                d.Destroy()

    def SaveFile(self):
        try:
            cfile = file(self.filename, 'wb')
            cfile.write(self.txtFile.GetText().encode('utf-8'))
            cfile.close()
        except IOError:
            d = ScrolledMessageDialog(self, ("Error Writing: " + self.filename), "Rhee Error")
            d.ShowModal()
            d.Destroy()

    def SetupPrefsFile(self):
        self.txtFile.SetEOLMode(self.eolmode)

        self.txtFile.SetViewWhiteSpace(self.whitespaceisvisible)

        self.txtFile.SetTabWidth(self.tabwidth)

        if (self.wordwrap):
            self.txtFile.SetWrapMode(STC_WRAP_WORD)
        else:
            self.txtFile.SetWrapMode(STC_WRAP_NONE)

        self.txtFile.StyleSetSpec(STC_STYLE_DEFAULT, self.txtFileStyleArray[0])

        self.txtFile.StyleClearAll()

        self.txtFile.StartStyling(0, 0xff)
        self.txtFile.StyleSetSpec(STC_STYLE_LINENUMBER, self.txtFileStyleArray[1])
        self.txtFile.StyleSetSpec(STC_STYLE_BRACELIGHT, self.txtFileStyleArray[2])
        self.txtFile.StyleSetSpec(STC_STYLE_BRACEBAD, self.txtFileStyleArray[3])
        self.txtFile.StyleSetSpec(STC_P_CHARACTER, self.txtFileStyleArray[4])
        self.txtFile.StyleSetSpec(STC_P_CLASSNAME, self.txtFileStyleArray[5])
        self.txtFile.StyleSetSpec(STC_P_COMMENTBLOCK, self.txtFileStyleArray[6])
        self.txtFile.StyleSetSpec(STC_P_COMMENTLINE, self.txtFileStyleArray[6])
        self.txtFile.StyleSetSpec(STC_P_DEFNAME, self.txtFileStyleArray[7])
        self.txtFile.StyleSetSpec(STC_P_WORD, self.txtFileStyleArray[8])
        self.txtFile.StyleSetSpec(STC_P_NUMBER, self.txtFileStyleArray[9])
        self.txtFile.StyleSetSpec(STC_P_OPERATOR, self.txtFileStyleArray[10])
        self.txtFile.StyleSetSpec(STC_P_STRING, self.txtFileStyleArray[11])
        self.txtFile.StyleSetSpec(STC_P_STRINGEOL, self.txtFileStyleArray[11])
        self.txtFile.StyleSetSpec(STC_P_TRIPLE, self.txtFileStyleArray[12])
        self.txtFile.StyleSetSpec(STC_P_TRIPLEDOUBLE, self.txtFileStyleArray[12])
        self.txtFile.SetCaretForeground(self.txtFileStyleArray[13])
        self.txtFile.SetSelForeground(1, self.txtFileStyleArray[14])
        self.txtFile.SetSelBackground(1, self.txtFileStyleArray[15])

    def SetupPrefsPrompt(self):
        self.txtPrompt.SetWrapMode(STC_WRAP_WORD)
        self.txtPrompt.SetEOLMode(self.eolmode)
        self.txtPrompt.StyleSetSpec(STC_STYLE_DEFAULT, self.txtPromptStyleArray[0])
        self.txtPrompt.SetCaretForeground(self.txtPromptStyleArray[1])
        self.txtPrompt.StyleClearAll()

        self.txtPrompt.StartStyling(0, 0xff)

    def SetupToolBar(self):

        self.toolbar.SetToolBitmapSize(Size(self.iconsize*2, self.iconsize*2))
        iconsizestr = str(self.iconsize) + ".xpm"
        self.toolbar.AddSimpleTool(ID_NEW, Bitmap((bitmapdirectory + "/new" + iconsizestr), BITMAP_TYPE_XPM), u"नया",
                                   u"नया फाइल बनाउ")
        self.toolbar.AddSimpleTool(ID_OPEN, Bitmap((bitmapdirectory + "/open" + iconsizestr), BITMAP_TYPE_XPM), u"खोल",
                                   u"रहेको फाइल खोल")

        # self.toolbar.AddSimpleTool(ID_RELOAD, Bitmap((bitmapdirectory + "/reload" + iconsizestr), BITMAP_TYPE_XPM),
        #                            "Reload", "Reload the current file")
        self.toolbar.AddSimpleTool(ID_CLOSE, Bitmap((bitmapdirectory + "/close" + iconsizestr), BITMAP_TYPE_XPM),
                                   u"बन्द", u"फाइल बन्द गर")
        self.toolbar.AddSimpleTool(ID_SAVE, Bitmap((bitmapdirectory + "/save" + iconsizestr), BITMAP_TYPE_XPM), u"सेव",
                                   u"फाइल सेव गर")
        self.toolbar.AddSeparator()
        self.toolbar.AddSeparator()
        self.toolbar.AddSeparator()
        self.toolbar.AddSimpleTool(ID_FIND, Bitmap((bitmapdirectory + "/find" + iconsizestr), BITMAP_TYPE_XPM), u"खोज",
                                   u"फाइलमा शब्द खोज")
        self.toolbar.AddSimpleTool(ID_REPLACE, Bitmap((bitmapdirectory + "/replace" + iconsizestr), BITMAP_TYPE_XPM),
                                   u"रिप्लेस", u"शब्दहरु रिप्लेस गर")

        # self.toolbar.AddSimpleTool(ID_PREFS, Bitmap((bitmapdirectory + "/prefs" + iconsizestr), BITMAP_TYPE_XPM),
        #                            "Preferences", "Customize Rhee")
        # self.toolbar.AddSimpleTool(ID_TOGGLE_PROMPT,
        #                            Bitmap((bitmapdirectory + "/prompt" + iconsizestr), BITMAP_TYPE_XPM),
        #                            "Toggle Prompt", "Toggle Prompt", ITEM_CHECK)
        # self.toolbar.AddSimpleTool(ID_TOGGLE_VIEWWHITESPACE,
        #                            Bitmap((bitmapdirectory + "/whitespace" + iconsizestr), BITMAP_TYPE_XPM),
        #                            "Toggle View Whitespace", "Toggle View Whitespace", ITEM_CHECK)
        # self.toolbar.ToggleTool(ID_TOGGLE_PROMPT, self.promptisvisible)
        # self.toolbar.ToggleTool(ID_TOGGLE_VIEWWHITESPACE, self.whitespaceisvisible)
        self.toolbar.AddSeparator()
        self.toolbar.AddSeparator()
        self.toolbar.AddSeparator()
        self.toolbar.AddSimpleTool(ID_RUN, Bitmap((bitmapdirectory + "/run" + iconsizestr), BITMAP_TYPE_XPM), u"चलाउ",
                                   u"कोड चलाउ")
        # self.toolbar.AddSimpleTool(ID_SET_ARGS, Bitmap((bitmapdirectory + "/setargs" + iconsizestr), BITMAP_TYPE_XPM),
        #                            "Set Arguments", "Set Arguments")
        # self.toolbar.AddSimpleTool(ID_PYTHON, Bitmap((bitmapdirectory + "/python" + iconsizestr), BITMAP_TYPE_XPM),
        #                            "Python", "Run The Python Interpreter")
        self.toolbar.AddSimpleTool(ID_PYTHON_DEBUGGER,
                                   Bitmap((bitmapdirectory + "/debug" + iconsizestr), BITMAP_TYPE_XPM),
                                   u"डिबग", u"कोड डिबग गर")
        self.toolbar.AddSimpleTool(ID_END, Bitmap((bitmapdirectory + "/stop" + iconsizestr), BITMAP_TYPE_XPM), u"रोक",
                                   u"कोड रोक")

        self.toolbar.AddSeparator()
        self.toolbar.AddSeparator()
        self.toolbar.AddSeparator()
        self.toolbar.AddSimpleTool(ID_FLOWCHART, Bitmap((bitmapdirectory + "/flowchart.png"), BITMAP_TYPE_PNG), u"फ्लोचार्ट",
                                   u"कोड रोक")

        if (len(self.filename) < 1):
            # self.toolbar.EnableTool(ID_RELOAD, False)
            # self.toolbar.EnableTool(ID_RUN, False)
            # self.toolbar.EnableTool(ID_SET_ARGS, False)
            # self.toolbar.EnableTool(ID_PYTHON_DEBUGGER, False)
            pass
        if (self.pid is -1):
            self.toolbar.EnableTool(ID_END, False)

        else:
            self.toolbar.EnableTool(ID_RUN, False)
            # self.toolbar.EnableTool(ID_FLOWCHART, False)
            self.toolbar.EnableTool(ID_SET_ARGS, False)
            self.toolbar.EnableTool(ID_PYTHON, False)
            self.toolbar.EnableTool(ID_PYTHON_DEBUGGER, False)

        self.toolbarsize = 21

        self.toolbar.Realize()

    def replace_all(self, ftext, rtext, flags):
        p = self.txtFile.FindText(0, self.txtFile.GetLength(), ftext, flags)
        x = 0
        while (p is not -1):
            self.txtFile.GotoPos(p)
            self.txtFile.SetTargetStart(p)
            self.txtFile.SetTargetEnd(p + len(ftext))
            self.txtFile.ReplaceTarget(rtext)
            p = self.txtFile.FindText((p + 1), self.txtFile.GetLength(), ftext, flags)
            x = x + 1
        return x

    def runcommand(self, command, event):
        if (len(self.filename) > 0) and (self.pid is -1):
            self.toolbar.EnableTool(ID_RUN, False)
            # self.toolbar.EnableTool(ID_FLOWCHART, False)
            self.toolbar.EnableTool(ID_SET_ARGS, False)
            self.toolbar.EnableTool(ID_PYTHON, False)
            self.toolbar.EnableTool(ID_PYTHON_DEBUGGER, False)
            self.toolbar.EnableTool(ID_END, True)
            self.programmenu.Enable(ID_RUN, False)
            self.programmenu.Enable(ID_SET_ARGS, False)
            self.programmenu.Enable(ID_PYTHON, False)
            self.programmenu.Enable(ID_PYTHON_DEBUGGER, False)
            self.programmenu.Enable(ID_END, True)
            self.toolbar.ToggleTool(ID_TOGGLE_PROMPT, True)
            if (not self.promptisvisible):
                self.promptisvisible = True
                if (self.txtPromptSize == 100):
                    self.bSizer.Show(self.txtFile, False)
                self.bSizer.Show(self.txtPrompt, True)
                self.bSizer.Layout()
            self.txtPrompt.SetReadOnly(0)
            self.txtPrompt.ClearAll()
            self.txtPrompt.editpoint = 0
            self.needToUpdatePos = True
            if (len(self.filename) > 0):
                try:
                    cdir = self.filename[0:self.filename.rindex('/')]
                    os.chdir(cdir)
                except:
                    d = ScrolledMessageDialog(self, "Error Setting current directory for Python.", "Rhee RunError")
                    d.ShowModal()
                    d.Destroy()
            self.SetStatusText(self.filename + u" चलाउदै " )
            self.process = Process(self)
            self.process.Redirect()
            if (Platform == '__WXMSW__'):
                self.pid = Execute(command, EXEC_ASYNC | EXEC_NOHIDE, self.process)
            else:
                self.pid = Execute(command, EXEC_ASYNC, self.process)
            self.txtPrompt.SetFocus()

    def RunShortcuts(self, event):
        keycode = event.GetKeyCode()
        if ((keycode + ord('a') - 1) == ord('n')):
            self.OnNew(event)
        elif ((keycode + ord('a') - 1) == ord('s')):
            if event.m_shiftDown:
                self.OnSaveAs(event)
            else:
                self.OnSave(event)
        elif ((keycode + ord('a') - 1) == ord('o')):
            self.OnOpen(event)
        elif ((keycode + ord('a') - 1) == ord('p')):
            self.OnPython(event)
        elif ((keycode + ord('a') - 1) == ord('r')):
            self.OnRun(event)
        elif ((keycode + ord('a') - 1) == ord('d')):
            self.OnRunWithDebugger(event)
        elif ((keycode + ord('a') - 1) == ord('e')):
            self.OnEnd(event)
        elif ((keycode + ord('a') - 1) == ord('f')):
            self.OnMenuFind(event)
        elif (keycode == WXK_F3):
            self.OnMenuFindNext(event)
        elif ((keycode + ord('a') - 1) == ord('g')):
            self.OnGoTo(event)
        elif (keycode == WXK_F6):
            self.OnTogglePrompt(event)
        elif (keycode == WXK_F5):
            # self.Maximize(not self.IsMaximized())
            self.WriteDebugString('c\n')

        elif (keycode == WXK_F2):
            self.OnAddBreakpoint(event)
        elif (keycode == WXK_F8):
            # if self.WaitingForDebugInput:
            #TODO: Figure out the step in pattern
            self.WriteDebugString('n\n')
        elif (keycode == WXK_F7):
            # if self.WaitingForDebugInput:
            #TODO: Figure out the step in pattern
            self.WriteDebugString('s\n')

        event.Skip()

    def WriteRecentFiles(self):
        try:
            fin = open((homedirectory + "/recent_files.log"), 'w')
            x = 0
            length = len(self.recentfiles)
            while (x < self.recentfileslimit) and (x < length):
                fin.write(self.recentfiles[x] + '\n')
                x = x + 1
            fin.close()
        except IOError:
            d = ScrolledMessageDialog(self, ("Error Writing: " + fin), "Recent Files Error")
            d.ShowModal()
            d.Destroy()
