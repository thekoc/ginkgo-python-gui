# -*- coding: utf-8 -*
import wx
from MatplotlibView import MatplotlibPanel
from CheckListWithFilterView import CheckListWithFilterPanel


class DataFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)

        self.panel = panel = wx.Panel(self)

        main_box = wx.BoxSizer(wx.VERTICAL)
        # ======== graph panel ========
        self.graph = graph = MatplotlibPanel(panel)
        main_box.Add(graph, 1, wx.EXPAND)

        # ======== buttom box ========
        bottom_box = wx.BoxSizer(wx.HORIZONTAL)

        # ======== option panel ========
        option_panel = wx.Panel(panel)
        option_box = wx.BoxSizer(wx.VERTICAL)
        plot_type_label = wx.StaticText(option_panel, label=u'图像类型')
        option_box.Add(plot_type_label, 0, wx.ALIGN_CENTRE | wx.BOTTOM, 10)

        pan_option = wx.RadioButton(option_panel, label=u'饼状图', style=wx.RB_GROUP)
        bar_option = wx.RadioButton(option_panel, label=u'柱状图')
        line_option = wx.RadioButton(option_panel, label=u'折线图')
        option_box.AddMany([(i, 0, wx.TOP) for i in [pan_option, bar_option, line_option]])

        option_box.AddSpacer(20)

        classify_type_label = wx.StaticText(option_panel, label=u'分类方式')
        option_box.Add(classify_type_label, 0, wx.ALIGN_CENTRE | wx.BOTTOM, 10)

        firmware_option = wx.RadioButton(option_panel, label=u'版本号', style=wx.RB_GROUP)
        case_option = wx.RadioButton(option_panel, label=u'测试用例')
        option_box.AddMany([(i, 0, wx.TOP) for i in [firmware_option, case_option]])

        option_panel.SetSizerAndFit(option_box)
        option_box.Layout()
        bottom_box.Add(option_panel, 0, wx.EXPAND | wx.ALL, 20)

        # ======== firmware list ========
        self.firmware_list = firmware_list = CheckListWithFilterPanel(panel)
        bottom_box.Add(firmware_list, 1, wx.EXPAND)

        main_box.Add(bottom_box, 0, wx.EXPAND)

        panel.SetSizerAndFit(main_box)
        self.Fit()
        self.Show(True)

if __name__ == '__main__':
    app = wx.App()
    frame = DataFrame(None, 'DataView')
    app.MainLoop()

