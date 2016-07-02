class CheckListWithFilterViewController(object):
    def __init__(self, panel):
        # type: (CheckListWithFilterPanel) -> None
        self.panel = panel
        self.list_ctrl = panel.list_ctrl

    def insert_column(self, column, title):
        # type: (int, basestring) -> None
        self.panel.column += 1
        self.list_ctrl.InsertColumn(column, title, width=-1)

    def insert_row(self, row, items):
        if len(items) != self.panel.column:
            raise ValueError('Wrong Dimensionality')
        else:
            index = 0
            for no, item in enumerate(items):
                if no == 0:
                    index = self.list_ctrl.InsertStringItem(row, item)
                else:
                    self.list_ctrl.SetStringItem(index, no, item)
                    self.list_ctrl.SetStringItem(index, no, item)