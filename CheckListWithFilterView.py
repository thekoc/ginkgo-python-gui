# -*- coding: utf-8 -*

import wx
import sys
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
from CheckListWithFilterViewController import CheckListWithFilterViewController

fake_data = [('android', '121'), ('ios', '34'), ('windows', '334'), ('linux', '41')]


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)


class CheckListWithFilterPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.column = 0
        main_box = wx.BoxSizer(wx.VERTICAL)
        list_box = wx.BoxSizer(wx.HORIZONTAL)

        # list ctrl setting
        self.list_ctrl = list_ctrl = CheckListCtrl(self)
        # list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, printhh)

        for i in fake_data:
            index = self.list_ctrl.InsertStringItem(sys.maxint, i[0])
            self.list_ctrl.SetStringItem(index, 1, i[1])

        list_box.Add(list_ctrl, 1, wx.EXPAND)
        # buttons setting
        button_box = wx.BoxSizer(wx.VERTICAL)
        self.select_all_button = select_all_button = wx.Button(self, label=u'全部选择')
        button_box.Add(select_all_button, 1, wx.EXPAND)

        self.delete_all_button = delect_all_button = wx.Button(self, label=u'全部取消')
        button_box.Add(delect_all_button, 1, wx.EXPAND)

        self.reverse_button = reverse_button = wx.Button(self, label=u'反选')
        button_box.Add(reverse_button, 1, wx.EXPAND)

        self.more_button = more_button = wx.Button(self, label=u'查看详情')
        button_box.Add(more_button, 1, wx.EXPAND)

        list_box.Add(button_box, 0, wx.EXPAND)

        main_box.Add(list_box, 1, wx.EXPAND)

        self.SetSizerAndFit(main_box)


if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title='testView')
    P = CheckListWithFilterPanel(frame)
    C = CheckListWithFilterViewController(P)
    C.insert_column(0, 'Firmware')
    C.insert_column(1, 'Amount')
    for i in fake_data:
        C.insert_row(sys.maxint, i)
    frame.Show()
    app.MainLoop()