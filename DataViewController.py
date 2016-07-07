# -*- coding: utf-8 -*
from DataView import DataFrame
from MatplotlibViewController import MatplotlibPanelController
from CheckListWithFilterViewController import CheckListWithFilterPanelController
import wx


class DataFrameController(object):
    def __init__(self, frame=None):
        # type: (DataFrame) -> None
        if frame is None:
            frame = DataFrame(None, '')
        self.frame = frame
        self.graph_controller = MatplotlibPanelController(frame.graph)
        self.firmware_list = frame.firmware_list
        self.firmware_controller = CheckListWithFilterPanelController(self.firmware_list)
        self.firmware_controller.insert_column(0, u'固件号')
        self.firmware_controller.insert_column(1, u'测试用例数')
        self.firmware_controller.insert_column(2, u'总数')


if __name__ == '__main__':
    app = wx.App()
    frame = DataFrame(None, 'test')
    controller = DataFrameController(frame)
    app.MainLoop()

