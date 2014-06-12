#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import pgangel_gui
import pgangel_conf

class Pgangel():

    def __init__(self):
        self.window = None
        ''':type : gtk.pgadow'''
        self.toolbutton1 = None
        ''':type : gtk.ToolButton'''
        self.db_servers = None
        # ''':type : list(pgangel_db.DbServer)'''
        # self.db_servers[0].

    def build(self):
        builder = Gtk.Builder()
        ''':type : gtk.Builder'''
        builder.add_from_file("resources/main1.xml")
        builder.connect_signals(self)

        # print builder.get_objects()
        self.dialog = builder.get_object("dialog1")
        ''':type : gtk.Dialog'''
        self.entry_name = builder.get_object("entry_name")
        self.connect('delete-event', Gtk.main_quit)


    def on_delete_pgadow(self, *args):
        Gtk.main_quit(args)


if __name__ == '__main__':
    pgangel_conf.ensure_app_folder_and_configs()

    pga = Pgangel()
    pga.db_servers = pgangel_conf.get_saved_servers()
    if len(pga.db_servers) == 0:   # offer to create a server first
        ns = pgangel_gui.NewServer(pga)
        ns.run()
        ns.destroy()

    pga.window.show_all()
    Gtk.main()
