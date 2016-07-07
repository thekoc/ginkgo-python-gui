# -*- coding: utf-8 -*
from MatplotlibView import MatplotlibPanel
import wx


class MatplotlibPanelController(object):
    def __init__(self, parent, panel=None):
        # type: (wx.Frame | wx.Panel, MatplotlibPanel) -> None
        if panel is None:
            panel = MatplotlibPanel(parent)
        self.panel = panel

