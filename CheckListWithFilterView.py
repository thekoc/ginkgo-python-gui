# -*- coding: utf-8 -*

import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin


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

        # ======== list ctrl setting ========
        self.list_ctrl = list_ctrl = CheckListCtrl(self)
        # list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, printhh)

        list_box.Add(list_ctrl, 1, wx.EXPAND)

        # ======== buttons setting ========
        button_box = wx.BoxSizer(wx.VERTICAL)
        self.select_all_button = select_all_button = wx.Button(self, label=u'全部选择')
        button_box.Add(select_all_button, 1, wx.EXPAND)

        self.deselect_all_button = deselect_all_button = wx.Button(self, label=u'全部取消')
        button_box.Add(deselect_all_button, 1, wx.EXPAND)

        self.reverse_select_button = reverse_select_button = wx.Button(self, label=u'反选')
        button_box.Add(reverse_select_button, 1, wx.EXPAND)

        self.more_button = more_button = wx.Button(self, label=u'查看详情')
        button_box.Add(more_button, 1, wx.EXPAND)

        list_box.Add(button_box, 0, wx.EXPAND | wx.LEFT, 10)
        main_box.Add(list_box, 1, wx.EXPAND | wx.ALL, 10)

        # ======== filter setting ========
        filter_box = wx.BoxSizer(wx.HORIZONTAL)
        self.filter_text_ctrl = filter_text_ctrl = wx.TextCtrl(self)
        filter_box.Add(filter_text_ctrl, 1, wx.EXPAND)
        self.filter_button = filter_button = wx.Button(self, label=u'搜索')
        filter_box.Add(filter_button, 0, wx.EXPAND | wx.LEFT, 10)

        main_box.Add(filter_box, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizerAndFit(main_box)


if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title='testView')
    P = CheckListWithFilterPanel(frame)
    frame.Show()
    app.MainLoop()