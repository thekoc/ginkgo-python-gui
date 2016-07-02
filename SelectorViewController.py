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
        self.new_button = frame.new_button
        self.edit_button = frame.edit_button
        self.delete_button = frame.delete_button
        self.clear_button = frame.delete_button
        self.inquire_button = frame.inquire_button

        self.action_bind()

    def action_bind(self):
        self.new_button.Bind()

    def get_start_date(self):
        return _wxdate2pydate(self.start_date_ctrl.Value)

    def get_end_date(self):
        return _wxdate2pydate(self.end_date_ctrl.Value)
