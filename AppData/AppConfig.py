import ConfigParser
import os
import threading


class AppConfig(object):
    file_path = 'AppData/app.cfg'
    lock = threading.Lock()

    def __init__(self):
        if not hasattr(AppConfig, 'config'):
            config = ConfigParser.SafeConfigParser()
            if not os.path.isfile(self.file_path):
                config.add_section('Login')
                config.set('Login', 'remember', 'False')
                self.save_to_file()
            else:
                config.read(self.file_path)
            AppConfig.config = config

    def __del__(self):
        self.save_to_file()

    def save_to_file(self):
        AppConfig.lock.acquire()
        try:
            with open(self.file_path, 'wb') as configfile:
                self.config.write(configfile)
        finally:
            AppConfig.lock.release()

    @property
    def remember(self):
        return self.config.getboolean('Login', 'remember')

    @remember.setter
    def remember(self, state):
        self.config.set('Login', 'remember', str(state))
        self.save_to_file()

    @property
    def ip(self):
        return self.config.get('Login', 'ip')

    @ip.setter
    def ip(self, value):
        self.config.set('Login', 'ip', value)
        self.save_to_file()

    @property
    def password(self):
        return self.config.get('Login', 'password')

    @password.setter
    def password(self, value):
        self.config.set('Login', 'password', value)
        self.save_to_file()

    @property
    def uid(self):
        return self.config.get('Login', 'uid')

    @uid.setter
    def uid(self, value):
        self.config.set('Login', 'uid', str(value))
        self.save_to_file()

if __name__ == '__main__':
    c = AppConfig()
