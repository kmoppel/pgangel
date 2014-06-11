#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2

class DbServer():
    def __init__(self):
        self.name = None
        self.host = None
        self.port = None
        self.db = None
        self.user = None
        self.password = None


class DBConnection():

    def __init__(self, host, port, dbname, user, password=None):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.connection = None

    def try_connect(self):
        try:
            conn = psycopg2.connect(host=self.host, port=self.port, user=self.user)
            conn.close()
            return True
        except Exception as e:
            print e
            return False

    def execute_query():
        return [{'a' : 1}]


if __name__ == '__main__':
    dbc = DBConnection('localhost', 5432, 'postgres', 'kmoppel')
    print dbc.try_connect()