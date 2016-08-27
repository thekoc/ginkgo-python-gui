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

        # ======== button box ========
        bottom_box = wx.BoxSizer(wx.HORIZONTAL)

        # ======== option panel ========
        option_panel = wx.Panel(panel)
        option_box = wx.BoxSizer(wx.VERTICAL)
        plot_type_label = wx.StaticText(option_panel, label=u'图像类型')
        option_box.Add(plot_type_label, 0, wx.ALIGN_CENTRE | wx.BOTTOM, 10)

        self.pan_option = pan_option = wx.RadioButton(option_panel, label=u'饼状图', style=wx.RB_GROUP)
        self.bar_option = bar_option = wx.RadioButton(option_panel, label=u'成功/失败个数')
        self.line_option = line_option = wx.RadioButton(option_panel, label=u'成功率趋势图')
        option_box.AddMany((i, 0, wx.TOP) for i in [pan_option, bar_option, line_option])

        option_box.AddSpacer(20)

        classify_type_label = wx.StaticText(option_panel, label=u'分类方式')
        option_box.Add(classify_type_label, 0, wx.ALIGN_CENTRE | wx.BOTTOM, 10)

        self.firmware_option = firmware_option = wx.RadioButton(option_panel, label=u'版本号', style=wx.RB_GROUP)
        self.case_option = case_option = wx.RadioButton(option_panel, label=u'测试用例')
        option_box.AddMany((i, 0, wx.TOP) for i in [firmware_option, case_option])

        self.option_list = [pan_option, bar_option, line_option, firmware_option, case_option]

        option_panel.SetSizerAndFit(option_box)
        option_box.Layout()
        bottom_box.Add(option_panel, 0, wx.EXPAND | wx.ALL, 20)

        # ======== firmware and case choose notebook ========
        nb = wx.Notebook(panel)
        self.firmware_list = firmware_list = CheckListWithFilterPanel(nb)
        nb.AddPage(firmware_list, u"固件选择")
        bottom_box.Add(nb, 1, wx.EXPAND)

        main_box.Add(bottom_box, 0, wx.EXPAND)

        panel.SetSizerAndFit(main_box)
        self.Fit()
        self.Show(True)

if __name__ == '__main__':
    app = wx.App()
    frame = DataFrame(None, 'DataView')
    app.MainLoop()
