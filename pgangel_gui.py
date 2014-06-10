#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk

class NewServer(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Create a new server", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        label = Gtk.Label("This is a dialog to display additional information")

        box = self.get_content_area()
        box.add(label)
        self.set_default_size(500, 400)

        self.entry = Gtk.Entry()
        self.entry.set_text("localhost")
        box.pack_end(self.entry, True, True, 0)
        # self.show_all()


if __name__ == '__main__':
    win = Gtk.Window(title='Testing')
    win.connect('delete-event', Gtk.main_quit)

    ns = NewServer(win)
    response = ns.run()
    ns.destroy()
    win.show_all()
    Gtk.main()
    print response

