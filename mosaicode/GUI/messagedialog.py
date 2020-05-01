# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the Dialog class.
"""
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import gettext
_ = gettext.gettext


class MessageDialog(Gtk.MessageDialog):
    """
    This class contains methods related the Dialog class.
    """

    def __init__(self, title, message, main_window):
        """
        This method is the constuctor.

        Parameters:
            * **title** (:class:`str<str>`)
            * **message** (:class:`str<str>`)
            * **main_window** (:class:`MainWindow<mosaicode.GUI.mainwindow>`)
        """
        Gtk.MessageDialog.__init__(
                            self,
                            transient_for=main_window,
                            message_type=Gtk.MessageType.INFO,
                            text=title,
                            destroy_with_parent=True)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.format_secondary_text(message)
        self.show_all()
        self.run()
        self.destroy()
