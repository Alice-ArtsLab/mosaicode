#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Status class.
"""
import gi
import datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango


class Status(Gtk.ScrolledWindow):
    """
    This class contains methods related the Status class
    """

    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        """
        This method is the constructor.
            Args:
                self(Status)
                main_window()
            Returns:
                None
        """
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
        """
        The method clear the buffer.
        """
        self.status.get_buffer().set_text("")

    # ----------------------------------------------------------------------
    def append_text(self, text):
        """
        This method append a text in text buffer.
        
            Parameters:
                * **self** (:class:`Status<mosaicode.GUI.status>`):The class.
                * **text** (:class:`str<str>`)
        """
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
        """
        This method set the log.

            Parameters:
                * **text** (:class:`str<str>`)
        """
        self.append_text(text)

# ----------------------------------------------------------------------
