# -*- coding: utf-8 -*
from MatplotlibView import MatplotlibPanel


class MatplotlibPanelController(object):
    def __init__(self, parent, panel=None):
        # type: (MatplotlibPanel) -> None
        if panel is None:
            panel = MatplotlibPanel(parent)
        self.panel = panel

