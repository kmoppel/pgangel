#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pgangel_db import DbServer
import pgangel_io

APP_FOLDER = '~/.pgangel'
SERVERS_CONF = APP_FOLDER + '/servers.conf'


def get_saved_servers():
    ret=[]
    conf = pgangel_io.get_file_as_json(SERVERS_CONF)
    if 'servers' in conf:
        for s in conf['servers']:
            db = DbServer() # TODO
            ret.append(db)
    return ret

def ensure_app_folder_and_configs():
    pgangel_io.ensure_folder(APP_FOLDER)
    pgangel_io.ensure_file(SERVERS_CONF)

def get_password_from_passwords_file(dbhost, username):
    return 'pass'