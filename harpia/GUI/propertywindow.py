# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import pkgutil # For dynamic package load
import inspect # For module inspect

import harpia.GUI.components

component_list = {} #Dynamic list to store components

class PropertyWindow(Gtk.VBox):

    def __init__(self):
        if not component_list: #load only if it is empty
            self.__load_components()
        self.plugin = None
        self.properties = {}
        Gtk.VBox.__init__(self)
        self.set_homogeneous(False)
        self.show_all()

    def set_block(self, plugin):
        self.plugin = plugin
        #Properties tab

        #Search plugin properties to create GUI
        for component in self.plugin.get_properties() :
            field = self._generate_field(component, self.plugin.get_properties()[component])
            self.add(field)

    def on_ok_clicked(self, widget, data):
        # It is time to look for values
        self._recursive_search(self)
        # Onde we have a returnable dictionary, call the callback method
        self.plugin.set_properties(self.properties)


    def _recursive_search(self, container):
        for widget in container.get_children() :
            #If widget is a container, search inside it
            if isinstance(widget, Gtk.Container) :
                self._recursive_search(widget)
            # Onde a component is found, search for it on the component list
            if widget.get_name() in self.plugin.get_properties() :
                self.properties[widget.get_name()] = widget.get_value()
    
    def _generate_field(self, component_key, component_attributes):
        type_ = component_attributes["type"]
        # zhu li, do the thing!
        #Creates a field based on the component list types
        field = component_list[type_](component_attributes)
        field.set_name(component_key) #Define widget name
        return field
    
    def __load_components(self):
        for importer, modname, ispkg in pkgutil.iter_modules(harpia.GUI.components.__path__):
            module = __import__("harpia.GUI.components." + modname, fromlist="dummy")
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    component_list[obj(None).get_type()] = obj
