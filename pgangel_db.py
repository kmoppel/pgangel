#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import json

class DBConnection():

    def __init__(self, host, port, db, user, password=None):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.connection = None
        self.dataset = None

    def try_connect(self):
        try:
            conn = psycopg2.connect(host=self.host, port=self.port, user=self.user)
            conn.close()
            return True
        except Exception as e:
            print e
            return False

    def send_query_for_execution(self, callback, sql, params):
        thread_handle = 'create a newthread....' # TODO dataset will be filled when thread finishes. some callback neededed
        # cur = self.connection.cursor(cursor_)
        # cur.execute(sql, params)
        return thread_handle
        # return [{'a' : 1}]


class DbServer():

    def __init__(self, name=None, db_conn=None):
        self.name = name
        self.db_conn = db_conn
        self.tags = None    # TODO
        self.save_password = None    # TODO

    def __str__(self):
        return '''{"name": "''' + self.name  + '''", "db_conn":''' + json.dumps(self.db_conn.__dict__) + '}'


if __name__ == '__main__':
    dbc = DBConnection('localhost', 5432, 'postgres', 'kmoppel')
    dbs = DbServer('srv1', dbc)
    # print dbc.try_connect()
    print dbs