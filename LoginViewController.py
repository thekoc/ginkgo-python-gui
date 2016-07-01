# -*- coding: utf-8 -*

from IDATdb import Database
from LoginView import LoginFrame
from AppData import AppConfig
import IDATdb
import wx


class LoginViewController(object):
    database = Database()
    config = AppConfig()

    def __init__(self, frame):
        self.frame = frame
        self.login_button = frame.login_button
        self.remember = frame.remember
        self.login_state = frame.login_state

        self.ip_text_field = frame.ip_text_field
        self.uid_text_field = frame.uid_text_field
        self.pwd_text_field = frame.pwd_text_field

        self.view_loaded()
        self.action_bind()

    def action_bind(self):
        frame = self.frame

        frame.Bind(wx.EVT_BUTTON, self.login, self.login_button)
        frame.Bind(wx.EVT_CHECKBOX, self.remember_changed, self.remember)

    def view_loaded(self):
        if self.config.remember:
            self.remember.Value = True
            self.ip_text_field.Value = self.config.ip
            self.uid_text_field.Value = self.config.uid
            self.pwd_text_field.Value = self.config.uid

    def login(self, event):
        uid = self.uid_text_field.Value
        pwd = self.pwd_text_field.Value
        server = self.ip_text_field.Value
        if self.config.remember:
            self.config.uid = uid
            self.config.password = pwd
            self.config.ip = server
        try:
            self.database.connect(uid, pwd, server)
        except IDATdb.ConnectionError:
            self.login_state.SetLabelText('登录失败, 请检查信息')
            self.frame.Layout()

    def remember_changed(self, event):
        self.config.remember = event.Checked()


if __name__ == '__main__':
    app = wx.App(False)
    frame = LoginFrame(None, 'Login')
    controller = LoginViewController(frame)
    app.MainLoop()