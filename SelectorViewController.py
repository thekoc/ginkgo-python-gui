# -*- coding: utf-8 -*
import wx
import datetime
from SelectorView import SelectorFrame
from wx.lib.pubsub import pub
from Radio.MessageType import FrameMessage
from Radio.Radio import Channel
from Database import IDATDBdatabase


def _wxdate2pydate(date):
    # type: (wx.DateTime) -> datetime.datetime
    assert isinstance(date, wx.DateTime)
    if date.IsValid():
        ymd = map(int, date.FormatISODate().split('-'))
        return datetime.date(*ymd)
    else:
        return None


class SelectorFrameController(object):
    def __init__(self, frame=None):
        # type: (SelectorFrame) -> None
        if frame is None:
            frame = SelectorFrame(None, u'选择用例')
        self.frame = frame

        self.database = IDATDBdatabase()

        self.start_date_ctrl = frame.start_date_ctrl
        self.end_date_ctrl = frame.end_date_ctrl
        self.list_box = frame.list_box
        self.new_button = frame.new_button
        self.edit_button = frame.edit_button
        self.delete_button = frame.delete_button
        self.clear_button = frame.clear_button
        self.inquire_button = frame.inquire_button

        self.view_loaded()
        self.action_bind()

    def view_loaded(self):
        # debug
        for i, j in enumerate(sorted(list(self.database.case_set))):
            if i < 1:
                self.list_box.Append(j)

    def action_bind(self):
        self.new_button.Bind(wx.EVT_BUTTON, self.add_case)
        self.edit_button.Bind(wx.EVT_BUTTON, self.edit_case)
        self.delete_button.Bind(wx.EVT_BUTTON, self.delete_case)
        self.clear_button.Bind(wx.EVT_BUTTON, self.clear_case)
        self.list_box.Bind(wx.EVT_LISTBOX_DCLICK, self.edit_case)
        self.inquire_button.Bind(wx.EVT_BUTTON, self.inquire)

    def add_case(self, event):
        case = ''
        if self.is_legal_case(case):
            self.list_box.Append('place holder')

    def edit_case(self, event):
        sel = self.list_box.GetSelection()
        text = self.list_box.GetString(sel)
        renamed = wx.GetTextFromUser(u'请输入新值', u'编辑用例', text)
        if renamed != '' and self.is_legal_case(renamed):
            self.list_box.Delete(sel)
            self.list_box.Insert(renamed, sel)
        else:
            wx.MessageBox(u'请重新输入', u'无效的测试用例', wx.OK | wx.ICON_ERROR)

    def delete_case(self, event):
        sel = self.list_box.GetSelection()
        if sel != -1:
            self.list_box.Delete(sel)
            self.list_box.SetSelection(sel-1)

    def clear_case(self, event):
        self.list_box.Clear()

    def inquire(self, event):
        data = dict()
        data['date'] = (self.get_start_date(), self.get_end_date())
        data['case_set'] = set(self.list_box.GetItems())
        pub.sendMessage(Channel.fmFrame, sender=self.frame, msg=FrameMessage.inquire,
                        data=data)

    def get_start_date(self):
        return _wxdate2pydate(self.start_date_ctrl.Value)

    def get_end_date(self):
        return _wxdate2pydate(self.end_date_ctrl.Value)

    def is_legal_case(self, case_name):
        return case_name in self.database.case_set

if __name__ == '__main__':
    app = wx.App(False)
    test_frame = SelectorFrame(None, 'Selector')
    con = SelectorFrameController(test_frame)
    app.MainLoop()
