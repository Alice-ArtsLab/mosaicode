#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This file contains the CodeWindow class.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource


class CodeWindow(Gtk.Dialog):

    """
    This class contains the methods related to CodeWindow class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, main_window, code):
        """
        This method is the constructor.
        """
        Gtk.Dialog.__init__(self, "Code Window", main_window,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT |
                            Gtk.DialogFlags.MODAL,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(800, 600)
        sw = Gtk.ScrolledWindow()
        box = self.get_content_area()
        box.pack_start(sw, True, True, 0)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        lang_manager = GtkSource.LanguageManager()
        textbuffer = GtkSource.Buffer.new_with_language(
            lang_manager.get_language('c'))
        textview = GtkSource.View.new_with_buffer(textbuffer)
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
