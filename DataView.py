# -*- coding: utf-8 -*
import wx
from MatplotlibView import MatplotlibPanel
from CheckListWithFilterView import CheckListWithFilterPanel

class DataFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)

        self.panel = panel = wx.Panel(self)

        main_box = wx.BoxSizer(wx.VERTICAL)
        # ======== graph panel ========
        self.graph = graph = MatplotlibPanel(panel)
        main_box.Add(graph, 1, wx.EXPAND)

        # ======== firmware list ========
        self.firmware_list = firmware_list = CheckListWithFilterPanel(panel)
        main_box.Add(firmware_list, 0, wx.EXPAND)

        panel.SetSizerAndFit(main_box)
        self.Fit()
        self.Show(True)

if __name__ == '__main__':
    app = wx.App()
    frame = DataFrame(None, 'DataView')
    app.MainLoop()

