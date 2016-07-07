# -*- coding: utf-8 -*

import pyodbc
import platform
import datetime


class ConnectionError(Exception):
    def __init__(self, value='Failed to connect'):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Database(object):
    connected = False
    odbc_connection = None
    data = []
    case_set = set()

    def __init__(self):
        self.database_name = 'IDATDB'
        self.port = 1433
        if platform.system() == 'Darwin':
            self.driver = 'FreeTDS'
        elif platform.system() == 'Windows':
            self.driver = '{Sql Server}'



    def connect(self, uid, pwd, server):
        try:
            odbc_connection = pyodbc.connect('DRIVER=%s;SERVER=%s;PORT=%d;DATABASE=%s;UID=%s;PWD=%s' %\
                                         (self.driver, server, self.port, self.database_name, uid, pwd))
        except pyodbc.Error:
            raise ConnectionError
        else:
            self.connected = True
            Database.odbc_connection = odbc_connection
            self.download_data()

    def download_data(self):
        cmd = "select b.Name as CaseName, d.FileVersion as FirmwareVersion, d.Name as FirmwareName, e.Content, e.Type, e.InsertDate from tbTaskRunCS a, tbAutoTestCS b, tbTaskNeedFirmware c, tbBinaryFile d, tbTaskResult e, tbAutoTestTask f where a.AutoTestCSID = b.ID and e.AutoTestCSID = b.ID and c.FirmwareFileID = d.ID and c.AutoTestTaskID = f.ID and e.AutoTestTaskID = f.ID and a.AutoTestTaskID = f.ID"
        cursor = self.odbc_connection.cursor()
        rows = cursor.execute(cmd).fetchall()
        for row in rows:
            row_data = dict(zip(['case_name', 'firmware_version', 'firmware_name', 'content', 'type', 'date'], row))
            Database.data.append(row_data)
            self.case_set.add(row_data['case_name'])


