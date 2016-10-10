# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

import pkgutil  # For dynamic package load
import inspect  # For module inspect

import harpia.GUI.components
from harpia.GUI.fieldtypes import *

component_list = {}  # Dynamic list to store components


class PropertyBox(Gtk.VBox):

# ----------------------------------------------------------------------

    def __init__(self, main_window):
        if not component_list:  # load only if it is empty
            self.__load_components()
        self.main_window = main_window
        self.block = None
        self.properties = {}
        Gtk.VBox.__init__(self)
        self.set_homogeneous(False)
        self.set_property("border-width", 0)
        white = Gdk.RGBA(1, 1, 1, 1)
        self.override_background_color(Gtk.StateType.NORMAL, white)
        self.show_all()

# ----------------------------------------------------------------------
    def set_block(self, block):
        self.block = block
        # First, remove all components
        for widget in self.get_children():
            self.remove(widget)

        # Search block properties to create GUI
        for component in self.block.get_properties():
            prop = self.block.get_properties()[component]
            prop["value"] = self.block.get_plugin().__dict__[component]
            field = self._generate_field(component, prop)
            if prop["type"] == HARPIA_OPEN_FILE or prop["type"] == HARPIA_SAVE_FILE:
                field.set_parent_window(self.main_window)
            self.pack_start(field, False, False, 0)

# ----------------------------------------------------------------------
    def notify(self, widget=None, data=None):
        # It is time to look for values
        self.__recursive_search(self)
        # we have a returnable dictionary, call the callback method
        self.block.set_properties(self.properties)

# ----------------------------------------------------------------------
    def __recursive_search(self, container):
        for widget in container.get_children():
            # If widget is a container, search inside it
            if isinstance(widget, Gtk.Container):
                self.__recursive_search(widget)
            # Onde a component is found, search for it on the component list
            if widget.get_name() in self.block.get_properties():
                self.properties[widget.get_name()] = widget.get_value()

# ----------------------------------------------------------------------
    def _generate_field(self, component_key, component_attributes):
        type_ = component_attributes["type"]
        field = component_list[type_](component_attributes, self.notify)
        field.set_name(component_key)  # Define widget name
        return field

# ----------------------------------------------------------------------
    def __load_components(self):
        for importer, modname, ispkg in pkgutil.iter_modules(harpia.GUI.components.__path__):
            module = __import__(
                "harpia.GUI.components." + modname, fromlist="dummy")
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    component_list[obj(None, self.notify).get_type()] = obj
# ----------------------------------------------------------------------
