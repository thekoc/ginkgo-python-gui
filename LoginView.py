# -*- coding: utf-8 -*
import wx

class LoginFrame(wx.Frame):
    """A frame that allows you to login."""

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(300, 300))
        self.panel = wx.Panel(self)
        self.init_ui()

    def init_ui(self):
        panel = self.panel
        menu_bar = wx.MenuBar()
        self.SetMenuBar(menu_bar)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddStretchSpacer(prop=1)

        ip_box = wx.BoxSizer(wx.HORIZONTAL)
        uid_box = wx.BoxSizer(wx.HORIZONTAL)
        pwd_box = wx.BoxSizer(wx.HORIZONTAL)
        login_box = wx.BoxSizer(wx.HORIZONTAL)
        self.login_state = login_state = wx.StaticText(panel, label='')

        # ip box
        ip_text = wx.StaticText(panel, label='地址:')
        self.ip_text_field = ip_text_field = wx.TextCtrl(panel)
        ip_box.Add(ip_text, 1, wx.ALIGN_CENTER_VERTICAL)
        ip_box.Add(ip_text_field, 4, wx.ALIGN_CENTER_VERTICAL)

        # uid box
        uid_text = wx.StaticText(panel, label='用户名:')
        self.uid_text_field = uid_text_field = wx.TextCtrl(panel)
        uid_box.Add(uid_text, 1, wx.ALIGN_CENTER_VERTICAL)
        uid_box.Add(uid_text_field, 4, wx.ALIGN_CENTER_VERTICAL)

        # pwd box
        pwd_text = wx.StaticText(panel, label='密码:')
        self.pwd_text_field = pwd_text_field =  wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        pwd_box.Add(pwd_text, 1, wx.ALIGN_CENTER_VERTICAL)
        pwd_box.Add(pwd_text_field, 4, wx.ALIGN_CENTER_VERTICAL)

        # space
        vbox.AddMany([(i, 1, wx.EXPAND | wx.ALL, 6) for i in [ip_box, uid_box, pwd_box]])
        vbox.AddStretchSpacer(prop=0.1)

        # login box
        self.login_button = login_button =  wx.Button(panel, label='连接')
        self.remember = remember = wx.CheckBox(panel, -1, '记住我')
        login_box.Add(login_button, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        login_box.Add(remember, 0, wx.ALIGN_CENTER_VERTICAL)

        vbox.Add(login_box, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        # state
        login_state.SetForegroundColour((255, 20, 20))

        vbox.Add(login_state, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP)

        panel.SetSizerAndFit(vbox)
        self.Fit()

        self.Centre()
        self.Show(True)

