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


class Dialog:
    """
    This class contains methods related the Dialog class.
    """

    # ----------------------------------------------------------------------

    def open_dialog(self, title, main_window, filetype=None):
        """
        This method open dialog box.

            Parameters:
                * **name** (:class:`str<str>`)
                * **main_window** (:class:`MainWindow<mosaicode.GUI.mainwindow>`)
            Returns:
                * **Types** (:class:`str<str>`)
        """
        dialog = Gtk.FileChooserDialog(title, main_window,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        allfiles = Gtk.FileFilter()
        allfiles.set_name(_("All Archives"))
        allfiles.add_pattern("*")
        dialog.add_filter(allfiles)

        if filetype is not None:
            filefilter = Gtk.FileFilter()
            filefilter.set_name(filetype)
            filefilter.add_pattern("*." +  filetype)
            dialog.add_filter(filefilter)

        response = dialog.run()
        file_name = ""
        if response == Gtk.ResponseType.OK:
            file_name = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            file_name = None
        dialog.destroy()
        return file_name

    # ----------------------------------------------------------------------
    def save_dialog(self, main_window, title="Save", filename=None, filetype=None):
        """
        This method open save dialog.

            Parameters:
                * **main_window** (:class:`MainWindow<mosaicode.GUI.mainwindow>`)
            Returns:
                * **Types** (:class:`str<str>`)
        """
        diagram = main_window.work_area.get_current_diagram()
        dialog = Gtk.FileChooserDialog(title,
                        main_window,
                        Gtk.FileChooserAction.SAVE,
                        (Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,
                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        if filename is not None:
            dialog.set_filename(filename)
            dialog.set_current_name(filename)

        allfiles = Gtk.FileFilter()
        allfiles.set_name(_("All Archives"))
        allfiles.add_pattern("*.*")
        dialog.add_filter(allfiles)

        if filetype is not None:
            filefilter = Gtk.FileFilter()
            filefilter.set_name(filetype)
            filefilter.add_pattern("*." +  filetype)
            dialog.add_filter(filefilter)

        response = dialog.run()
        file_name = None

        if response == Gtk.ResponseType.OK:
            file_name = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            file_name = None
        dialog.destroy()
        return file_name

    # ----------------------------------------------------------------------
    def confirm_overwrite(self, name, main_window):
        """
        This method confirm overwrite of the file.

            Parameters:
                * **name** (:class:`str<str>`)
                * **main_window** (:class:`MainWindow<mosaicode.GUI.mainwindow>`)
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        if os.path.exists(name) is False:
            return True

        msg = _("Already exists a file with the same name in this folder.")
        msg = msg + _(" Do you want to continue?")
        dialog = Dialog().confirm_dialog(msg, main_window)
        result = dialog.run()
        dialog.destroy()
        if result == Gtk.ResponseType.OK:
            return True
        if result == Gtk.ResponseType.CANCEL:
            return False

# ----------------------------------------------------------------------
    def message_dialog(self, title, message, main_window):
        """
        This method open message dialog.

            Parameters:
                * **title** (:class:`str<str>`)
                * **message** (:class:`str<str>`)
                * **main_window** (:class:`MainWindow<mosaicode.GUI.mainwindow>`)
        """
        dialog = Gtk.MessageDialog(main_window, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, title)
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

# ----------------------------------------------------------------------
    def confirm_dialog(self, message, main_window):
        """
        This method open confirm dialog.

            Parameters:
                * **message** (:class:`str<str>`)
                * **main_window** (:class:`MainWindow<mosaicode.GUI.mainwindow>`)
            Returns:
               * **Types:** (:class:`dialog<GTK.MessageDialog>`)
        """
        dialog = Gtk.MessageDialog(main_window,
                            0,
                            Gtk.MessageType.INFO,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                            Gtk.STOCK_OK, Gtk.ResponseType.OK),  "")
        dialog.format_secondary_text(message)
        return dialog

# ----------------------------------------------------------------------
