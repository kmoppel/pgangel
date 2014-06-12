#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import psycopg2
import psycopg2.extras
import json

class DBConnection():

    def __init__(self, host, port, database, username=None, password=None):
        # if not (username and password):
        #     pgpass = os.path.expanduser('~/.pgpass')
        #     auths = [re.sub('#.*$|\n', '', line) for line in open( pgpass, r'r') if not re.match('#.*', line.strip())]
        #     auths = [line.replace('*', '.*') for line in auths]   #pgpass *'s are converted to .*'s
        #     for auth in auths:
        #         auth_parts = auth.split(':')    #host:port:database:user:pass
        #         if re.match(auth_parts[0], host) and re.match(auth_parts[1], port) and re.match(auth_parts[2], database):
        #             username = username or auth_parts[3]
        #             password = password or auth_parts[4]
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.dataset = None
        self.connection = psycopg2.connect(host=self.host, port=self.port, dbname=self.database, user=self.username, password=self.password)
        self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

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
        vars=dict(self.db_conn.__dict__)
        vars.pop('connection')
        vars.pop('cursor')
        vars.pop('password')
        vars.pop('dataset')
        return '''{"name": "''' + self.name  + '''", "db_conn":''' + json.dumps(vars) + '}'


if __name__ == '__main__':
    dbc = DBConnection('localhost', 5432, 'postgres', 'kmoppel', '')
    dbs = DbServer('srv1', dbc)
    # print dbc.try_connect()
    print dbs