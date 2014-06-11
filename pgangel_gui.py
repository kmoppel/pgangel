#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk

import pgangel_conf
import pgangel_db

ns = None # 'new server' dialog handle

class ServerDialogHandler:
    def on_delete_window(self, *args):
        # print args
        args[0].destroy()
        #Gtk.main_quit(args)

    def on_button_test_connection_clicked(self, *args):
        dbc = pgangel_db.DBConnection()

    def on_button_ok_clicked(self, *args):
        print "ok"

    def on_button_cancel_clicked(self, *args):
        print "cancel"

class ServerDialog():
    def __init__(self):
        self.dialog = None
        self.entry_name = None
        self.entry_host = None
        self.entry_port = None
        self.entry_db = None
        self.entry_user = None
        self.entry_password = None

    def build(self):
        builder = Gtk.Builder()
        ''':type : gtk.Builder'''
        builder.add_from_file("resources/newserver1.xml")
        builder.connect_signals(self)

        # print builder.get_objects()
        self.dialog = builder.get_object("dialog1")
        ''':type : gtk.Dialog'''
        self.entry_port = builder.get_object("entry_port")


        # notebook1 = Gtk.Notebook()
        # textview1 = create_text()
        # textview2 = create_text()
        # notebook1.append_page(textview1, None)
        # notebook1.append_page(textview2, None)
        #
        # paned1.add1(notebook1)
        # textview3 = create_text()
        # paned1.add2(textview3)


    def on_delete_window(self, *args):
        print self.entry_port.get_text()
        args[0].destroy()
        #Gtk.main_quit(args)

    def on_button_test_connection_clicked(self, *args):
        dbc = pgangel_db.DBConnection()

    def on_button_ok_clicked(self, *args):
        print "ok"

    def on_button_cancel_clicked(self, *args):
        print "cancel"

if __name__ == '__main__':
    win = Gtk.Window(title='Testing')
    win.connect('delete-event', Gtk.main_quit)
    ns = ServerDialog()
    ns.build()
    # ns.dialog.set_parent(win)
    response = ns.dialog.run()
    # ns.destroy()
    win.show_all()
    Gtk.main()
    # print response

