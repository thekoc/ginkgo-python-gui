from wx.lib.pubsub import pub
from LoginViewController import LoginFrameController
from SelectorViewController import SelectorFrameController
from DataViewController import DataFrameController
from Radio.MessageType import FrameMessage
from Radio.Radio import Channel
import wx


class AppController(object):
    """
    :type selector_controller : SelectorFrameController
    :type data_frame_controller : DataFrameController
    """
    def __init__(self):
        self.app = wx.App()

        self.login_controller = LoginFrameController()
        self.selector_controller = None
        self.data_frame_controller = None

        self.subscribe()
        self.app.MainLoop()

    def subscribe(self):
        pub.subscribe(self.frame_manager, Channel.fmRadio)

    def frame_manager(self, sender, msg, data=None):
        if msg == FrameMessage.logged_in:
            self.selector_controller = SelectorFrameController()
            wx.CallAfter(sender.Close)

        elif msg == FrameMessage.inquire:
            self.data_frame_controller = DataFrameController()
            self.data_frame_controller.set_start_data(data)


if __name__ == '__main__':
    actrl = AppController()
