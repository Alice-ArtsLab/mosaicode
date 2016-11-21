# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------

import gi
import os
from filefilters import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from harpia.GUI.components.stringfield import StringField
import gettext
_ = gettext.gettext


class Dialog():

    # ----------------------------------------------------------------------

    def open_dialog(self, title, main_window):
        dialog = Gtk.FileChooserDialog(title, main_window,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        dialog.add_filter(AllFileFilter())
        dialog.add_filter(HarpiaFileFilter())

        response = dialog.run()
        file_name = ""
        if response == Gtk.ResponseType.OK:
            file_name = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            file_name = None
        dialog.destroy()
        return file_name

    # ----------------------------------------------------------------------

    def confirm_overwrite(self, name, main_window):
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
    def save_dialog(self, title, main_window):
        diagram = main_window.work_area.get_current_diagram()
        dialog = Gtk.FileChooserDialog(title, main_window,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        dialog.add_filter(AllFileFilter())
        dialog.add_filter(HarpiaFileFilter())

        response = dialog.run()
        file_name = ""

        if response == Gtk.ResponseType.OK:
            file_name = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            file_name = None
        dialog.destroy()
        return file_name

    # ----------------------------------------------------------------------
    def save_png_dialog(self, title, main_window):
        dialog = Gtk.FileChooserDialog(title, main_window,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        dialog.add_filter(PNGFileFilter())

        response = dialog.run()
        file_name = ""
        if response == Gtk.ResponseType.OK:
            file_name = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            file_name = None
        dialog.destroy()
        return file_name

# ----------------------------------------------------------------------
    def message_dialog(self, title, message, main_window):
        dialog = Gtk.MessageDialog(main_window, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, title)
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

# ----------------------------------------------------------------------
    def confirm_dialog(self, message, main_window):
        dialog = Gtk.MessageDialog(main_window, 0, Gtk.MessageType.INFO,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OK, Gtk.ResponseType.OK),  "")
        dialog.format_secondary_text(message)
        return dialog

# ----------------------------------------------------------------------
    def rename_dialog(self, main_window, diagram):
        dialog = Gtk.Dialog(_("Rename"), main_window,
                            0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_OK, Gtk.ResponseType.OK))

        box = dialog.get_content_area()
        vbox = Gtk.VBox()
        box.add(vbox)

        # File name
        data = {"name": _("File name"),
                "value": diagram.get_file_name()}
        self.file_name = StringField(data, None)
        vbox.add(self.file_name)

        dialog.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            diagram.set_file_name(self.file_name.get_value())

        dialog.close()
        dialog.destroy()

        return


# ----------------------------------------------------------------------
