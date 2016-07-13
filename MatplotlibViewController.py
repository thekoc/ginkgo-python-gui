# -*- coding: utf-8 -*
from MatplotlibView import MatplotlibPanel
import numpy as np
import wx
from wx.lib.pubsub import pub
from Radio.Radio import Channel
from Radio.MessageType import GraphMessage


class MatplotlibPanelController(object):
    def __init__(self, parent, panel=None):
        # type: (wx.Frame | wx.Panel, MatplotlibPanel) -> None
        if panel is None:
            panel = MatplotlibPanel(parent)
        self.panel = panel

        self.subscribe()

    def plot(self, xx, yy):
        self.panel.axes.clear()
        self.panel.axes.plot(xx, yy)
        self.panel.canvas.draw()

    def subscribe(self):
        pub.subscribe(self.radio_handler, Channel.fmGraph)

    def radio_handler(self, msg, data, option):
        if msg == GraphMessage.plot:
            self.plot_handler(data, option)
        else:
            raise ValueError

    def plot_handler(self, data, option):
        """
        Handles data received from radio and hand over them for further procedure

        Args:
            data: list that contained all data needs to be plotted as a dict
            option: two-element tuple.
        """
        if option[1] == u'版本号':
            classified_data = self.version_classify_data(data)
        elif option[1] == u'测试用例':
            classified_data = self.case_classify_data(data)
        else:
            raise ValueError

        if option[0] == u'饼状图':
            pass
        elif option[0] == u'柱状图':
            pass
        elif option[0] == u'折线图':
            pass
        else:
            raise ValueError

    def version_classify_data(self, data):
        return self.common_classify_data(data, 'firmware_version')

    def case_classify_data(self, data):
        return self.common_classify_data(data, 'case_name')

    def common_classify_data(self, data, feature):
        # type: (list[dict], str) -> list[list[dict]]
        assert isinstance(feature, str) and isinstance(data, list)
        feature_list = set(i[feature] for i in data)
        return [[i for i in data if i[feature] == kind] for kind in feature_list]

