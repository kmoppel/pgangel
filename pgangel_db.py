#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import psycopg2
import psycopg2.extras
import json


class DBConnection(object):

    def __init__(self, host, database, port='5432', username=None, password=None):
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
        self.database = database
        self.port = port
        self.username = username
        self.password = password
        self.connection = None

    def try_connect(self):
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
        self.cursor = dbconnection.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #self.columns = None

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            #self.columns = [desc[0] for desc in self.cursor.description]
            return True
        except Exception as e:
            print e
        return False

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
    dbs = DbServer('srv1', 'local', '5432', 'postgres', 'kmoppel')
    # print dbc.try_connect()
    print dbs

