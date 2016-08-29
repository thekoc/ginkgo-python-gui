# -*- coding: utf-8 -*
import wx
import sys
from CheckListWithFilterView import CheckListWithFilterPanel
from Database import FilterListDatabase
import re


class CheckListWithFilterPanelController(object):
    """
    Controller of the panel.
    Bind your own function on two customizable button by .set_custom_function1 and 2.
    Set label of two button by .set_custom_button_label1 and 2

    Use .insert_column(column, title) to insert a column
    Use .insert_row(row, items) to insert a row

    Use .get_selected_text() to get selected text (not checked text)
    Use .get_checked_text() to get the latter

    Use .get_display_items() to get items list on the display and use .set_display_items() to set
    """

    def __init__(self, parent, panel=None):
        # type: (wx.Frame | wx.Panel, CheckListWithFilterView.CheckListWithFilterPanel) -> None
        if panel is None:
            panel = CheckListWithFilterPanel(parent)
        self.panel = panel
        self.is_warning_shown = False
        self.list_ctrl = panel.list_ctrl
        self.select_all_button = panel.select_all_button
        self.deselect_all_button = panel.deselect_all_button
        self.reverse_select_button = panel.reverse_select_button
        self.custom_button1 = panel.custom_button1
        self.search_method_button = panel.search_method_button
        self.filter_text_ctrl = panel.filter_text_ctrl
        self.select_index = 0

        self.search_method_types = ['contain', 'regex']
        self.search_method = 'contain'

        self.database = FilterListDatabase()

        self.view_loaded()
        self.action_bind()

    def view_loaded(self):
        pass

    def action_bind(self):
        self.select_all_button.Bind(wx.EVT_BUTTON, self.select_all)
        self.deselect_all_button.Bind(wx.EVT_BUTTON, self.deselect_all)
        self.reverse_select_button.Bind(wx.EVT_BUTTON, self.reverse_select)
        self.search_method_button.Bind(wx.EVT_BUTTON, self.switch_search_method)

        self.filter_text_ctrl.Bind(wx.EVT_TEXT, self.filter)

        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.double_click)
        self.list_ctrl.Bind(wx.EVT_LIST_COL_CLICK, self.column_click)

        self.list_ctrl.OnCheckItem = self.on_check_item

    def get_selected_index(self):
        return self.list_ctrl.GetFirstSelected()

    def get_selected_item_text(self):
        return self.list_ctrl.GetItemText(self.get_selected_index())

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

    def switch_search_method(self, event):
        if self.search_method_button.LabelText == u'切换到Regex':
            self.search_method_button.LabelText = u'切换到包含'
            self.search_method = self.search_method_types[1]
        elif self.search_method_button.LabelText == u'切换到包含':
            self.search_method_button.LabelText = u'切换到Regex'
            self.search_method = self.search_method_types[0]
        else:
            raise KeyError(self.search_method_button.LabelText)

    def filter(self, event):
        text = self.filter_text_ctrl.Value.lower()
        self.list_ctrl.DeleteAllItems()
        assert self.search_method in self.search_method_types
        if self.search_method == self.search_method_types[0]:
            row_items = [[line.lower() for line in row] for row in self.database.row_items]
            self.set_display_items(ori_items for ori_items, items in zip(self.database.row_items, row_items)
                                   if text in items[0])
        elif self.search_method == self.search_method_types[1]:
            pat = re.compile(text)
            row_items = [[line.lower() for line in row] for row in self.database.row_items]
            self.set_display_items(ori_items for ori_items, items in zip(self.database.row_items, row_items)
                                   if pat.match(items[0]))


    def apply(self, event):
        pass

    def double_click(self, event):
        pass

    def column_click(self, event):
        """sort the row depends on column clicked"""
        c = event.GetColumn()
        self.set_display_items(sorted(self.get_display_items(), key=lambda x: float(x[c]) if x[c].isdigit() else x[c]))

    def insert_column(self, column, title):
        # type: (int, basestring) -> None
        self.panel.column += 1
        self.list_ctrl.InsertColumn(column, title, width=-1)

    def safe_insert_row(self, row, items, display=True):
        if len(items) != self.panel.column:
            raise ValueError('Wrong Dimensionality')
        else:
            self.database.insert_row(row, items)
            if display:
                if self.list_ctrl.GetItemCount() < 300000:
                    index = 0
                    for no, item in enumerate(items):
                        if no == 0:
                            index = self.list_ctrl.InsertStringItem(row, item)
                        else:
                            self.list_ctrl.SetStringItem(index, no, item)
                    return True
                else:
                    return False

    def safe_insert_rows(self, rows):
        print ('inserting')
        warned = False
        for i, r in enumerate(rows):
            if not self.safe_insert_row(i, r):
                if not warned:
                    wx.MessageBox(u'数据过多, 将不会全部显示, 请用下方过滤文本框进行过滤', 'Info',
                                  wx.OK | wx.ICON_INFORMATION)
                warned = True
        print ('done')

    def get_checked_item_text(self):
        """
        Get checked items as a list
        """
        num = self.list_ctrl.GetItemCount()
        items = []
        for i in range(num):
            if self.list_ctrl.IsChecked(i):
                items.append(self.list_ctrl.GetItemText(i))
        return items

    def get_display_items(self):
        num = self.list_ctrl.GetItemCount()
        return [[self.list_ctrl.GetItemText(i, j) for j in range(self.panel.column)] for i in range(num)]

    def delete_all_items(self):
        self.list_ctrl.DeleteAllItems()
        self.database.delete_all()

    def set_display_items(self, row_items=None):
        self.list_ctrl.DeleteAllItems()
        if row_items is None:
            row_items = self.database.row_items
        for items in row_items:
            if self.safe_insert_row(sys.maxint, items):
                if tuple(items) in self.database.checked_items:
                    self.list_ctrl.CheckItem(self.list_ctrl.GetItemCount() - 1)

    def set_custom_button_label1(self, label):
        self.custom_button1.LabelText = label

    def set_custom_function1(self, func):
        self.custom_button1.Bind(wx.EVT_BUTTON, func)

    def set_double_click_function(self, func):
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, func)

    def on_check_item(self, index, flag):
        row_items = tuple(self.list_ctrl.GetItemText(index, i) for i in range(0, self.panel.column))
        if flag:
            self.database.merge_checked_item(row_items)
        else:
            self.database.delete_checked_item(row_items)


if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title='testView')
    C = CheckListWithFilterPanelController(frame)
    C.insert_column(0, 'Firmware')
    C.insert_column(1, 'Amount')
    for z in fake_data:
        C.safe_insert_row(sys.maxint, z)
    frame.Show()
    app.MainLoop()
