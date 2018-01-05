from wx import *
from wx.stc import *
from RheeVariables import *



class RheePrompt(StyledTextCtrl):
    def __init__(self, parent, id):
        StyledTextCtrl.__init__(self, parent, id)

        self.CommandArray = []
        self.CommandArrayPos = -1

        self.SetMarginWidth(0, 0)
        self.SetMarginWidth(1, 0)
        self.SetMarginWidth(2, 0)

        EVT_KEY_DOWN(self, self.OnKeyDown)
        EVT_KEY_UP(self, self.OnKeyUp)
        EVT_UPDATE_UI(self, id, self.RunCheck)
        EVT_CHAR(self, self.OnChar)
        self.editpoint = 0

    def RunCheck(self, event):
        if (self.GetCurrentPos() < self.editpoint) or (self.GetParent().pid == -1) or self.Parent.WaitingForDebugInput:
            self.SetReadOnly(1)
        else:
            self.SetReadOnly(0)

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()
        pos = self.GetCurrentPos()
        if self.GetParent().pid != -1 and not self.Parent.WaitingForDebugInput:
            if (pos >= self.editpoint) and (keycode == WXK_RETURN):
                text = self.GetTextRange(self.GetParent().writeposition, self.GetLength())
                l = len(self.CommandArray)
                if (l < MAX_PROMPT_COMMANDS):
                    self.CommandArray.insert(0, text)
                    self.CommandArrayPos = -1
                else:
                    self.CommandArray.pop()
                    self.CommandArray.insert(0, text)
                    self.CommandArrayPos = -1
                self.GetParent().process.GetOutputStream().write(text.encode('utf8') + '\n')
                self.GotoPos(self.GetLength())
            if (keycode == WXK_UP):
                l = len(self.CommandArray)
                if (len(self.CommandArray) > 0):
                    if (self.CommandArrayPos + 1) < l:
                        self.GotoPos(self.editpoint)
                        self.SetTargetStart(self.editpoint)
                        self.SetTargetEnd(self.GetLength())
                        self.CommandArrayPos = self.CommandArrayPos + 1
                        self.ReplaceTarget(self.CommandArray[self.CommandArrayPos])

            elif (keycode == WXK_DOWN):
                if (len(self.CommandArray) > 0):
                    self.GotoPos(self.editpoint)
                    self.SetTargetStart(self.editpoint)
                    self.SetTargetEnd(self.GetLength())
                    if (self.CommandArrayPos - 1) > -1:
                        self.CommandArrayPos = self.CommandArrayPos - 1
                        self.ReplaceTarget(self.CommandArray[self.CommandArrayPos])
                    else:
                        if (self.CommandArrayPos - 1) > -2:
                            self.CommandArrayPos = self.CommandArrayPos - 1
                        self.ReplaceTarget("")
        if ((pos > self.editpoint) and (not keycode == WXK_UP)) or (
                    (not keycode == WXK_BACK) and (not keycode == WXK_LEFT) and (not keycode == WXK_UP) and (
                    not keycode == WXK_DOWN)):
            if (pos < self.editpoint):
                if (not keycode == WXK_RIGHT):
                    event.Skip()
            else:
                event.Skip()

    def OnKeyUp(self, event):
        keycode = event.GetKeyCode()
        pos = self.GetCurrentPos()
        if keycode == WXK_HOME:
            if (self.GetCurrentPos() < self.editpoint):
                self.GotoPos(self.editpoint)
            return
        elif keycode == WXK_PAGEUP :
            if (self.GetCurrentPos() < self.editpoint):
                self.GotoPos(self.editpoint)
            return
        event.Skip()

    def OnChar(self, event):
        self.GetParent().RunShortcuts(event)
