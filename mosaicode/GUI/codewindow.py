#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the CodeWindow class.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource
import gettext
_ = gettext.gettext


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

        self.main_window = main_window
        self.set_default_size(800, 600)
        box = self.get_content_area()
        vbox = Gtk.VBox()
        box.pack_start(vbox, True, True, 0)

        toolbar = Gtk.Toolbar()
        toolbar.set_style(Gtk.ToolbarStyle.BOTH)
        toolbar.set_hexpand(False)
        toolbar.set_property("expand", False)
        vbox.pack_start(toolbar, False, False, 0)


        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_SAVE_AS)
        button.set_expand(False)
        button.set_label(_("Save Source"))
        button.set_is_important(True)
        button.connect("clicked", self.__save_button_clicked, None)
        toolbar.add(button)

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_EXECUTE)
        button.set_expand(False)
        button.set_label(_("Run this code"))
        button.set_is_important(True)
        button.connect("clicked", self.__run_button_clicked, None)
        toolbar.add(button)

        sw = Gtk.ScrolledWindow()
        vbox.pack_start(sw, True, True, 0)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        lang_manager = GtkSource.LanguageManager()
        textbuffer = GtkSource.Buffer.new_with_language(
            lang_manager.get_language('c'))
        textview = GtkSource.View.new_with_buffer(textbuffer)
        textview.set_show_line_numbers(True)
        textview.set_left_margin(10)
        textview.set_right_margin(10)
        textview.get_buffer().set_text(code)
        self.buffer = textview.get_buffer()

        sw.add(textview)
        textview.show()
        self.show_all()

    # ----------------------------------------------------------------------
    def __save_button_clicked(self, widget, data):
        """
        This method monitors if the button was clicked.

            Parameters:

        """
        code = self.buffer.get_text( self.buffer.get_start_iter(),
                    self.buffer.get_end_iter(), True)
        self.main_window.main_control.save_source(code)

    # ----------------------------------------------------------------------
    def __run_button_clicked(self, widget, data):
        """
        This method monitors if the button was clicked.

            Parameters:

        """
        code = self.buffer.get_text( self.buffer.get_start_iter(),
                    self.buffer.get_end_iter(), True)
        self.main_window.main_control.run(code)

# ----------------------------------------------------------------------
