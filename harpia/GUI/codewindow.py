#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from harpia.constants import *

class CodeWindow(Gtk.Window):

    def __init__(self, main_window, code):
        Gtk.Window.__init__(self, title="Harpia")
        self.set_parent(main_window)

        sw = Gtk.ScrolledWindow()
        self.add(sw)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        textview = Gtk.TextView()
        textview.set_left_margin(10)
        textview.set_right_margin(10)
        textview.get_buffer().set_text(code)

        sw.add(textview)
        textview.show()
        self.show_all()
        self.resize(800, 600)



