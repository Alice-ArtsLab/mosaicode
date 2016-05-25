# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject


from filefilters import *

class Dialog():

# ----------------------------------------------------------------------
    def save_dialog(self, title, main_window):
        dialog = Gtk.FileChooserDialog(title, main_window,
                    Gtk.FileChooserAction.SAVE,
                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
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
