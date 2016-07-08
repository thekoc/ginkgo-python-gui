# -*- coding: utf-8 -*

import pyodbc
import platform
import datetime


class ConnectionError(Exception):
    def __init__(self, value='Failed to connect'):
        self.value = value

    def __str__(self):
        return repr(self.value)


class IDATDBdatabase(object):
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
            IDATDBdatabase.odbc_connection = odbc_connection
            self.download_data()

    def download_data(self):
        cmd = "select b.Name as CaseName, d.FileVersion as FirmwareVersion, d.Name as FirmwareName, e.Content, e.Type, e.InsertDate from tbTaskRunCS a, tbAutoTestCS b, tbTaskNeedFirmware c, tbBinaryFile d, tbTaskResult e, tbAutoTestTask f where a.AutoTestCSID = b.ID and e.AutoTestCSID = b.ID and c.FirmwareFileID = d.ID and c.AutoTestTaskID = f.ID and e.AutoTestTaskID = f.ID and a.AutoTestTaskID = f.ID"
        cursor = self.odbc_connection.cursor()
        rows = cursor.execute(cmd).fetchall()
        for row in rows:
            row[-1] = row[-1].date()
            row_data = dict(zip(['case_name', 'firmware_version', 'firmware_name', 'content', 'type', 'date'], row))
            IDATDBdatabase.data.append(row_data)
            self.case_set.add(row_data['case_name'])


class DataViewDatabase(object):
    def __init__(self):
        self.database = IDATDBdatabase()
        self.available_data = None

    def set_available_data(self, post_data):
        filter_data = filter(lambda x: post_data['date'][0] <= x['date'] <= post_data['date'][1], self.database.data)
        filter_data = filter(lambda x: x['case_name'] in post_data['case_set'], filter_data)
        available_data = {}
        for i in filter_data:
            if available_data.get(i['firmware_name']) is None:
                available_data[i['firmware_name']] = [i]
            else:
                available_data[i['firmware_name']].append(i)
        self.available_data = available_data

    def get_list_content(self):
        assert self.available_data is not None
        available_data = self.available_data
        content_rows = []
        for firm_name in available_data:
            value = available_data[firm_name]
            content_rows.append((firm_name, str(len(set([j['case_name'] for j in value]))), str(len(value))))
        return content_rows

