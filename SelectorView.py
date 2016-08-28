# -*- coding: utf-8 -*

import wx
from CheckListWithFilterView import CheckListWithFilterPanel
from Database import IDATDBdatabase


class SlectorPanel(wx.Panel):
    """选择时间, case 等的界面."""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        print('builting')
        main_box = wx.BoxSizer(wx.VERTICAL)
        panel = self

        # ======== time selector ========
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

        # ======== case selector ========
        self.check_list = check_list = CheckListWithFilterPanel(panel)

        main_box.Add(check_list, 1, wx.EXPAND | wx.ALL, 10)
        # 
        # # ======== inquire button ========
        # self.inquire_button = inquire_button = wx.Button(
        #     panel, label=u'查询用例测试固件')
        # main_box.Add(inquire_button, 0, wx.EXPAND | wx.ALL, 10)

        panel.SetSizerAndFit(main_box)
        # self.Centre()
        # self.Show(True)


if __name__ == '__main__':
    app = wx.App(False)
    test_frame = SlectorPanel(None, 'Selector')
    app.MainLoop()
