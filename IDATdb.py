# -*- coding: utf-8 -*

import pyodbc


class ConnectionError(Exception):
    def __init__(self, value='Failed to connect'):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Database(object):
    def __init__(self):
        self.database_name = 'IDATDB'
        self.port = 1433
        self.driver = 'FreeTDS'
        self.connected = False
        self.odbc_connection = None

    def connect(self, uid, pwd, server):
        try:
            self.odbc_connection = pyodbc.connect('DRIVER=%s;SERVER=%s;PORT=%d;DATABASE=%s;UID=%s;PWD=%s' %\
                                         (self.driver, server, self.port, self.database_name, uid, pwd))
        except pyodbc.Error:
            raise ConnectionError
        else:
            self.connected = True

