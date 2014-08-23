#encoding=utf8
from wx import *
from wx.stc import *
from RheeVariables import *
from wx.grid import *


map_num = {'0':u'\u0966', '1':u'\u0967', '2':u'\u0968', '3':u'\u0969',
            '4':u'\u096a', '5':u'\u096b', '6':u'\u096c', '7':u'\u096d',
            '8':u'\u096e' ,'9':u'\u096f'
            }

def to_uni(ascii):
    temp = ''
    for digit in ascii:
        temp += map_num[digit] if (digit in map_num) else digit
    return temp

def str_to_unicode( st):
    n = st[1:]
    return n.decode('hex').decode('utf-8')

class RheeWatch(wx.Frame):

    def __init__(self, parent):

        Frame.__init__(self, parent, ID_ANY, u"वाच", Point(0,0),Size(300,200), style=DEFAULT_DIALOG_STYLE)#)

        # Create a wxGrid object
        panel = Panel(self, ID_ANY)
        self.grid = Grid(panel, ID_ANY)

        self.bSizer = BoxSizer(VERTICAL)

        panel.SetAutoLayout(True)
        panel.SetSizer(self.bSizer)

        # Then we call CreateGrid to set the dimensions of the grid
        # (100 rows and 10 columns in this example)
        self.grid.CreateGrid(10, 2)

        self.bSizer.Fit(panel)
        # We can set the sizes of individual rows and columns
        # in pixels
        # grid.SetRowSize(0, 60)
        # grid.SetColSize(0, 120)
        self.grid.SetColSize(1, 250)
        self.grid.SetRowLabelSize(0)
        self.grid.SetColLabelSize(0)
        # And set grid cell contents as strings
        self.grid.SetCellValue(0, 0, u'रहे')

        # We can specify that some cells are read.only
        self.grid.SetCellValue(0, 1, 'This is read.only')
        self.grid.SetReadOnly(0, 1)
        self.bSizer.Add(self.grid, 1, EXPAND|ALL, 5)
        # self.restart({'a':123, 'b':3112, 'c':"This is all lie!!"})
        # self.grid.GetGridWindow().Bind(EVT_MOTION, self.onMouseOver)
        # self.grid.SetToolTip()



    def restart(self, variables):
        self.grid.ClearGrid()
        if self.grid.NumberRows: self.grid.DeleteRows(0, self.grid.NumberRows)
        if variables:
            num_vars = len(variables)
            self.grid.AppendRows(num_vars)
            i = 0
            for key, value in variables.iteritems():
                # value = value[1:-1]
                self.grid.SetCellValue(i, 0, str_to_unicode(key))
                if str(value).replace('.','').isdigit():
                    value = to_uni(value)
                else:
                    value = unicode(value)
                self.grid.SetCellValue(i, 1, value)
                i += 1

    def onMouseOver(self, event):
        '''
        Method to calculate where the mouse is pointing and
        then set the tooltip dynamically.
        '''

        # Use CalcUnscrolledPosition() to get the mouse position
        # within the
        # entire grid including what's offscreen
        x, y = self.grid.CalcUnscrolledPosition(event.GetX(),event.GetY())
        # self.grid.Cell
        coords = self.grid.XYToCell(x, y)
        # you only need these if you need the value in the cell
        row = coords[0]
        col = coords[1]
        if 0<=col<self.grid.NumberCols and 0<=row<self.grid.NumberRows:
            val = self.grid.GetCellValue(row, col)
            if val:
                event.GetEventObject().SetToolTipString(val)
                event.GetEventObject().ToolTip.GetWindow().SetSize(Size(500,500))
                # event.GetEventObject().SetToolTipSize(100,100)
        event.Skip()