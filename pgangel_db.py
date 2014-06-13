#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import psycopg2
import psycopg2.extras
import json
import threading
import time
import collections

class HostMetadata():

    def __init__(self):
        self.databases = []
        self.schemas = []
        self.tables_by_schemas = collections.defaultdict(list)
        self.views_by_schemas = collections.defaultdict(list)

    def populate_metadata(self, conn):
        q_dbs = '''select datname from pg_database where not datistemplate order by 1'''
        q_tables = '''select table_catalog, table_schema, table_name from information_schema.tables where table_schema not in ('pg_catalog', 'information_schema')'''
        q_views = '''select table_catalog, table_schema, table_name from information_schema.views where table_schema not in ('pg_catalog', 'information_schema')'''
        cur = DBCursor(conn)
        self.databases = [ x[0] for x in cur.execute_query_blocking(q_dbs) ]
        all_tables = cur.execute_query_blocking(q_tables)
        for t in all_tables:
            if t['table_schema'] not in self.schemas:
                self.schemas.append(t['table_schema'])
            self.tables_by_schemas[t['table_schema']].append(t['table_name'])
        all_views = cur.execute_query_blocking(q_views)
        for t in all_views:
            if t['table_schema'] not in self.schemas:
                self.schemas.append(t['table_schema'])
            self.views_by_schemas[t['table_schema']].append(t['table_name'])


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
        self.metadata = None
        ''':type: HostMetadata'''

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

    def get_metadata(self):
        hm = HostMetadata()
        hm.populate_metadata(self)
        return hm

class DBCursor(object):
    def __init__(self, dbconnection):
        self.dbconnection = dbconnection
        if dbconnection.connection is None:
            dbconnection.connect()
        self.cursor = dbconnection.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.rowcount = None
        # self.cstore = None
        self.columns = None
        self.datarows = None
        self.running = False
        self.available = True           #e.g. after data is offloaded
        self.thread = None
        ''':type : threading.Thread'''
        self.callback = None

    def process_query(self, query):
        self.running = True
        try:
            self.cursor.execute(query)
            self.columns = [desc[0] for desc in self.cursor.description]
            self.rowcount = self.cursor.rowcount
            self.datarows = self.cursor.fetchall()
            # self.cstore = {}
            # for row in self.cursor:
            #     for col in self.columns:
            #         data = row[col]
            #         if not self.cstore.get(col, None):
            #             self.cstore[col] = []
            #         self.cstore[col].append(data)
        except Exception as e:
            print e
        self.running = False
        self.callback()

    def execute_query_blocking(self, query):
        result = None
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        except Exception as e:
            print e
        return result

    def execute_query(self, query, callback):
        if self.available:
            try:
                self.callback = callback
                self.available = False
                self.thread = threading.Thread(target=self.process_query, args=(query,))
                self.thread.daemon = True
                self.thread.start()
            except Exception as e:
                self.available = True
                print e

    def cancel_query(self):
        if self.thread:
            if self.thread.isAlive():
                try:
                    self.thread._Thread__stop()
                    self.thread = None
                except Exception as e:
                    print('Thread could not be terminated:' + e.message)

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
    # print dbc
    # cur = DBCursor(dbc)
    # cur.execute_query('select pg_sleep(10)')
    # time.sleep(5)
    # cur.cancel_query()
    md = HostMetadata()
    md.populate_metadata(dbc)
    print md.databases
    print md.schemas
    print md.tables_by_schemas
    print md.views_by_schemas
