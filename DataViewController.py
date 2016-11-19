# -*- coding: utf-8 -*
from DataView import DataFrame
from MatplotlibViewController import MatplotlibPanelController
from CheckListWithFilterViewController import CheckListWithFilterPanelController
from SelectorViewController import SelectorPanelController
from Database import DataViewDatabase
import wx
import sys
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.pubsub import pub
from Radio.Radio import Channel
from Radio.MessageType import GraphMessage


class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)
        self.column = 0

    def insert_row(self, row, items):
        if len(items) != self.column:
            raise ValueError('Wrong Dimensionality')
        else:
            index = 0
            for no, item in enumerate(items):
                if no == 0:
                    index = self.InsertStringItem(row, item)
                else:
                    self.SetStringItem(index, no, item)
                    self.SetStringItem(index, no, item)

    def insert_column(self, column, title):
        # type: (int, basestring) -> None
        self.column += 1
        self.InsertColumn(column, title, width=-1)


class DataFrameController(object):
    def __init__(self, frame=None):
        # type: (DataFrame) -> None
        if frame is None:
            frame = DataFrame(None, u'')
        self.database = DataViewDatabase()
        self.frame = frame
        self.graph_controller = MatplotlibPanelController(self.frame, frame.graph)
        self.firmware_list_panel = frame.firmware_list
        self.firmware_controller = CheckListWithFilterPanelController(self.frame, self.firmware_list_panel)

        self.case_controller = SelectorPanelController(frame.case_list_panel)

        self.set_firmware()

        self.action_bind()
        self.set_default_option_button()

    def action_bind(self):
        list(map(lambda x: x.Bind(wx.EVT_RADIOBUTTON, self.radio_button_changed), self.frame.option_list))
        self.firmware_controller.set_double_click_function(self.more)

    def set_firmware(self):
        self.firmware_controller.set_custom_button_label1(u'更新图像')
        self.firmware_controller.set_custom_function1(self.update_graph)

        self.firmware_controller.insert_column(0, u'固件号')
        self.firmware_controller.insert_column(1, u'测试用例数')
        self.firmware_controller.insert_column(2, u'总数')

    def set_case(self):
        pass

    def radio_button_changed(self, event):
        self.plot_data()

    def update_graph(self, event):
        self.plot_data()

    def set_default_option_button(self):
        self.frame.pan_option.Value = True
        self.frame.firmware_option.Value = True

    def set_start_data(self, post_data):
        self.database.set_available_data(post_data, 'firmware_version')
        content_rows = self.database.get_list_content()
        self.firmware_controller.delete_all_items()
        # for i, row in enumerate(content_rows):
        #     # print('adding', i)
        #     self.firmware_controller.safe_insert_row(i, row)
        self.firmware_controller.safe_insert_rows(content_rows)
        self.plot_data()

    def more(self, event):
        if self.firmware_controller.get_selected_index() != -1:
            firmware_name = self.firmware_controller.get_selected_item_text()
            firmware_data = self.database.available_data[firmware_name]
            new_frame = wx.Frame(self.frame, title='more')
            list_ctrl = AutoWidthListCtrl(new_frame)
            list_ctrl.insert_column(0, u'固件')
            list_ctrl.insert_column(1, u'固件版本')
            list_ctrl.insert_column(2, u'时间')
            list_ctrl.insert_column(3, u'测试用例')
            list_ctrl.insert_column(4, u'结果')
            list_ctrl.insert_column(5, u'内容')

            for i, d in enumerate(firmware_data):
                list_ctrl.insert_row(i, (d['firmware_name'], d['firmware_version'],
                                         str(d['date']), d['case_name'], str(d['type']), d['content']))

            new_frame.Fit()
            new_frame.Show()

    def get_option(self):
        return [i.GetLabel() for i in self.frame.option_list if i.Value]

    def plot_data(self):
        print('plotting')
        data = self.database.get_available_data_from_database()
        print('1')
        checked = self.firmware_controller.get_checked_item_text()
        print(checked)
        print('2')
        data = [i for i in data if i['firmware_version'] in checked]
        print('3')
        option = self.get_option()
        print('4')
        pub.sendMessage(Channel.fmGraph, msg=GraphMessage.plot, data=data, option=option)
        print('done')


if __name__ == '__main__':
    app = wx.App()
    controller = DataFrameController()
    app.MainLoop()
