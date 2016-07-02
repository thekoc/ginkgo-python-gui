# -*- coding: utf-8 -*
import wx
import datetime
from SelectorView import SelectorFrame


def _wxdate2pydate(date):
    # type: (wx.DateTime) -> datetime.datetime
    assert isinstance(date, wx.DateTime)
    if date.IsValid():
        ymd = map(int, date.FormatISODate().split('-'))
        return datetime.date(*ymd)
    else:
        return None

class SelectorViewController(object):
    def __init__(self, frame):
        # type: (SelectorFrame) -> None
        self.frame = frame

        self.start_date_ctrl = frame.start_date_ctrl
        self.end_date_ctrl = frame.end_date_ctrl
        self.list_box = frame.list_box
        self.new_button = frame.new_button
        self.edit_button = frame.edit_button
        self.delete_button = frame.delete_button
        self.clear_button = frame.clear_button
        self.inquire_button = frame.inquire_button

        self.action_bind()

    def action_bind(self):
        self.new_button.Bind(wx.EVT_BUTTON, self.add_case)
        self.edit_button.Bind(wx.EVT_BUTTON, self.edit_case)
        self.delete_button.Bind(wx.EVT_BUTTON, self.delete_case)
        self.clear_button.Bind(wx.EVT_BUTTON, self.clear_case)

    def add_case(self, event):
        self.list_box.Append('place holder')

    def edit_case(self, event):
        sel = self.list_box.GetSelection()
        text = self.list_box.GetString(sel)
        renamed = wx.GetTextFromUser(u'编辑', u'编辑用例', text)
        if renamed != '':
            self.list_box.Delete(sel)
            self.list_box.Insert(renamed, sel)

    def delete_case(self, event):
        sel = self.list_box.GetSelection()
        if sel != -1:
            self.list_box.Delete(sel)

    def clear_case(self, event):
        self.list_box.Clear()

    def get_start_date(self):
        return _wxdate2pydate(self.start_date_ctrl.Value)

    def get_end_date(self):
        return _wxdate2pydate(self.end_date_ctrl.Value)

if __name__ == '__main__':
    app = wx.App(False)
    test_frame = SelectorFrame(None, 'Selector')
    con = SelectorViewController(test_frame)
    app.MainLoop()
