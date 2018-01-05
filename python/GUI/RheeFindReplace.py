#encoding=utf8
from wx import *
#
# class RheeFindReplaceDialog(Dialog):
#     def __init__(self, *args, **kwargs):
#         Dialog.__init__(self, *args, **kwargs)
#         self.InitUI()
#         self.SetSize((300, 140))
#         self.SetTitle(u"खोज राख")
#
#     def InitUI(self):
#         pnl = wx.Panel(self)
#         vbox = wx.BoxSizer(wx.HORIZONTAL)
#
#         sb = wx.StaticBox(pnl, label=u'खोज')
#         sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
#         # sbs.Add(wx.RadioButton(pnl, label='256 Colors',
#         #     style=wx.RB_GROUP))
#         # sbs.Add(wx.RadioButton(pnl, label='16 Colors'))
#         # sbs.Add(wx.RadioButton(pnl, label='2 Colors'))
#
#         hbox1 = wx.BoxSizer(wx.HORIZONTAL)
#         # hbox1.Add(wx.RadioButton(pnl, label='Custom'))
#         findtextlabel = wx.StaticText(pnl, label=u'खोज्ने शब्द')
#
#
#         hbox1.Add(findtextlabel,flag=wx.LEFT, border=5)
#         hbox1.AddSpacer(10)
#         self.findtext = wx.TextCtrl(pnl)
#         w,h = self.findtext.GetSize()
#         # self.findtext.SetSize((600,h))
#         hbox1.Add(self.findtext,flag=wx.LEFT|wx.RIGHT, border=5)
#         sbs.Add(hbox1)
#
#         hbox3 = wx.BoxSizer(wx.HORIZONTAL)
#         # hbox3.Add(wx.RadioButton(pnl, label='Custom'))
#         replacetextlabel = wx.StaticText(pnl, label=u'राख्ने शब्द')
#
#         sbs.AddSpacer(15)
#         hbox3.Add(replacetextlabel,flag=wx.LEFT, border=5)
#         hbox3.AddSpacer(18)
#         self.replacetext = wx.TextCtrl(pnl)
#         hbox3.Add(self.replacetext,flag=wx.LEFT, border=5)
#         sbs.Add(hbox3)
#
#         pnl.SetSizer(sbs)
#
#         hbox2 = wx.BoxSizer(wx.VERTICAL)
#         okButton = wx.Button(self, label=u'खोज')
#         replaceButton = wx.Button(self, label=u'राख')
#         closeButton = wx.Button(self, label=u'हटाउ')
#         hbox2.Add(okButton,flag=wx.EXPAND)
#         hbox2.AddSpacer(10)
#         hbox2.Add(replaceButton, flag=wx.EXPAND)
#         hbox2.AddSpacer(10)
#         hbox2.Add(closeButton, flag=wx.EXPAND)
#
#         vbox.Add(pnl, proportion=4,
#             flag=wx.ALL|wx.EXPAND, border=5)
#         vbox.Add(hbox2,proportion=0.25,
#             flag=wx.TOP|wx.BOTTOM, border=10)
#
#         self.SetSizer(vbox)
#
#         okButton.Bind(wx.EVT_BUTTON, self.OnClose)
#         closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
#
#     def OnClose(self, e):
#
#         self.Destroy()
#

class RheeFindReplaceDialog(Dialog):
    def __init__(self, parent, id,title, findstring='',findreplace=False):
        Dialog.__init__(self, parent, id, title, Point(50, 50), Size(350, 160))

        self.ID_SWITCH = 3001
        # self.ID_CANCEL = 3002
        self.ID_REPLACE = 3003

        self.findreplace = findreplace




        if self.findreplace:
            self.txtA = TextCtrl(self, id, "", Point(60, 10), Size(270, 25))
            stA = StaticText(self, id, u"खोज: ", Point(10, 10))
        else:
            self.txtA = TextCtrl(self, id, "", Point(60, 25), Size(270, 25))
            stA = StaticText(self, id, u"खोज: ", Point(10, 25))
        if findstring:
            self.txtA.SetValue(findstring)
        self.txtA.SetFocus()
        if self.findreplace:
            self.txtB = TextCtrl(self, id, "", Point(60, 40), Size(270, 25))
            stB = StaticText(self, id, u"राख:   ", Point(10, 40))

        # self.chkCase = CheckBox(self, id, "&Match Case", Point(10, 75))
        self.chkWholeWord = CheckBox(self, id, u"सम्पुर्ण शब्द मात्र", Point(10, 75))

        self.btnSwitch = Button(self, self.ID_SWITCH, u"खोज", Point(160, 85))
        self.btnSwitch.SetDefault()
        if self.findreplace:
            self.btnReplace = Button(self, self.ID_REPLACE, u"राख", Point(250, 85))
        EVT_BUTTON(self, self.ID_SWITCH, self.OnbtnSwitch)
        EVT_BUTTON(self, self.ID_REPLACE, self.OnbtnReplace)

        self.textA = ""
        self.textB = ""
        self.flags = FR_DOWN
        self.findnext = False


    def IsValidText(self):
        return ((len(self.textA) > 0) and (len(self.textB) > 0))

    def OnbtnSwitch(self, event):

        event = wx._windows.FindDialogEvent()
        if self.findnext:
            event.SetEventType(EVT_COMMAND_FIND_NEXT.typeId)
        else:
            event.SetEventType(EVT_COMMAND_FIND.typeId)
        event.SetFindString(self.txtA.GetValue())
        if (self.chkWholeWord.IsChecked()):
            event.SetFlags(FR_WHOLEWORD)
        wx.PostEvent(self.Parent.GetEventHandler(), event)
        # self.textA = self.txtA.GetValue()
        # self.textB = self.txtB.GetValue()
        # if (self.chkCase.IsChecked()):
        #     self.flags = self.flags + FR_WHOLEWORD
        self.findnext = True
        # self.EndModal(0)

    def OnbtnReplace(self, event):
        event = wx._windows.FindDialogEvent()
        event.SetEventType(EVT_COMMAND_FIND_REPLACE.typeId)
        event.SetFindString(self.txtA.GetValue())
        event.SetReplaceString(self.txtB.GetValue())
        if (self.chkWholeWord.IsChecked()):
            event.SetFlags(FR_WHOLEWORD)
        wx.PostEvent(self.Parent.GetEventHandler(), event)
        # self.textA = self.txtA.GetValue()
        # self.textB = self.txtB.GetValue()
        # if (self.chkCase.IsChecked()):
        #     self.flags = self.flags + FR_WHOLEWORD


