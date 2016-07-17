# -*- coding: utf-8 -*
import wx
import matplotlib
matplotlib.use("WxAgg")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure


class MatplotlibPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.toolbar = self.add_toolbar()

        self.SetSizer(self.sizer)
        self.Fit()

    def add_toolbar(self):
        toolbar = NavigationToolbar2Wx(self.canvas)
        toolbar.Realize()
        self.sizer.Add(toolbar, 0, wx.ALIGN_CENTER | wx.EXPAND)
        toolbar.update()
        return toolbar

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, title='demo app')
    p = MatplotlibPanel(frame)
    frame.Show(True)
    app.MainLoop()
