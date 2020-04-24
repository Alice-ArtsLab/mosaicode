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

    def __init__(self):
        """
        This method is the constuctor.
        """
        self.dialog = Gtk.Dialog()

    # ----------------------------------------------------------------------

    def open_dialog(self, title, main_window, filetype=None, path=None):
        """
        This method open dialog box.

            Parameters:
                * **name** (:class:`str<str>`)
                * **main_window** (:class:`MainWindow<mosaicode.GUI.mainwindow>`)
            Returns:
                * **Types** (:class:`str<str>`)
        """
        self.dialog = Gtk.FileChooserDialog(
                            title=title,
                            transient_for=main_window,
                            action=Gtk.FileChooserAction.OPEN)
        self.dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.dialog.add_buttons(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        if path is not None:
            self.dialog.set_current_folder(path)

        allfiles = Gtk.FileFilter()
        allfiles.set_name(_("All Archives"))
        allfiles.add_pattern("*")
        self.dialog.add_filter(allfiles)

        if filetype is not None:
            filefilter = Gtk.FileFilter()
            filefilter.set_name(filetype)
            filefilter.add_pattern("*." +  filetype)
            self.dialog.add_filter(filefilter)

        response = self.dialog.show()
        file_name = ""
        if response == Gtk.ResponseType.OK:
            file_name = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            file_name = None
        self.dialog.destroy()
        return file_name

    # ----------------------------------------------------------------------
    def save_dialog(self,
                main_window,
                title="Save",
                filename=None,
                filetype=None):
        """
        This method open save dialog.

            Parameters:
                * **main_window** (:class:`MainWindow<mosaicode.GUI.mainwindow>`)
            Returns:
                * **Types** (:class:`str<str>`)
        """
        self.dialog = Gtk.FileChooserDialog(
                        title=title,
                        transient_for=main_window,
                        action=Gtk.FileChooserAction.SAVE)
        self.dialog.add_buttons(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL)
        self.dialog.add_buttons(Gtk.STOCK_SAVE, Gtk.ResponseType.OK)

        if filename is not None:
            self.dialog.set_filename(filename)
            self.dialog.set_current_name(filename)

        allfiles = Gtk.FileFilter()
        allfiles.set_name(_("All Archives"))
        allfiles.add_pattern("*.*")
        self.dialog.add_filter(allfiles)

        if filetype is not None:
            filefilter = Gtk.FileFilter()
            filefilter.set_name(filetype)
            filefilter.add_pattern("*." +  filetype)
            self.dialog.add_filter(filefilter)

        response = self.dialog.show()
        file_name = None

        if response == Gtk.ResponseType.OK:
            file_name = self.dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            file_name = None
        self.dialog.destroy()
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
        if name is None:
            return True
        if os.path.exists(name) is False:
            return True

        msg = _("Already exists a file with the same name in this folder.")
        msg = msg + _(" Do you want to continue?")
        result = self.confirm_dialog(msg, main_window)

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
        self.dialog = Gtk.MessageDialog(
                                    transient_for=main_window,
                                    message_type=Gtk.MessageType.INFO,
                                    text=title)
        self.dialog.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.dialog.format_secondary_text(message)
        self.dialog.show()
        self.dialog.destroy()

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
        self.dialog = Gtk.MessageDialog(
                            transient_for=main_window,
                            message_type=Gtk.MessageType.INFO,
                            text="",
                            destroy_with_parent=True)
        self.dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.dialog.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.dialog.format_secondary_text(message)
        result = self.dialog.show()
        self.dialog.destroy()
        return result
# ----------------------------------------------------------------------
