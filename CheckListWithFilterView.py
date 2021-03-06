# -*- coding: utf-8 -*

import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)


class CheckListWithFilterPanel(wx.Panel):
    """
    Panel that contains a checklist and a filter text ctrl with two customizable button.
    The two button can be achieved by .custom_button1 and .custom_button2.
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.column = 0
        self.main_box = main_box = wx.BoxSizer(wx.VERTICAL)
        list_box = wx.BoxSizer(wx.HORIZONTAL)

        # ======== list ctrl setting ========
        self.list_ctrl = list_ctrl = CheckListCtrl(self)
        list_box.Add(list_ctrl, 1, wx.EXPAND)

        # ======== buttons setting ========
        button_box = wx.BoxSizer(wx.VERTICAL)
        self.select_all_button = select_all_button = wx.Button(self, label=u'全部选择')
        button_box.Add(select_all_button, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 3)

        self.deselect_all_button = deselect_all_button = wx.Button(self, label=u'全部取消')
        button_box.Add(deselect_all_button, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 3)

        self.reverse_select_button = reverse_select_button = wx.Button(self, label=u'反选')
        button_box.Add(reverse_select_button, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 3)

        self.custom_button1 = custom_button1 = wx.Button(self)
        button_box.Add(custom_button1, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 3)

        list_box.Add(button_box, 0, wx.EXPAND | wx.LEFT, 10)
        main_box.Add(list_box, 1, wx.EXPAND | wx.ALL, 10)

        # ======== filter setting ========
        filter_box = wx.BoxSizer(wx.HORIZONTAL)
        self.filter_text_ctrl = filter_text_ctrl = wx.TextCtrl(self)
        filter_box.Add(filter_text_ctrl, 1, wx.EXPAND)
        self.search_method_button = search_method_button = wx.Button(self, label=u'切换到Regex')
        filter_box.Add(search_method_button, 0, wx.EXPAND | wx.LEFT, 10)

        main_box.Add(filter_box, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizerAndFit(main_box)


if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title='testView')
    P = CheckListWithFilterPanel(frame)
    frame.Fit()
    frame.Show()
    app.MainLoop()
