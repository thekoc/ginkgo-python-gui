# -*- coding: utf-8 -*
from __future__ import division
from MatplotlibView import MatplotlibPanel
import numpy as np
from wx.lib.pubsub import pub
from Radio.Radio import Channel
from Radio.MessageType import GraphMessage
from matplotlib.dates import date2num
import datetime
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cmx
import matplotlib.colors as colors



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
            self.plot_bar_graph(classified_data, feature)
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
        self.figure.delaxes(self.axes)
        self.axes = self.figure.add_subplot(111)
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
        if classified_data:
            success = [7, 11, 14]
            fail = [8, 12, 15]
            self.figure.delaxes(self.axes)
            self.axes = self.figure.add_subplot(111)
            self.axes.clear()

            for data in classified_data:
                plot_data_dict = self._divide_into_interval(data)
                success_dict = {}
                for key in plot_data_dict:
                    items = plot_data_dict[key]
                    success_dict[key] = sum(1 for i in items if i['type'] in success) / len(items)
                    assert isinstance(success_dict[key], float)

                plot_items = sorted(success_dict.items(), key=lambda x: x[0][0])
                xx = [date2num(i[0][0]) for i in plot_items]
                yy = [i[1] for i in plot_items]
                self.axes.plot_date(xx, yy, fmt='-', label=data[0][feature])

            self.axes.set_ylabel('success rate')
            self.axes.legend(fontsize=10).get_frame().set_alpha(0.5)
            self.figure.patch.set_facecolor('white')
            self.axes.set_aspect('auto')
            self.axes.autoscale_view()
            self.axes.grid(True)
            self.figure.autofmt_xdate()

            self.canvas.draw()

    def plot_bar_graph(self, classified_data, feature):
        if classified_data:
            self.figure.delaxes(self.axes)
            self.axes = self.figure.add_subplot(111, projection='3d')
            success = [7, 11, 14]
            fail = [8, 12, 15]
            y_index = 0
            z_limits = [-1, 1]
            x_limits_dict = {'possible_min': [], 'possible_max':[]}
            num = len(classified_data) * 2
            cm = self.get_cmap(num)

            y_ticks = []
            y_labels = []
            for j, data in enumerate(classified_data):
                success_dict = {}
                fail_dict = {}
                plot_data_dict = self._divide_into_interval(data)
                for key in plot_data_dict:
                    success_dict[key] = sum(1 for i in plot_data_dict[key] if i['type'] in success)
                    fail_dict[key] = sum(-1 for i in plot_data_dict[key] if i['type'] in fail)

                success_items = sorted(success_dict.items(), key=lambda x: x[0][0])
                fail_items = sorted(fail_dict.items(), key=lambda x: x[0][0])
                # print success_items
                # print fail_items

                xx = [date2num(i[0][0]) for i in success_items]
                dx = [date2num(i[0][1]) - date2num(i[0][0]) for i in fail_items]
                zz = [i[1] for i in success_items]
                if max(zz) > z_limits[1]:
                    z_limits[1] = max(zz)
                self.plot_bar2d(xx, dx, zz, y_index, data[0][feature], color=cm(2 * j))

                xx = [date2num(i[0][0]) for i in fail_items]
                dx = [date2num(i[0][1]) - date2num(i[0][0]) for i in fail_items]
                zz = [i[1] for i in fail_items]
                if min(zz) < z_limits[0]:
                    z_limits[0] = min(zz)
                self.plot_bar2d(xx, dx, zz, y_index, data[0][feature], color=cm(2 * j + 1))

                y_ticks.append(y_index)
                y_labels.append(data[0][feature])

                x_limits_dict['possible_min'].append(min(success_items[0][0][0], fail_items[0][0][0]))
                x_limits_dict['possible_max'].append(max(success_items[-1][0][1], fail_items[-1][0][1]))
                y_index += 1

            ax = self.axes
            import matplotlib.dates as mdates
            # months = mdates.MonthLocator()  # every month
            months = mdates.MonthLocator(range(1, 13), bymonthday=1, interval=3)
            years_fmt = mdates.DateFormatter('%b %Y')
            ax.set_zlim3d(z_limits)
            ax.xaxis.set_major_locator(months)
            ax.xaxis.set_major_formatter(years_fmt)
            ax.autoscale_view()
            self.figure.autofmt_xdate()
            ax.yaxis.set_ticks(y_ticks)
            ax.yaxis.set_ticklabels(y_labels)

            date_min = datetime.date(min(x_limits_dict['possible_min']).year, 1, 1)
            date_max = datetime.date(max(x_limits_dict['possible_max']).year + 1, 1, 1)
            ax.set_xlim(date_min, date_max)


            self.canvas.draw()

    def plot_bar2d(self, xx, dx, zz, y_index, feature_name, color):
        color = [color] * len(xx)
        if len(xx) >= 1:
            y = [y_index] * len(dx)
            dy = [0.95] * len(dx)
            dz = zz
            z = [0] * len(dx)
            self.axes.bar3d(xx, y, z, dx, dy, dz, color=color)

    def get_cmap(self, n):
        """
        Returns a function that maps each index in 0, 1, ... N-1 to a distinct
        RGB color.
        """
        color_norm = colors.Normalize(vmin=0, vmax=max(n-1, 1))
        scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv')

        def map_index_to_rgb_color(index):
            return scalar_map.to_rgba(index)

        return map_index_to_rgb_color
