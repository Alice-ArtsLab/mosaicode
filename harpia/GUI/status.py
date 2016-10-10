#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
import datetime
from gi.repository import Gtk
from gi.repository import Pango

gi.require_version('Gtk', '3.0')


class Status(Gtk.ScrolledWindow):

    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.main_window = main_window

        self.status = Gtk.TextView()
        self.status.set_wrap_mode(Gtk.WrapMode.WORD)
        self.status.set_editable(False)
        self.status.set_left_margin(2)
        self.add(self.status)

        textbuffer = self.status.get_buffer()
        self.tag_bold = textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
        self.tag = textbuffer.create_tag("red", weight=Pango.Weight.NORMAL)
        self.tag_red = textbuffer.create_tag("normal", background="red")

    # ----------------------------------------------------------------------
    def clear(self):
        self.status.get_buffer().set_text("")

    # ----------------------------------------------------------------------
    def append_text(self, text):
        textbuffer = self.status.get_buffer()
        end_iter = textbuffer.get_end_iter()
        msg = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        textbuffer.insert_with_tags(end_iter, msg, self.tag_bold)

        end_iter = textbuffer.get_end_iter()
        msg = " - " + text + "\n"
        textbuffer.insert_with_tags(end_iter, msg, self.tag)
        self.status.scroll_to_mark(
            textbuffer.get_insert(), 0.0, True, 0.5, 0.5)

    # ----------------------------------------------------------------------
    def log(self, text):
        self.append_text(text)

# ----------------------------------------------------------------------
