# -*- coding: utf-8 -*

from IDATdb import Database
from LoginView import LoginFrame
import IDATdb
import wx

class LoginViewController(object):
    database = Database()

    def __init__(self, frame):
        self.frame = frame
        self.bind_widget()
        self.view_loaded()
        self.action_bind()

    def bind_widget(self):
        frame = self.frame
        self.login_button = frame.login_button
        self.login_state = frame.login_state

        self.ip_text_field = frame.ip_text_field
        self.uid_text_field = frame.uid_text_field
        self.pwd_text_field = frame.pwd_text_field

    def action_bind(self):
        self.frame.Bind(wx.EVT_BUTTON, self.login, self.login_button)

    def view_loaded(self):



    def login(self, e):
        uid = self.uid_text_field.Value
        pwd = self.pwd_text_field.Value
        server = self.ip_text_field.Value
        try:
            self.database.connect(uid, pwd, server)
        except IDATdb.ConnectionError:
            self.login_state.SetLabelText('登录失败, 请检查信息')
            self.frame.Layout()


if __name__ == '__main__':
    app = wx.App(False)
    frame = LoginFrame(None, 'Login')
    controller = LoginViewController(frame)
    app.MainLoop()