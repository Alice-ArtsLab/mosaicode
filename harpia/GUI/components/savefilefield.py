import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

from harpia.GUI.components.field import Field
from harpia.GUI.fieldtypes import *

class SaveFileField(Field, Gtk.HBox):

    def __init__(self, data, event):
        if not isinstance(data,dict):
            return
        self.file = data["value"]
        Gtk.HBox.__init__(self, False)
        self.label = Gtk.Label(data["name"])
        self.label.set_property("halign", Gtk.Align.START)
        self.add(self.label)

        self.field = Gtk.Entry()
        self.field.set_text(self.file)
        self.field.connect("changed", event)
        self.add(self.field)

        button = Gtk.Button.new_from_icon_name("gtk-file",Gtk.IconSize.BUTTON)
        button.connect("clicked", self.on_choose_file)
        self.add(button)
        self.show_all()

    def on_choose_file(self, widget):
        dialog = Gtk.FileChooserDialog("Salvar...",
                                       None,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                       Gtk.ResponseType.CANCEL,
                                       Gtk.STOCK_SAVE,
                                       Gtk.ResponseType.OK)
                                        )
        dialog.set_current_folder(self.field.get_text())

        filter = Gtk.FileFilter()
        filter.set_name("images")
        filter.add_mime_type("*.jpg")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.field.set_text(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.destroy()

    def get_type(self):
        return HARPIA_SAVE_FILE

    def get_value(self):
        return self.field.get_text()
