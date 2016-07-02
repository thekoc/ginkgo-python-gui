# -*- coding: utf-8 -*

import wx
import wx.lib.scrolledpanel

class SelectorFrame(wx.Frame):
    """选择时间, case 等的界面."""
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(300, 300))
        self.panel = panel = wx.Panel(self)
        main_box = wx.BoxSizer(wx.VERTICAL)

        date_box = wx.BoxSizer(wx.HORIZONTAL)
        self.start_date_ctrl = start_date = wx.DatePickerCtrl(panel, -1, style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        date_box.Add(wx.StaticText(panel, label=u'开始日期'), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        date_box.Add(start_date, 1, wx.ALIGN_CENTER_VERTICAL)
        self.end_date_ctrl = end_date = wx.DatePickerCtrl(panel, -1, style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        date_box.Add(wx.StaticText(panel, label=u'结束日期'), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 10)
        date_box.Add(end_date, 1, wx.ALIGN_CENTER_VERTICAL)
        main_box.Add(date_box, 0, wx.EXPAND | wx.ALL, 10)

        case_box = wx.BoxSizer(wx.HORIZONTAL)

        self.list_box = list_box = wx.ListBox(panel, -1)
        case_box.Add(list_box, 1, wx.EXPAND | wx.UP, 10)
        for i in range(10):
            list_box.Append('123')

        button_panel = wx.Panel(panel, -1)
        button_box = wx.BoxSizer(wx.VERTICAL)
        new = wx.Button(button_panel, -1, u'添加用例')
        ren = wx.Button(button_panel, -1, u'编辑用例')
        dlt = wx.Button(button_panel, -1, u'删除用例')
        clr = wx.Button(button_panel, -1, u'清除全部')

        button_box.Add(new, 1, wx.EXPAND | wx.UP, 10)
        button_box.Add(ren, 1, wx.EXPAND | wx.UP, 10)
        button_box.Add(dlt, 1, wx.EXPAND | wx.UP, 10)
        button_box.Add(clr, 1, wx.EXPAND | wx.UP, 10)
        button_panel.SetSizer(button_box)
        case_box.Add(button_panel, 0, wx.EXPAND | wx.LEFT, 10)

        main_box.Add(case_box, 1, wx.EXPAND | wx.ALL, 10)


        panel.SetSizerAndFit(main_box)
        main_box.Layout()
        panel.Layout()
        self.Fit()
        self.Centre()
        self.Show(True)


if __name__ == '__main__':
    if __name__ == '__main__':
        app = wx.App(False)
        test_frame = SelectorFrame(None, 'Selector')
        app.MainLoop()
