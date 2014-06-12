#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import pgangel_gui
import pgangel_conf

def add_text_view_tab_to_notebook(notebook, label):
    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_hexpand(True)
    scrolled_window.set_vexpand(True)
    textview = Gtk.TextView()
    scrolled_window.add(textview)
    notebook.append_page(scrolled_window, Gtk.Label(label))
    return textview


class Pgangel():

    def __init__(self):
        self.window = None
        ''':type : gtk.Window'''
        self.toolbutton1 = None
        ''':type : gtk.ToolButton'''
        self.revealer1 = None
        self.treeBarBox = None
        ''':type : gtk.HBox'''
        self.statusbar1 = None
        ''':type : gtk.Statusbar'''
        self.sb_context_id = None
        self.paned1 = None
        ''':type : gtk.Paned'''

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
        self.statusbar1 = builder.get_object("statusbar1")
        self.sb_context_id = self.statusbar1.get_context_id('messages')
        self.statusbar1.push(self.sb_context_id, 'statusbar...')
        self.paned1 = builder.get_object("paned1")
        ''':type : gtk.Paned'''

        tb_builder = Gtk.Builder()
        tb_builder.add_from_file("resources/treebox.xml")
        # tb_builder.connect_signals(self)
        box1 = tb_builder.get_object("box1")
        self.revealer1.add(box1)

        treestore = Gtk.TreeStore(str)
        dog = treestore.append(None, ["Dog"])
        treestore.append(dog, ["Fido"])
        treestore.append(dog, ["Spot"])
        cat = treestore.append(None, ["Cat"])
        treestore.append(cat, ["Ginger"])
        rabbit = treestore.append(None, ["Rabbit"])
        treestore.append(rabbit, ["Twitch"])
        treestore.append(rabbit, ["Floppy"])
        treeview = Gtk.TreeView(model=treestore)
        treeviewcolumn = Gtk.TreeViewColumn("Pet Names")
        treeview.append_column(treeviewcolumn)
        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn.pack_start(cellrenderertext, True)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 0)
        box1.pack_start(treeview, False, True, 0)

        notebook1 = Gtk.Notebook()
        sw1 = Gtk.ScrolledWindow()
        sw1.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        textview1 = Gtk.TextView()
        textview1.set_vexpand(True)
        textview1.set_hexpand(True)
        sw1.add(textview1)

        sql_tab1 = add_text_view_tab_to_notebook(notebook1, 'sql tab 1')
        # TODO need to map tabs to connections

        notebook2 = Gtk.Notebook()
        add_text_view_tab_to_notebook(notebook2, 'data output')

        self.paned1.add1(notebook1)
        self.paned1.add2(notebook2)
        self.paned1.set_position(450)


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
