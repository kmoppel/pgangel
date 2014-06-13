#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import psycopg2
import psycopg2.extras
import json
import threading
import time

class DBConnection(object):

    def __init__(self, host, port, database, username=None, password=None):
        if not (username and password):
            auths = []
            try:
                pgpass = os.path.expanduser('~/.pgpass')
                auths = [re.sub('#.*$|\n', '', line) for line in open( pgpass, r'r') if not re.match('#.*', line.strip())]
                auths = [re.sub('\.\*|\*', '.*', line) for line in auths]   #pgpass *'s are converted to .*'s
            except Exception as e:
                print e
                pass
            for auth in auths:
                auth_parts = auth.split(':')    #host:port:database:user:pass
                if re.match(auth_parts[0], host) and re.match(auth_parts[1], port) and re.match(auth_parts[2], database):
                    username = username or auth_parts[3]
                    password = password or auth_parts[4]
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(host=self.host, port=self.port, dbname=self.database, user=self.username, password=self.password)
            self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            return True
        except Exception as e:
            print e
            return False

    def __exit__(self):
        if self.connection:
            self.connection.close()


class DBCursor(object):
    def __init__(self, dbconnection):
        self.dbconnection = dbconnection
        if dbconnection.connection is None:
            dbconnection.connect()
        self.cursor = dbconnection.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.rowcount = None
        self.cstore = None
        self.columns = None
        self.running = False
        self.available = True           #e.g. after data is offloaded
        self.thread = None
        ''':type : threading.Thread'''

    def process_query(self, query):
        self.running = True
        try:
            self.cursor.execute(query)
            self.columns = [desc[0] for desc in self.cursor.description]
            self.rowcount = self.cursor.rowcount
            self.cstore = {}
            for row in self.cursor:
                for col in self.columns:
                    data = row[col]
                    if not self.cstore.get(col, None):
                        self.cstore[col] = []
                    self.cstore[col].append(data)
        except Exception as e:
            print e
        self.running = False

    def execute_query(self, query):
        if self.available:
            try:
                self.available = False
                self.thread = threading.Thread(target=self.process_query, args=(query,))
                self.thread.daemon = True
                self.thread.start()
            except Exception as e:
                self.available = True
                print e

    def cancel_query(self):
        status = False
        if self.thread:
            if self.thread.isAlive():
                try:
                    pid = self.dbconnection.get_backend_pid()
                    self.cursor.execute('select pg_terminate_backend(' + str(pid) + ') AS status')
                    for row in self.cursor:
                        status = row['status']
                    if status:
                        self.available = True
                        self.running = False
                        self.thread = None
                except Exception as e:
                    print('Thread could not be terminated:' + e.message)
        return status

    def __exit__(self):
        self.cursor.close()

class DbServer():

    def __init__(self, name, host, port, dbname, user):
        self.name = name
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.tags = None    # TODO
        self.save_password = None    # TODO

    def __str__(self):
        return json.dumps(self.__dict__)



if __name__ == '__main__':
    dbc = DBConnection('localhost', '5432', 'postgres', 'kmoppel', '')
    # dbs = DbServer('srv1', 'local', '5432', 'postgres', 'kmoppel')
    # print dbc.try_connect()
    print dbc
    cur = DBCursor(dbc)
    cur.execute_query('select pg_sleep(10)')
    time.sleep(5)
    cur.cancel_query()

