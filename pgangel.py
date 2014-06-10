#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import pgangel_gui
import pgangel_conf

class Pgangel(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='PgAngel')
        self.set_default_size(400, 200)
        grid = Gtk.Grid()
        self.add(grid)

        #uimanager = Gtk.UIManager()
        # uimanager.add_ui_from_file('mainmenu.xml')
        #accelgroup = uimanager.get_accel_group()
        #self.add_accel_group(accelgroup)
        button1 = Gtk.Button(label="Button 1")
        button2 = Gtk.Button(label="Button 2")
        button3 = Gtk.Button(label="Button 3")

        mb = Gtk.MenuBar()
        filemenu = Gtk.Menu()
        filem = Gtk.MenuItem("File")
        filem.set_submenu(filemenu)

        exit = Gtk.MenuItem("Exit")
        exit.connect("activate", Gtk.main_quit)
        filemenu.append(exit)

        agr = Gtk.AccelGroup()
        self.add_accel_group(agr)
        key, mod = Gtk.accelerator_parse("<Control>Q")
        exit.add_accelerator("activate", agr, key, mod, Gtk.AccelFlags.VISIBLE)

        mb.append(filem)

        grid.add(mb)
        grid.add(button1)
        grid.attach(button2, 1, 0, 2, 1)
        grid.attach_next_to(button3, button1, Gtk.PositionType.BOTTOM, 1, 2)
        self.connect('delete-event', Gtk.main_quit)


    def on_button1_clicked(self, widget):
        print 'Hello'


if __name__ == '__main__':
    pgangel_conf.ensure_app_folder_and_configs()

    win = Pgangel()
    current_servers = pgangel_conf.get_saved_servers()
    if len(current_servers) == 0:   # offer to create a server first
        ns = pgangel_gui.NewServer(win)
        ns.run()
        ns.destroy()
    win.show_all()
    Gtk.main()
