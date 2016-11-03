#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource


class CodeWindow(Gtk.Dialog):

    # ----------------------------------------------------------------------

    def __init__(self, main_window, code):
        Gtk.Dialog.__init__(self, "Code Window", main_window,
                            0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(800, 600)
        sw = Gtk.ScrolledWindow()
        box = self.get_content_area()
        box.pack_start(sw, True, True, 0)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        textview = GtkSource.View()
        textview.set_show_line_numbers(True)
        textview.set_left_margin(10)
        textview.set_right_margin(10)
        textview.get_buffer().set_text(code)

        sw.add(textview)
        textview.show()
        self.show_all()
        self.run()
        self.close()
        self.destroy()
# ----------------------------------------------------------------------
