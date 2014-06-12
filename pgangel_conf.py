#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pgangel_db import DbServer
from pgangel_db import DBConnection
import pgangel_io
import json

APP_FOLDER = '~/.pgangel'
SERVERS_CONF = APP_FOLDER + '/servers.conf'
PASSWORDS_FILE = APP_FOLDER + '/.passwords' # save passwords separately to enable regexes and to make sharing the servers.conf file with colleagues safer


def get_saved_servers():
    '''
    JSON format:
    [ {'name':'x', 'host':'x' , 'port':'x', 'db':'x', 'user':'x', 'password':'x'}
    ]
    '''
    ret=[]
    conf = pgangel_io.get_file_as_json(SERVERS_CONF)
    if conf:
        for s in conf:
            db = DbServer()
            db.name = s['name']
            password = get_password_from_passwords_file(s['db_conn']['host'], s['db_conn']['user'])
            # db.db_conn = DBConnection(s['db_conn']['host'], s['db_conn']['port'], s['db_conn']['db'], s['db_conn']['user'], password)
            # print db
            ret.append(db)
    return ret

def save_server(server):
    current_servers = get_saved_servers()
    is_update = False
    j = 0
    for i, s in enumerate(current_servers): # server change, remove old
        if s.name == server.name: # TODO add warning in UI
            is_update = True
            j = i
            break
    if is_update:
        current_servers.pop(j)
    current_servers.append(server)
    # for s in current_servers:
    #     print s
    pgangel_io.write_objects_to_file_as_json(current_servers, SERVERS_CONF)


def ensure_app_folder_and_configs():
    pgangel_io.ensure_folder(APP_FOLDER)
    pgangel_io.ensure_file(SERVERS_CONF)

def get_password_from_passwords_file(dbhost, username):
    return 'pass'


if __name__ == '__main__':
    # servers = get_saved_servers()
    # print 'len(servers)', len(servers)
    # print servers[0]
    dbc = DBConnection('host', 5432, 'postgres', 'kmoppel', '')
    dbs = DbServer('srv2', dbc)
    save_server(dbs)