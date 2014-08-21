#encoding=utf8
from wx import *
from wx.stc import *
from RheeVariables import *

class RheeText(StyledTextCtrl):
    def __init__(self, parent, id):
        StyledTextCtrl.__init__(self, parent, id)

        self.SetMarginType(0, STC_MARGIN_SYMBOL)
        self.SetMarginType(1, STC_MARGIN_NUMBER)
        self.SetMarginWidth(0, 10)
        self.SetMarginWidth(1, 41)
        self.SetMarginWidth(2, 0)

        self.MarkerDefine(0, STC_MARK_ARROW)
        self.SetScrollWidth(1)

        print self.AutoCompGetSeparator()
        print self.AutoCompGetDropRestOfWord()
        self.AutoCompSetAutoHide(False)
        self.AutoCompSetDropRestOfWord(True)
        # self.AutoCompSetFillUps('a')

        self.RegisterImage(1, Bitmap(bitmapdirectory + '/reload24.xpm') )
        self.RegisterImage(2, Bitmap(bitmapdirectory + '/reload24.xpm') )
        self.RegisterImage(3, Bitmap(bitmapdirectory + '/reload24.xpm') )

        EVT_STC_MODIFIED(parent, id, self.OnModified)
        EVT_UPDATE_UI(self, id, self.OnUpdateUI)
        EVT_KEY_DOWN(self, self.OnKeyDown)
        EVT_CHAR(self, self.OnChar)
        EVT_STC_USERLISTSELECTION(self, id, self.OnUserListSelection)

    def OnModified(self, event):
        if (self.GetModify()):
            if (len(self.GetParent().filename) <= 0):
                self.GetParent().SetTitle(u"ऋ - नया फाइल*")
            elif (self.GetParent().GetTitle().find('*') == -1):
                self.GetParent().SetTitle(u"ऋ - " + self.GetParent().filename + "*")
        if (self.GetParent().txtFile.CanUndo() == False):
            self.GetParent().txtFile.SetSavePoint()
            if (len(self.GetParent().filename) <= 0):
                self.GetParent().SetTitle(u"ऋ - नया फाइल")
            else:
                self.GetParent().SetTitle(u"ऋ - " + self.GetParent().filename)
        ll = self.TextWidth(STC_STYLE_DEFAULT, "OOO")
        x = 0
        spaces = ""
        while (x < self.GetParent().tabwidth):
            spaces = spaces + " "
            x = x + 1
        current_width = self.GetScrollWidth()
        line = self.GetCurLine()[0].replace('\t', spaces)
        actual_width = self.TextWidth(STC_STYLE_DEFAULT, line)
        if (current_width < actual_width):
            self.SetScrollWidth(actual_width + ll)

    def OnUpdateUI(self, event):
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        charAfter = None
        caretPos = self.GetCurrentPos()
        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # check before
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)
        if charAfter and chr(charAfter) in "[]{}()" and styleAfter == STC_P_OPERATOR:
            braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1 and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()
        pos = self.GetCurrentPos()
        # event.Skip()
        if (keycode == WXK_RETURN) and (self.GetParent().autoindent) and not self.AutoCompActive():
            line = self.GetLine(self.GetCurrentLine())
            pos = self.GetCurrentPos()
            self.GotoLine(self.LineFromPosition(pos))
            sop = pos - self.GetCurrentPos()
            self.GotoPos(pos)
            line = line[0:sop]
            numtabs = line.count('\t')
            self.AddText('\n')
            x = 0
            while (x < numtabs):
                self.AddText('\t')
                x = x + 1
        else:
            event.Skip()

    def OnChar(self, event):
        self.GetParent().RunShortcuts(event)
        # print self.GetCurrentPos()
        # if self.GetCurrentLine() != 0:      #the autcomp was showing wierd behavior at first line, so cancel it
        list = [u"रामरामराम?1", u"हरिहरि?1",u"कालमहिमा?2", u"रामायन?2"]
        # list = ["public?1", "private?2", "nothing?3", "everything?3"]
        # if not self.AutoCompActive():
        # self.AutoCompShow(3, u" ".join(sorted(list)))
        if event.GetKeyCode() ==WXK_SPACE or event.GetKeyCode() == WXK_RETURN: return
        l = self.GetCurrentPos()
        ip, fp = self.GetCurrentWord(l)
        self.SetSelectionStart(ip)
        self.SetSelectionEnd(fp+1)
        word = self.GetSelectedText()
        self.SetSelectionStart(l)
        self.SetSelectionEnd(l)
        if len(word)>=3:
            predictions = u" ".join(filter(lambda x: word in x or x in word,sorted(list)))
            if predictions:
                self.UserListShow(2, predictions)

            else:
                self.AutoCompCancel()
        else:
            self.AutoCompCancel()

            # self.AutoCompSelect(u"रामा")
        # self.AutoCompShow(3, "")

    def GetCurrentWord(self, pos):
        # returns ip, fp: ip=initial position, fp=final position
        ip, fp = 0, self.GetLength()-1
        p = pos-1
        cl = self.GetCurrentLine()
        delimiters = [ord(i) for i in [' ', '\n', '\t', '(', ')', '[', ']']]
        while p!=-1:
            c = self.GetCharAt(p)
            # print chr(c)
            if c in delimiters:
                ip = p+1
                break
            p-=1

        p = pos
        while p!=self.GetLength():

            c = self.GetCharAt(p)
            # print chr(c)
            if c in delimiters:
                fp = p-1
                break
            p+=1
        return ip, fp

    def OnUserListSelection(self, event):
        print event.GetText()
        ip, fp = self.GetCurrentWord(self.GetCurrentPos())
        self.SetSelectionStart(ip)
        self.SetSelectionEnd(fp+1)
        self.ReplaceSelection(event.GetText())
        # self.DropTarget()
        newpos = ip+len(event.GetText().encode('utf-8'))
        self.SetSelectionStart(newpos)
        self.SetSelectionEnd(newpos)
        pass
