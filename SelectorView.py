# -*- coding: utf-8 -*

import wx


class SelectorFrame(wx.Frame):
    """选择时间, case 等的界面."""

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(300, 300))
        self.panel = panel = wx.Panel(self)
        main_box = wx.BoxSizer(wx.VERTICAL)

        # 时间选择
        date_box = wx.BoxSizer(wx.HORIZONTAL)
        self.start_date_ctrl = start_date = wx.DatePickerCtrl(
            panel, -1, style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        date_box.Add(wx.StaticText(panel, label=u'开始日期'), 0,
                     wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        date_box.Add(start_date, 1, wx.ALIGN_CENTER_VERTICAL)
        self.end_date_ctrl = end_date = wx.DatePickerCtrl(
            panel, -1, style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        date_box.Add(wx.StaticText(panel, label=u'结束日期'), 0,
                     wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 10)
        date_box.Add(end_date, 1, wx.ALIGN_CENTER_VERTICAL)
        main_box.Add(date_box, 0, wx.EXPAND | wx.ALL, 10)

        # 用例选择
        case_box = wx.BoxSizer(wx.HORIZONTAL)

        self.list_box = list_box = wx.ListBox(panel, -1)
        case_box.Add(list_box, 1, wx.EXPAND | wx.UP, 10)
        for i in range(10):
            list_box.Append('123')

        button_panel = wx.Panel(panel, -1)
        button_box = wx.BoxSizer(wx.VERTICAL)
        self.new_button = new_button = wx.Button(button_panel, label=u'添加用例')
        self.edit_button = edit_button = wx.Button(button_panel, label=u'编辑用例')
        self.delete_button = delete_button = wx.Button(button_panel, label=u'删除用例')
        self.clear_button = clear_button = wx.Button(button_panel, label=u'清除全部')

        button_box.Add(new_button, 1, wx.EXPAND | wx.UP, 10)
        button_box.Add(edit_button, 1, wx.EXPAND | wx.UP, 10)
        button_box.Add(delete_button, 1, wx.EXPAND | wx.UP, 10)
        button_box.Add(clear_button, 1, wx.EXPAND | wx.UP, 10)
        button_panel.SetSizer(button_box)
        case_box.Add(button_panel, 0, wx.EXPAND | wx.LEFT, 10)

        main_box.Add(case_box, 1, wx.EXPAND | wx.ALL, 10)

        # 查询按钮
        self.inquire_button = inquire_button = wx.Button(panel, label=u'查询用例测试固件')
        main_box.Add(inquire_button, 0, wx.EXPAND | wx.ALL, 10)

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
