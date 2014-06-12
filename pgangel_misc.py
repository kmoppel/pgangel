#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk

def create_gridview_from_dict_list(columns_list, dict_list):
    columns_list =['Item', 'Quantity']
    types_list = [ type(x) for x in columns_list ]
    liststore = Gtk.ListStore(types_list)
    liststore.append(["Apples", "3"])

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

    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_hexpand(True)
    scrolled_window.set_vexpand(True)
    scrolled_window.add(treeview)
    return scrolled_window


if __name__ == '__main__':
    window = Gtk.Window()
    window.connect("destroy", lambda q: Gtk.main_quit())

    data = [{'col1':'aa', 'col2':'111'}, {'col1':'bb', 'col2':'222'}]
    gv = create_gridview_from_dict_list(['col1', 'col2'], data)
    window.add(gv)

    window.show_all()
    Gtk.main()