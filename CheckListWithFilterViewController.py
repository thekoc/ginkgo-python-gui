# -*- coding: utf-8 -*
import wx
import sys
from CheckListWithFilterView import CheckListWithFilterPanel

fake_data = [('android', '121'), ('ios', '34'), ('windows', '334'), ('linux', '41')]


class CheckListWithFilterPanelController(object):

    def __init__(self, parent, panel=None):
        # type: (wx.Frame | wx.Panel, CheckListWithFilterView.CheckListWithFilterPanel) -> None
        if panel is None:
            panel = CheckListWithFilterPanel(parent)
        self.panel = panel
        self.list_ctrl = panel.list_ctrl
        self.select_all_button = panel.select_all_button
        self.deselect_all_button = panel.deselect_all_button
        self.reverse_select_button = panel.reverse_select_button
        self.custom_button = panel.custom_button
        self.filter_button = panel.filter_button
        self.filter_text_ctrl = panel.filter_text_ctrl
        self.select_index = 0

        self.view_loaded()
        self.action_bind()

    def view_loaded(self):
        pass

    def action_bind(self):
        self.select_all_button.Bind(wx.EVT_BUTTON, self.select_all)
        self.deselect_all_button.Bind(wx.EVT_BUTTON, self.deselect_all)
        self.reverse_select_button.Bind(wx.EVT_BUTTON, self.reverse_select)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.double_click)
        self.list_ctrl.Bind(wx.EVT_LIST_COL_CLICK, self.column_click)

    def get_selected_index(self):
        return self.panel.list_ctrl.GetFirstSelected()

    def get_selected_item_text(self):
        return self.panel.list_ctrl.GetItemText(self.get_selected_index())

    def select_all(self, event):
        num = self.list_ctrl.GetItemCount()
        for i in range(num):
            self.list_ctrl.CheckItem(i)

    def deselect_all(self, event):
        num = self.list_ctrl.GetItemCount()
        for i in range(num):
            self.list_ctrl.CheckItem(i, False)

    def reverse_select(self, event):
        num = self.list_ctrl.GetItemCount()
        for i in range(num):
            self.list_ctrl.CheckItem(i, not self.list_ctrl.IsChecked(i))

    def filter(self, event):
        text = self.filter_text_ctrl.Value
        num = self.list_ctrl.GetItemCount()
        for i in range(num):
            if text in self.list_ctrl.GetItemText(i):
                pass

    def double_click(self, event):
        pass

    def column_click(self, event):
        pass

    def insert_column(self, column, title):
        # type: (int, basestring) -> None
        self.panel.column += 1
        self.list_ctrl.InsertColumn(column, title, width=-1)

    def insert_row(self, row, items):
        if len(items) != self.panel.column:
            raise ValueError('Wrong Dimensionality')
        else:
            index = 0
            for no, item in enumerate(items):
                if no == 0:
                    index = self.list_ctrl.InsertStringItem(row, item)
                else:
                    self.list_ctrl.SetStringItem(index, no, item)
                    self.list_ctrl.SetStringItem(index, no, item)

    def get_checked_item_text(self):
        num = self.list_ctrl.GetItemCount()
        items = []
        for i in range(num):
            if self.list_ctrl.IsChecked(i):
                items.append(self.list_ctrl.GetItemText(i))
        return items

    def set_custom_button_label(self, label):
        self.custom_button.LabelText = label

    def set_custom_function(self, func):
        self.custom_button.Bind(wx.EVT_BUTTON, func)

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title='testView')
    C = CheckListWithFilterPanelController(frame)
    C.insert_column(0, 'Firmware')
    C.insert_column(1, 'Amount')
    for i in fake_data:
        C.insert_row(sys.maxint, i)
    frame.Show()
    app.MainLoop()
