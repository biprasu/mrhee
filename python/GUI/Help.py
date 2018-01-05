
from wx import *
from wx.html import *


class HelpDialog(Dialog):
    def __init__(self, parent, title, programdirectory):
        Dialog.__init__(self, parent, -1, title, Point(50, 50), Size(640, 480),
                        DEFAULT_DIALOG_STYLE | MAXIMIZE_BOX | THICK_FRAME | RESIZE_BORDER)

        self.theSizer = BoxSizer(VERTICAL)

        htmlwin = HtmlWindow(self, -1, Point(0, 0), Size(400, 200))
        self.theSizer.Add(htmlwin, 15, EXPAND)

        InitAllImageHandlers()

        htmlwin.LoadPage(programdirectory + "documentation/help.html")

        self.btnClose = Button(self, 101, "&Close")
        self.theSizer.Add(self.btnClose, 1, EXPAND)
        self.btnClose.SetDefault()

        self.SetAutoLayout(True)
        self.SetSizer(self.theSizer)

        EVT_BUTTON(self, 101, self.OnbtnClose)

    def OnbtnClose(self, event):
        self.EndModal(0)