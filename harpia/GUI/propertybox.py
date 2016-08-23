# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

import pkgutil # For dynamic package load
import inspect # For module inspect

import harpia.GUI.components

component_list = {} #Dynamic list to store components

class PropertyWindow(Gtk.VBox):

# ----------------------------------------------------------------------
    def __init__(self):
        if not component_list: #load only if it is empty
            self.__load_components()
        self.plugin = None
        self.properties = {}
        Gtk.VBox.__init__(self)
        self.set_homogeneous(False)
        self.set_property("border-width", 0)
        self.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1, 1, 1, 1))
        self.show_all()

# ----------------------------------------------------------------------
    def set_block(self, plugin):
        self.plugin = plugin
        # First, remove all components
        for widget in self.get_children() :
            self.remove(widget)

        #Search plugin properties to create GUI
        for component in self.plugin.get_properties() :
            field = self._generate_field(component, self.plugin.get_properties()[component])
            self.pack_start(field, False, False, 0)

# ----------------------------------------------------------------------
    def notify(self, widget = None, data = None):
        # It is time to look for values
        self.__recursive_search(self)
        # we have a returnable dictionary, call the callback method
        self.plugin.set_properties(self.properties)

# ----------------------------------------------------------------------
    def __recursive_search(self, container):
        for widget in container.get_children() :
            #If widget is a container, search inside it
            if isinstance(widget, Gtk.Container) :
                self.__recursive_search(widget)
            # Onde a component is found, search for it on the component list
            if widget.get_name() in self.plugin.get_properties() :
                self.properties[widget.get_name()] = widget.get_value()

# ----------------------------------------------------------------------
    def _generate_field(self, component_key, component_attributes):
        type_ = component_attributes["type"]
        field = component_list[type_](component_attributes, self.notify)
        field.set_name(component_key) #Define widget name
        return field

# ----------------------------------------------------------------------
    def __load_components(self):
        for importer, modname, ispkg in pkgutil.iter_modules(harpia.GUI.components.__path__):
            module = __import__("harpia.GUI.components." + modname, fromlist="dummy")
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    component_list[obj(None, self.notify).get_type()] = obj
# ----------------------------------------------------------------------
