#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import pgangel_gui
import pgangel_conf

class Pgangel():

    def __init__(self):
        self.window = None
        ''':type : gtk.Window'''
        self.toolbutton1 = None
        ''':type : gtk.ToolButton'''
        self.revealer1 = None
        self.treeBarBox = None
        ''':type : gtk.HBox'''

        self.db_servers = None
        # ''':type : list(pgangel_db.DbServer)'''
        # self.db_servers[0].


    def build(self):
        builder = Gtk.Builder()
        builder.add_from_file("resources/main1.xml")
        builder.connect_signals(self)

        self.window = builder.get_object("window1")
        ''':type : gtk.Window'''
        self.toolbutton1 = builder.get_object("toolbutton1")
        self.revealer1 = builder.get_object("revealer1")

        tb_builder = Gtk.Builder()
        tb_builder.add_from_file("resources/treebox.xml")
        # tb_builder.connect_signals(self)
        box1 = tb_builder.get_object("box1")
        liststore = Gtk.ListStore(str, int)
        liststore.append(["Oranges", 5])
        liststore.append(["Apples", 3])
        liststore.append(["Bananas", 1])
        liststore.append(["Tomatoes", 4])
        liststore.append(["Cucumber", 1])
        treeview = Gtk.TreeView(model=liststore)

        treeviewcolumn = Gtk.TreeViewColumn("Item")
        treeview.append_column(treeviewcolumn)
        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn.pack_start(cellrenderertext, True)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 0)

        treeviewcolumn = Gtk.TreeViewColumn("Quantity")
        treeview.append_column(treeviewcolumn)
        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn.pack_start(cellrenderertext, True)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 1)

        box1.pack_start(treeview, False, True, 0)

        self.revealer1.add(box1)


    def on_delete(self, *args):
        Gtk.main_quit(args)

    def on_toolbutton1_clicked(self, *args):
        if self.revealer1.get_reveal_child():
            self.revealer1.set_reveal_child(False)
        else:
            self.revealer1.set_reveal_child(True)


if __name__ == '__main__':
    pgangel_conf.ensure_app_folder_and_configs()

    pga = Pgangel()
    pga.build()

    pga.db_servers = pgangel_conf.get_saved_servers()
    if len(pga.db_servers) == 0:   # offer to create a server first
#        ns = pgangel_gui.NewServer(pga)
        ns = pgangel_gui.ServerDialog()
        ns.build()
#        ns.run()
#        ns.destroy()
    pga.db_servers = pgangel_conf.get_saved_servers()   # refresh

    pga.window.show_all()
    Gtk.main()
