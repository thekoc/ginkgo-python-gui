import wx


class CheckListWithFilterViewController(object):

    def __init__(self, panel):
        # type: (CheckListWithFilterView.CheckListWithFilterPanel) -> None
        self.panel = panel
        self.list_ctrl = panel.list_ctrl
        self.select_all_button = panel.select_all_button
        self.deselect_all_button = panel.deselect_all_button
        self.reverse_select_button = panel.reverse_select_button
        self.more_button = panel.more_button

        self.view_loaded()
        self.action_bind()

    def view_loaded(self):
        pass

    def action_bind(self):
        self.select_all_button.Bind(wx.EVT_BUTTON, self.select_all)
        self.deselect_all_button.Bind(wx.EVT_BUTTON, self.deselect_all)
        self.reverse_select_button.Bind(wx.EVT_BUTTON, self.reverse_select)

    def select_all(self, event):
        num = self.list_ctrl.GetItemCount()
        for i in range(num):
            self.list_ctrl.CheckItem(i)

    def deselect_all(self, event):
        num = self.list_ctrl.GetItemCount()
        for i in range(num):
            self.list_ctrl.CheckItem(i, False)

    def reverse_select(self, event):
        num = self.list_ctrl.GetItemCount()
        for i in range(num):
            self.list_ctrl.CheckItem(i, not self.list_ctrl.IsChecked(i))

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
