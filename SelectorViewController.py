# -*- coding: utf-8 -*
import wx
import datetime
from SelectorView import SlectorPanel
from CheckListWithFilterViewController import CheckListWithFilterPanelController
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


def _pydate2wxdate(date):
    tt = date.timetuple()
    dmy = (tt[2], tt[1] - 1, tt[0])
    return wx.DateTimeFromDMY(*dmy)


class SlectorPanelController(object):
    def __init__(self, panel=None):
        # type: (SlectorPanel) -> None
        if panel is None:
            panel = SlectorPanel(None, u'选择用例')
        self.panel = panel

        self.database = IDATDBdatabase()

        self.start_date_ctrl = panel.start_date_ctrl
        self.end_date_ctrl = panel.end_date_ctrl
        self.check_list = panel.check_list
        self.check_controller = CheckListWithFilterPanelController(self.panel.check_list)

        self.view_loaded()
        self.action_bind()

    def view_loaded(self):
        self.start_date_ctrl.Value = self.end_date_ctrl.Value - wx.DateSpan(months=1)
        # set check_ctrl
        check_controller = self.check_controller
        check_controller.set_custom_button_label2(u'更新数据')
        check_controller.set_custom_function2(self.inquire)
        check_controller.insert_column(0, u'用例')
        for i, c in enumerate(IDATDBdatabase.case_set):
            check_controller.insert_row(i, (c,))

    def action_bind(self):
        pass

    def inquire(self, event):
        data = dict()
        data['date'] = (self.get_start_date(), self.get_end_date())
        data['case_set'] = set(self.check_controller.get_checked_item_text())
        print(data)
        pub.sendMessage(Channel.fmFrame, sender=self.panel, msg=FrameMessage.inquire,
                        data=data)

    def get_start_date(self):
        return _wxdate2pydate(self.start_date_ctrl.Value)

    def get_end_date(self):
        return _wxdate2pydate(self.end_date_ctrl.Value)


if __name__ == '__main__':
    app = wx.App(False)
    con = SlectorPanelController()
    app.MainLoop()
