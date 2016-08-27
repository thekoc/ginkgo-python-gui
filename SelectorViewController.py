# -*- coding: utf-8 -*
import wx
import datetime
from SelectorView import SelectorFrame
from CheckListWithFilterViewController import CheckListWithFilterPanelController
from wx.lib.pubsub import pub
from Radio.MessageType import FrameMessage
from Radio.Radio import Channel
from Database import IDATDBdatabase


class CheckListDialog(wx.Dialog):
    def __init__(
            self, parent, id_, title, size=wx.DefaultSize,
            pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='dialog'):
        wx.Dialog.__init__(self, parent, id_, title, pos, size, style, name)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.check_controller = check_controller = CheckListWithFilterPanelController(self)
        panel = check_controller.panel

        sizer.Add(panel, 0, wx.ALIGN_CENTRE | wx.ALL, 5)


        # set check_ctrl
        check_controller.set_custom_button_label2(u'完成选择')
        check_controller.set_custom_function2(self.finish)
        check_controller.insert_column(0, u'用例')
        for i, c in enumerate(IDATDBdatabase.case_set):
            check_controller.insert_row(i, (c,))
        sizer.Fit(self)

    def finish(self, event):
        self.EndModal(wx.ID_OK)

    def get_checked_item_text(self):
        return self.check_controller.get_checked_item_text()


def _wxdate2pydate(date):
    # type: (wx.DateTime) -> datetime.datetime
    assert isinstance(date, wx.DateTime)
    if date.IsValid():
        ymd = map(int, date.FormatISODate().split('-'))
        return datetime.date(*ymd)
    else:
        return None


def _pydate2wxdate(date):
    tt = date.timetuple()
    dmy = (tt[2], tt[1]-1, tt[0])
    return wx.DateTimeFromDMY(*dmy)


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
        self.start_date_ctrl.Value = self.end_date_ctrl.Value - wx.DateSpan(months=1)

    def action_bind(self):
        self.new_button.Bind(wx.EVT_BUTTON, self.add_case)
        self.edit_button.Bind(wx.EVT_BUTTON, self.edit_case)
        self.delete_button.Bind(wx.EVT_BUTTON, self.delete_case)
        self.clear_button.Bind(wx.EVT_BUTTON, self.clear_case)
        self.list_box.Bind(wx.EVT_LISTBOX_DCLICK, self.edit_case)
        self.inquire_button.Bind(wx.EVT_BUTTON, self.inquire)

    def add_case(self, event):
        dlg = CheckListDialog(self.frame, -1, u"请选择", size=(350, 200),
                              style=wx.DEFAULT_DIALOG_STYLE)
        dlg.CenterOnScreen()
        dlg.ShowModal()
        cases = dlg.get_checked_item_text()
        dlg.Destroy()
        for case in cases:
            if self.is_legal_case(case) and not self.has_in_box(case):
                self.list_box.Append(case)

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

    def has_in_box(self, case_name):
        return case_name in self.list_box.GetItems()


if __name__ == '__main__':
    app = wx.App(False)
    con = SelectorFrameController()
    app.MainLoop()
