#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class BlockDescription(Gtk.ScrolledWindow):

    def __init__(self, main_window):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.main_window = main_window

        self.description = Gtk.TextView()
        self.description.set_wrap_mode(Gtk.WrapMode.WORD)
        self.description.set_editable(False)
        self.description.set_left_margin(2)
        self.add(self.description)

    def set_text(self, text):
        self.description.get_buffer().set_text(text)
