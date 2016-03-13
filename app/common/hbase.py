# -*- coding: UTF-8 -*-

from thrift.transport import TSocket
from thrift.packages.hbase import THBaseService
from thrift.packages.hbase.ttypes import *


class HbaseClient(object):
    def __init__(self, app=None):
        self.host = None
        self.port = None
        self.framed = False
        self.socket = None
        self.transport = None
        self.protocol = None
        self.client = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.host = app.config.get('HBASE_HOST')
        self.port = app.config.get('HBASE_PORT')

        self.socket = TSocket.TSocket(self.host, self.port)
        if self.framed:
            self.transport = TTransport.TFramedTransport(self.socket)
        else:
            self.transport = TTransport.TBufferedTransport(self.socket)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = THBaseService.Client(self.protocol)

    def get(self, table, t_get):
        self.transport.open()
        t_result = self.client.get(table, t_get)
        self.transport.close()
        return t_result

    def put(self, table, t_put):
        self.transport.open()
        self.client.put(table, t_put)
        self.transport.close()

    def delete(self, table, t_delete):
        self.transport.open()
        self.client.deleteSingle(table, t_delete)
        self.transport.close()

    def delete_multiple(self, table, t_deletes):
        self.transport.open()
        self.client.deleteMultiple(table, t_deletes)
        self.transport.close()

    def open_scanner(self, table, scan):
        self.transport.open()
        scanner_id = self.client.openScanner(table, scan)
        self.transport.close()
        return scanner_id

    def close_scanner(self, scanner_id):
        self.transport.open()
        self.closeScanner(scanner_id)
        self.transport.close()

    def scan_by_id(self, scanner_id, num):
        self.transport.open()
        t_results = self.client.getScannerRows(scanner_id, num)
        self.transport.close()
        return t_results

    def scan(self, table, scan, num):
        self.transport.open()
        t_results = self.client.getScannerResults(table, scan, num)
        self.transport.close()
        return t_results













