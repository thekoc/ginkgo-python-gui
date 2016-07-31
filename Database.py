# -*- coding: utf-8 -*

import pyodbc
import platform
import pickle
import sys
import os

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)


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
        # with open('data.pickle', 'rb') as f:
        #     rows = pickle.load(f)
        for row in rows:
            if row[-2] not in [7, 8, 11, 12, 14, 15]:
                continue
            row[-1] = row[-1].date()
            row_data = dict(zip(['case_name', 'firmware_version', 'firmware_name', 'content', 'type', 'date'], row))
            IDATDBdatabase.data.append(row_data)
            self.case_set.add(row_data['case_name'])


class DataViewDatabase(object):
    def __init__(self):
        self.database = IDATDBdatabase()
        self.available_data = None
        self.list_data = None

    def set_available_data(self, post_data):

        # type: (dict) -> dict[str, list[dict]]
        """
        Called by DataViewController for initializing.

        Args:
            post_data: A dict that has 2 keys: date and case set
                       the date is a tuple that contains two datetime.date referring start date and end date
                       the case set is a set that contains all needed cases
        """
        filter_data = filter(lambda x: post_data['date'][0] <= x['date'] <= post_data['date'][1], self.database.data)
        filter_data = filter(lambda x: x['case_name'] in post_data['case_set'], filter_data)
        self.list_data = list(filter_data)
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

    def get_available_data_from_database(self):
        # type: () -> list[dict]
        return self.list_data


class FilterListDatabase(object):
    def __init__(self):
        self.row_items = []
        self.checked_items = set()

    def insert_row(self, row, items):
        if items not in self.row_items:
            self.row_items.insert(row, items)

    def merge_checked_item(self, item_text):
        self.checked_items.add(item_text)

    def delete_checked_item(self, item_text):
        self.checked_items.discard(item_text)


class GraphDatabase(object):
    def __init__(self):
        pass

