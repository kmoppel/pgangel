#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk

import pgangel_conf
import pgangel_db
import os

class ServerDialog():
    def __init__(self):
        self.dialog = None
        self.entry_name = None
        self.entry_host = None
        self.entry_port = None
        self.entry_db = None
        self.entry_user = None
        self.entry_password = None
        self.checkbox_save_password = None

    def build(self):
        builder = Gtk.Builder()
        ''':type : gtk.Builder'''
        builder.add_from_file("resources/newserver1.xml")
        builder.connect_signals(self)

        # print builder.get_objects()
        self.dialog = builder.get_object("dialog1")
        ''':type : gtk.Dialog'''
        self.entry_name = builder.get_object("entry_name")
        self.entry_host = builder.get_object("entry_host")
        self.entry_port = builder.get_object("entry_port")
        self.entry_db = builder.get_object("entry_db")
        self.entry_user = builder.get_object("entry_user")
        self.entry_password = builder.get_object("entry_password")
        self.checkbox_save_password = builder.get_object("checkbox_save_password")

        self.entry_user.set_text(os.getenv('USER'))

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
        password = self.entry_password.get_text()
        if len(password) == 0:
            pass # TODO get pass from ~/.pgangel/.passwords file
        dbc = pgangel_db.DBConnection(self.entry_host.get_text(), self.entry_port.get_text(), self.entry_db.get_text(), self.entry_user.get_text(), password)
        is_test_ok = dbc.try_connect()
        dialog = Gtk.MessageDialog(self.dialog, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Works!" if is_test_ok else "Naah:(") # TODO show exception
        dialog.run()
        dialog.destroy()
        # TODO - populate the "Database" combobox

    def on_button_ok_clicked(self, *args):
        # TODO validate input
        password = self.entry_password.get_text()
        if len(password) == 0:
            pass # TODO get pass from ~/.pgangel/.passwords file
        pgangel_conf.save_server(pgangel_db.DbServer(self.entry_name.get_text(),
                                                    pgangel_db.DBConnection(self.entry_host.get_text(), self.entry_port.get_text(),
                                                                            self.entry_db.get_text(), self.entry_user.get_text(), password)))
        self.dialog.hide()

    def on_button_cancel_clicked(self, *args):
        self.dialog.hide()

if __name__ == '__main__':
    pgangel_conf.ensure_app_folder_and_configs()

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

