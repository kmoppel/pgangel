#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import pgangel_db
import pgangel_gui
import pgangel_conf
import pgangel_misc
import pgangel_connection_pool

def add_text_view_tab_to_notebook(notebook, label):
    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_hexpand(True)
    scrolled_window.set_vexpand(True)
    textview = Gtk.TextView()
    scrolled_window.add(textview)
    notebook.append_page(scrolled_window, Gtk.Label(label))
    return textview, scrolled_window

def replace_tab_in_notebook(notebook, tab_index, new_element, label):
    notebook.remove_page(tab_index)
    notebook.insert_page(new_element, Gtk.Label(label), tab_index)
    notebook.show_all()

class Pgangel():

    def __init__(self):
        self.window = None
        ''':type : gtk.Window'''
        self.toolbutton_expander = None
        ''':type : gtk.ToolButton'''
        self.revealer1 = None
        self.treeBarBox = None
        ''':type : gtk.HBox'''
        self.statusbar1 = None
        ''':type : gtk.Statusbar'''
        self.sb_context_id = None
        self.paned1 = None
        ''':type : gtk.Paned'''
        self.notebook1 = None
        ''':type : gtk.Notebook'''
        self.notebook2 = None
        ''':type : gtk.Notebook'''

        self.sql_tab1 = None
        self.output_tab = None
        self.servers = [] #DbServer
        # self.servers_list_store = None
        self.current_server = ''
        self.current_db_connection = None
        # ''':type : list(pgangel_db.DbServer)'''
        # self.db_servers[0].
        self.connectionPool = pgangel_connection_pool.ConnectionPool()
        self.cursor = None
        self.current_db_metadata = None
        ''':type : pgangel_db.HostMetadata'''
        self.treestore = None
        ''':type : gtk.TreeStore'''
        self.treeview = None
        ''':type : gtk.TreeView'''


    def build(self):
        builder = Gtk.Builder()
        builder.add_from_file("resources/main1.xml")
        builder.connect_signals(self)

        self.window = builder.get_object("window1")
        ''':type : gtk.Window'''
        self.toolbutton_expander = builder.get_object("toolbutton_expander")
        self.revealer1 = builder.get_object("revealer1")
        self.statusbar1 = builder.get_object("statusbar1")
        self.sb_context_id = self.statusbar1.get_context_id('messages')
        self.statusbar1.push(self.sb_context_id, 'statusbar...')
        self.paned1 = builder.get_object("paned1")
        ''':type : gtk.Paned'''
        self.combobox_servers = builder.get_object("combobox_servers")
        ''':type : gtk.ComboBox'''
        renderer_text = Gtk.CellRendererText()
        self.combobox_servers.pack_start(renderer_text, True)
        self.combobox_servers.add_attribute(renderer_text, "text", 0)

        tb_builder = Gtk.Builder()
        tb_builder.add_from_file("resources/treebox.xml")
        # tb_builder.connect_signals(self)
        box1 = tb_builder.get_object("box1")
        self.revealer1.add(box1)

        treestore = Gtk.TreeStore(str)
        treestore.append(None, ["Tables"])
        treestore.append(None, ["Views"])

        self.treestore = treestore

        treeview = Gtk.TreeView(model=treestore)
        ''':type : gtk.TreeView'''
        treeviewcolumn = Gtk.TreeViewColumn("Schemas")
        treeview.append_column(treeviewcolumn)
        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn.pack_start(cellrenderertext, True)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 0)
        box1.pack_start(treeview, True, True, 0)
        self.treeview = self.treeview

        self.notebook1 = Gtk.Notebook()
        sw1 = Gtk.ScrolledWindow()
        sw1.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        textview1 = Gtk.TextView()
        textview1.set_vexpand(True)
        textview1.set_hexpand(True)
        sw1.add(textview1)

        self.sql_tab1, scrollview = add_text_view_tab_to_notebook(self.notebook1, 'sql tab 1')
        # TODO need to map tabs to connections

        self.notebook2 = Gtk.Notebook()

        self.output_tab, self.output_tab_scrollview  = add_text_view_tab_to_notebook(self.notebook2, 'Data output')
        self.messages_tab, self.messages_tab_scrollview = add_text_view_tab_to_notebook(self.notebook2, 'Messages')
        self.history_tab, self.history_tab_scrollview =  add_text_view_tab_to_notebook(self.notebook2, 'History')

        self.paned1.add1(self.notebook1)
        self.paned1.add2(self.notebook2)
        self.paned1.set_position(450)

    def set_servers(self, servers):
        self.servers = []
        servers_list_store = Gtk.ListStore(str)
        servers_list_store.append([''])
        for s in servers:
            self.servers.append(s)
            servers_list_store.append([s.name])
        self.combobox_servers.set_model(servers_list_store)

    def on_delete(self, *args):
        Gtk.main_quit(args)

    def on_toolbutton_expander_clicked(self, *args):
        if self.revealer1.get_reveal_child():
            self.revealer1.set_reveal_child(False)
        else:
            self.revealer1.set_reveal_child(True)

    def on_toolbutton_new_tab_clicked(self, *args):
        self.statusbar1.push(self.sb_context_id, 'new tab opened...')

    def on_combobox_servers_changed(self, *args):
        pass

    def on_button_manage_servers_clicked(self, *args):
        self.statusbar1.push(self.sb_context_id, 'on_button_manage_servers_clicked...')

    def on_combobox_current_db_changed(self, *args):
        pass

    def on_button_connect_clicked(self, *args):
        i = self.combobox_servers.get_active()
        if i == 0:
            return
        model = self.combobox_servers.get_model()
        server_name = model[i][0]
        if self.current_server == server_name:
            return
        # connect
        s = self.servers[i]
        self.current_db_connection = pgangel_db.DBConnection(s.host, s.port, s.dbname, s.user)
        self.current_db_metadata = self.current_db_connection.get_metadata()
        self.statusbar1.push(self.sb_context_id, 'connection OK - [{}@{}:{}/{}]'.format(s.user, s.host, s.port, s.dbname))  # TODO add timestamp

        treestore = self.treestore
        treestore.clear()
        for schema in self.current_db_metadata.schemas:
            snode = treestore.append(None, [schema])
            tnode = treestore.append(snode, ["Tables"])
            vnode = treestore.append(snode, ["Views"])
            for table in self.current_db_metadata.tables_by_schemas[schema]:
                treestore.append(tnode, [table])
            for view in self.current_db_metadata.views_by_schemas[schema]:
                treestore.append(vnode, [view])

    def on_toolbutton_execute_clicked(self, *args):
        buf = self.sql_tab1.get_buffer()
        start, end = buf.get_bounds()
        text = buf.get_text(start, end, True)

        self.cursor = pgangel_db.DBCursor(self.current_db_connection)
        self.cursor.execute_query(text, self.query_execute_callback)

    def query_execute_callback(self):
        grid = pgangel_misc.create_gridview_from_column_list_and_dict_list(self.cursor.columns, self.cursor.datarows)

        replace_tab_in_notebook(self.notebook2, 0, grid, 'Data output')
        self.notebook2.set_current_page(0)
        self.notebook2.show_all()


if __name__ == '__main__':
    pgangel_conf.ensure_app_folder_and_configs()

    pga = Pgangel()
    pga.build()

    pga.servers = pgangel_conf.get_saved_servers()
    if len(pga.servers) == 0:   # offer to create a server first
        ns = pgangel_gui.ServerDialog()
        ns.build()
        ns.dialog.run()
        ns.dialog.destroy()
    pga.set_servers(pgangel_conf.get_saved_servers())   # refresh

    pga.window.show_all()
    Gtk.main()
