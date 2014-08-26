import wx
import os
import wx.lib.scrolledpanel as scrolled
# Some classes to use for the notebook pages.  Obviously you would
# want to use something more meaningful for your application, these
# are just for illustration.


class FlowChartPage(scrolled.ScrolledPanel):
    def __init__(self, parent, imageFile):
        scrolled.ScrolledPanel.__init__(self, parent, style=wx.SUNKEN_BORDER | wx.HSCROLL | wx.VSCROLL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        png = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        sb = wx.StaticBitmap(self, -1, png, (0, 0), (png.GetWidth(), png.GetHeight()))
        # sizer.AddSpacer(10)
        sizer.Add(sb,1, flag= wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)
        self.SetAutoLayout(1)

        # self.SetupScrolling()
        # self.EnableScrolling()
        # self.Refresh()
        # print self.GetScaleX()
        # print self.GetScaleY()
        # self.SetScale(10,10)
        self.SetupScrolling()
        # self.Bind(wx.EVT_PAINT, self.OnPaint)
        # sb.Bind(wx.EVT_MOTION, self.OnMove)
        # sb.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        # sb.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        # self.IsRectReady = False


class MainFrame(wx.Frame):
    def __init__(self, flowchartdir):
        wx.Frame.__init__(self, None, title="Simple Notebook Example")

        pages = []

        p = wx.Panel(self)
        nb = wx.Notebook(p)

        for file in os.listdir(flowchartdir):
            fullfile = os.path.join(flowchartdir, file)
            if os.path.isfile(fullfile) and file[-3:] == 'png':

                nb.AddPage(FlowChartPage(nb, fullfile), file)

        # Here we create a panel and a notebook on the panel


        # create the page windows as children of the notebook
        # page1 = PageOne(nb)
        # page2 = PageTwo(nb)
        # page3 = PageThree(nb)

        # add the pages to the notebook with the label to show on the tab
        # nb.AddPage(page1, "Page 1")
        # nb.AddPage(page2, "Page 2")
        # nb.AddPage(page3, "Page 3")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.GROW)
        sizer.Fit(nb)
        p.SetSizer(sizer)


if __name__ == "__main__":
    app = wx.App()
    MainFrame(flowchartdir='flowcharts\\').Show()
    app.MainLoop()