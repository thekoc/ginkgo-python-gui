import ConfigParser
import os


class AppConfig(object):
    def __init__(self):
        self.file_path = 'AppData/app.cfg'
        self.config = ConfigParser.SafeConfigParser()
        self.config.read(self.file_path)

    def __del__(self):
        self.save_to_file()

    def save_to_file(self):
        with open(self.file_path, 'wb') as configfile:
            self.config.write(configfile)

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
