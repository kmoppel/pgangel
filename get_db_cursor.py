#!/usr/bin/env python

import os
import re
import psycopg2
import psycopg2.extras

def get_file_content(filename):
    with open(filename, r'r') as f:
        return f.read()


def get_db_cursor(db_host, db_name, db_port='5432', db_user=None, db_pass=None):
    if not (db_user and db_pass):
        pgpass = os.path.expanduser('~/.pgpass')
        auths = [re.sub('#.*$|\n', '', line) for line in open( pgpass, r'r') if not re.match('#.*', line.strip())]
        auths = [line.replace('*', '.*') for line in auths]   #pgpass *'s are converted to .*'s
        for auth in auths:
            auth_parts = auth.split(':')    #host:port:database:user:pass
            if re.match(auth_parts[0], db_host) and re.match(auth_parts[1], db_port) and re.match(auth_parts[2], db_name):
                db_user = db_user or auth_parts[3]
                db_pass = db_pass or auth_parts[4]
    conn_string = r'host=' + db_host + r' dbname=' + db_name + ' port=' + db_port + r' user=' + db_user + r' password=' + db_pass
    db_conn = psycopg2.connect(conn_string)
    db_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    db_cur = db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return db_cur
