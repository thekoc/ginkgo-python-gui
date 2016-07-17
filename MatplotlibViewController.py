# -*- coding: utf-8 -*
from __future__ import division
from MatplotlibView import MatplotlibPanel
import numpy as np
import wx
from wx.lib.pubsub import pub
from Radio.Radio import Channel
from Radio.MessageType import GraphMessage
from matplotlib.dates import date2num
import datetime
import random


def _monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return date.replace(day=d, month=m, year=y)


class MatplotlibPanelController(object):
    def __init__(self, parent, panel=None):
        # type: (wx.Frame | wx.Panel, MatplotlibPanel) -> None
        if panel is None:
            panel = MatplotlibPanel(parent)
        self.panel = panel
        self.axes = self.panel.axes
        self.canvas = self.panel.canvas
        self.figure = self.panel.figure

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
            feature = 'firmware_name'
        elif option[1] == u'测试用例':
            feature = 'case_name'
        else:
            raise ValueError
        classified_data = self.common_classify_data(data, feature)

        if option[0] == u'饼状图':
            self.plot_pie_graph(classified_data, feature)
        elif option[0] == u'柱状图':
            pass
        elif option[0] == u'折线图':
            self.plot_line_graph(classified_data, feature)
        else:
            raise ValueError

    def common_classify_data(self, data, feature):
        # type: (list[dict], str) -> list[list[dict]]
        assert isinstance(feature, str) and isinstance(data, list)
        feature_list = set(i[feature] for i in data)
        return [[i for i in data if i[feature] == kind] for kind in feature_list]

    def plot_pie_graph(self, classified_data, feature):
        self.figure.patch.set_facecolor('white')
        self.axes.clear()
        self.axes.set_aspect(1)
        data_tuple = [(i[0][feature], len(i)) for i in classified_data]
        data_tuple.sort(key=lambda x: x[1])
        if data_tuple is not None and sum([i[1] for i in data_tuple]) != 0:
            large = data_tuple[:len(data_tuple) // 2]
            small = data_tuple[len(data_tuple) // 2:]
            reordered = large[::2] + small[::2] + large[1::2] + small[1::2]
            angle = 180 + float(sum([i[1] for i in small][::2])) / sum([i[1] for i in reordered]) * 360
            self.axes.pie([i[1] for i in reordered], labels=[i[0] for i in reordered],
                          shadow=True, labeldistance=1.2, startangle=angle)

        self.canvas.draw()

    def _divide_into_interval(self, feature_data):
        """
        divide a list of data with one feature into date interval using dict, indexed by a tuple.
        :rtype: dict[(datetime.date, datetime.date), dict]
        """
        def find_interval(date, sectioned_data):
            assert isinstance(date, datetime.date)
            assert isinstance(sectioned_data[0][0], datetime.date)
            for interval in sectioned_data:
                if interval[0] <= date < interval[1]:
                    return interval
            raise IndexError('date: ' + str(date) + 'is out of index', sectioned_data[0], sectioned_data[-1])

        feature_data.sort(key=lambda x: x['date'])
        int_start_date = feature_data[0]['date'].replace(day=1)
        int_end_date = _monthdelta(feature_data[-1]['date'], 1).replace(day=1)
        sectioned_date = []
        tem_date = int_start_date
        while tem_date < int_end_date:
            sectioned_date.append((tem_date, _monthdelta(tem_date, 1)))
            tem_date = _monthdelta(tem_date, 1)

        plot_data_dict = {}
        for d in feature_data:
            date_interval = find_interval(d['date'], sectioned_date)
            if plot_data_dict.get(date_interval) is None:
                plot_data_dict[date_interval] = [d]
            else:
                plot_data_dict[date_interval].append(d)
        return plot_data_dict

    def plot_line_graph(self, classified_data, feature):
        self.figure.patch.set_facecolor('white')
        self.axes.clear()
        self.axes.set_aspect('auto')
        success = [7, 11, 14]
        fail = [8, 12, 15]

        for data in classified_data:
            plot_data_dict = self._divide_into_interval(data)
            for key in plot_data_dict:
                items = plot_data_dict[key]
                plot_data_dict[key] = sum(1 for i in items if i['type'] in success) / len(items)
                assert isinstance(plot_data_dict[key], float)

            plot_items = sorted(plot_data_dict.items(), key=lambda x: x[0][0])
            xx = [date2num(i[0][0]) for i in plot_items]
            yy = [i[1] for i in plot_items]
            self.axes.plot_date(xx, yy, '-')

        self.axes.autoscale_view()
        self.axes.grid(True)
        self.figure.autofmt_xdate()

        self.canvas.draw()


