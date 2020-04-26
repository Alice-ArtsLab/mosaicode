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


class ConfirmDialog(Gtk.MessageDialog):
    """
    This class contains methods related the Dialog class.
    """

    def __init__(self, message, main_window):
        """
        This method is the constuctor.

            Parameters:
                * **message** (:class:`str<str>`)
                * **main_window** (:class:`MainWindow<mosaicode.GUI.mainwindow>`)
            Returns:
               * **Types:** (:class:`dialog<GTK.MessageDialog>`)
        """
        Gtk.MessageDialog.__init__(
                            self,
                            transient_for=main_window,
                            message_type=Gtk.MessageType.INFO,
                            text="",
                            destroy_with_parent=True)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.format_secondary_text(message)
        self.show_all()

    def run(self):
        result = super(Gtk.MessageDialog, self).run()
        self.close()
        self.destroy()
        return result
# ----------------------------------------------------------------------
