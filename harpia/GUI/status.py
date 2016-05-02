#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Status(Gtk.ScrolledWindow):

    def __init__(self, main_window):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.main_window = main_window

        self.status = Gtk.TextView()
        self.status.set_wrap_mode(Gtk.WrapMode.WORD)
        self.status.set_editable(False)
        self.status.set_left_margin(2)
        self.add(self.status)

    def clear(self):
        self.status.get_buffer().set_text("")

    def append_text(self, text):
        self.status.get_buffer().insert_at_cursor(text, len(text))
