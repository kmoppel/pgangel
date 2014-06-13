#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2


class ConnectionPool():

    def __init__(self):
        self.connections = {}


    def get_connection_for_uri(self, connection_string):
        if uri is None:
            return
        if not uri in self.connections:
            self.connections[connection_string] = psycopg2.pool.ThreadedConnectionPool(1,5,None,connection_string)
        return self.connections[connection_string].getConn()
        
        

