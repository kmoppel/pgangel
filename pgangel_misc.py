#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk

def create_gridview_from_column_list_and_dict_list(columns_list, dict_list):
    types_list = [ type(x) for x in columns_list ]
    liststore = Gtk.ListStore(*types_list)

    for row_as_dict in dict_list:
        row = []
        for col in columns_list:
            row.append(str(row_as_dict[col]))
        liststore.append(row)

    treeview = Gtk.TreeView(model=liststore)

    for i, col in enumerate(columns_list):
        treeviewcolumn = Gtk.TreeViewColumn(col)
        treeview.append_column(treeviewcolumn)
        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn.pack_start(cellrenderertext, True)
        treeviewcolumn.add_attribute(cellrenderertext, "text", i)

    return treeview


if __name__ == '__main__':
    window = Gtk.Window()
    ''' :type : gtk.Window '''
    window.set_default_size(500, 300)
    window.connect("destroy", lambda q: Gtk.main_quit())

    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_hexpand(True)
    scrolled_window.set_vexpand(True)

    data = []
    for i in xrange(1,200):
        data.append({'col1':'aa'+str(i), 'col2':'val'+str(i)})
    gv = create_gridview_from_column_list_and_dict_list(['col1', 'col2'], data)
    scrolled_window.add(gv)
    window.add(scrolled_window)

    window.show_all()
    Gtk.main()