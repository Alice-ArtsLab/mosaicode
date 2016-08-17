# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------

import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject


from filefilters import *

class Dialog():

# ----------------------------------------------------------------------
    def open_dialog(self, title, main_window):
        dialog = Gtk.FileChooserDialog(title, main_window,
                    Gtk.FileChooserAction.OPEN,
                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
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

#------------------------------------------------------------------------------
    def confirm_overwrite(self, name, main_window):
        msg = "Already exists a file with the same name in this folder.\nDo you want to continue?"
        if os.path.exists(name) !=True:
            name=(("%s"+".hrp")%name)
            if os.path.exists(name) == True:
                dialog2 = Dialog().confirm_dialog(msg, main_window)
                result = dialog2.run() 
                dialog2.destroy()
                if result ==  Gtk.ResponseType.OK:
                    pass
                if result ==  Gtk.ResponseType.CANCEL:
                    dialog2.destroy()
        elif os.path.exists(name) == True:
                dialog2 = Dialog().confirm_dialog(msg, main_window)
                result = dialog2.run() 
                dialog2.destroy()
                if result ==  Gtk.ResponseType.OK:
                    pass
                if result ==  Gtk.ResponseType.CANCEL:
                    dialog2.destroy()

# ----------------------------------------------------------------------
    def save_dialog(self, title, main_window):
        diagram = main_window.work_area.get_current_diagram()
        dialog = Gtk.FileChooserDialog(title, main_window,
                    Gtk.FileChooserAction.SAVE,
                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        dialog.add_filter(AllFileFilter())
        dialog.add_filter(HarpiaFileFilter())

        response = dialog.run()
        file_name = ""
        name=None
        name=dialog.get_filename()
        if name != None:
        	self.confirm_overwrite(name, main_window)

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
                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
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
