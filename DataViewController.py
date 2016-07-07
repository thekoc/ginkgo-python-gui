# -*- coding: utf-8 -*
from DataView import DataFrame
from MatplotlibViewController import MatplotlibPanelController
from CheckListWithFilterViewController import CheckListWithFilterPanelController
from Database import DataViewDatabase
import wx


class DataFrameController(object):
    def __init__(self, frame=None):
        # type: (DataFrame) -> None
        if frame is None:
            frame = DataFrame(None, u'')
        self.database = DataViewDatabase()
        self.frame = frame
        self.graph_controller = MatplotlibPanelController(self.frame, frame.graph)
        self.firmware_list = frame.firmware_list
        self.firmware_controller = CheckListWithFilterPanelController(self.frame, self.firmware_list)
        self.firmware_controller.insert_column(0, u'固件号')
        self.firmware_controller.insert_column(1, u'测试用例数')
        self.firmware_controller.insert_column(2, u'总数')

    def set_start_data(self, post_data):
        self.database.set_available_data(post_data)
        content_rows = self.database.get_list_content()
        for i, row in enumerate(content_rows):
            self.firmware_controller.insert_row(i, row)



if __name__ == '__main__':
    app = wx.App()
    controller = DataFrameController()
    app.MainLoop()

