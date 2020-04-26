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


class OpenDialog(Gtk.FileChooserDialog):
    """
    This class contains methods related the Dialog class.
    """

    def __init__(self, title, main_window, filetype=None, path=None):
        """
        This method is the constuctor.

            Parameters:
                * **name** (:class:`str<str>`)
                * **main_window** (:class:`MainWindow<mosaicode.GUI.mainwindow>`)
            Returns:
                * **Types** (:class:`str<str>`)
        """
        Gtk.FileChooserDialog.__init__(
                            self,
                            title=title,
                            transient_for=main_window,
                            action=Gtk.FileChooserAction.OPEN,
                            destroy_with_parent=True)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_buttons(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        if path is not None:
            self.set_current_folder(path)

        allfiles = Gtk.FileFilter()
        allfiles.set_name(_("All Archives"))
        allfiles.add_pattern("*")
        self.add_filter(allfiles)

        if filetype is not None:
            filefilter = Gtk.FileFilter()
            filefilter.set_name(filetype)
            filefilter.add_pattern("*." +  filetype)
            self.add_filter(filefilter)
        self.show_all()

    def run(self):
        response = super(Gtk.FileChooserDialog, self).run()
        file_name = None
        if response == Gtk.ResponseType.OK:
            file_name = self.get_filename()
        self.close()
        self.destroy()
        return file_name
