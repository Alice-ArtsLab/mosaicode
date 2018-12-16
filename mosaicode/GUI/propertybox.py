# -*- coding: utf-8 -*-
"""
This module contains the PropertyBox class.
"""
import gi
gi.require_version('Gtk', '3.0')
import inspect  # For module inspect
import pkgutil  # For dynamic package load
import mosaicomponents
from gi.repository import Gtk
from gi.repository import Gdk
from mosaicode.GUI.fieldtypes import *
import gettext
_ = gettext.gettext


class PropertyBox(Gtk.VBox):
    """
    This class contains methods related the PropertyBox class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        Gtk.VBox.__init__(self, True)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.add(scrolled_window)

        self.vbox = Gtk.VBox(self, True)
        scrolled_window.add(self.vbox)
        self.main_window = main_window
        self.block = None
        self.comment = None
        self.properties = {}
        self.vbox.set_homogeneous(False)
        self.vbox.set_property("border-width", 0)
        white = Gdk.RGBA(1, 1, 1, 1)
        self.override_background_color(Gtk.StateType.NORMAL, white)
        self.show_all()

# ----------------------------------------------------------------------
    def set_diagram(self, diagram):
        """
        This method set the property of the diagram.

            Parameters:
                * **comment** (:class:`PropertyBox<mosaicode.GUI.propertybox>`)
            Returns:
                None
        """
        # First, remove all components
        for widget in self.vbox.get_children():
            self.vbox.remove(widget)

        data1 = {"label": _("Diagram"),
                "name": "file_name",
                "value": diagram.file_name}
        field = LabelField(data1, self.notify_comment)
        self.vbox.pack_start(field, False, False, 0)

        
        data2 = {"label": _("Language"),
                "name": "language",
                "value": diagram.language}
        field2 = LabelField(data2, self.notify_comment)
        self.vbox.pack_start(field2, False, False, 0)

        value = "None"
        if diagram.code_template is None:
            return

        value = diagram.code_template.name
        data3 = {"label": _("Code Template"),
                "name": "code_template",
                "value": value}
        field3 = LabelField(data3, self.notify_comment)
        self.vbox.pack_start(field3, False, False, 0)
        for prop in diagram.code_template.get_properties():
            field = self._generate_field(prop.get("name"), prop)
            self.properties[prop.get("name")] = ""
            if prop["type"] == MOSAICODE_OPEN_FILE or \
                    prop["type"] == MOSAICODE_SAVE_FILE:
                field.set_parent_window(self.main_window)
            self.vbox.pack_start(field, False, False, 0)

# ----------------------------------------------------------------------
    def set_comment(self, comment):
        """
        This method set the comment.

            Parameters:
                * **comment** (:class:`PropertyBox<mosaicode.GUI.propertybox>`)
            Returns:
                None
        """
        self.comment = comment
        # First, remove all components
        for widget in self.vbox.get_children():
            self.vbox.remove(widget)
        self.__generate_fields(self.comment.get_properties(), self.notify_comment)

# ----------------------------------------------------------------------
    def notify_comment(self, widget=None, data=None):
        """
        This method notify modifications in propertybox
        """
        self.__recursive_search(self.vbox)
        self.comment.set_properties(self.properties)

# ----------------------------------------------------------------------
    def set_block(self, block):
        """
        This method set properties the block.

            Parameters:
                * **block** (:class:`PropertyBox<mosaicode.GUI.propertybox>`)
            Returns:
                None
        """
        self.block = block
        # First, remove all components
        for widget in self.vbox.get_children():
            self.vbox.remove(widget)

        data1 = {"label": "Block",
                "name": "",
                "value": block.label}
        field = LabelField(data1, None)
        self.vbox.pack_start(field, False, False, 0)
        self.__generate_fields(self.block.get_properties(), self.notify_block)

# ----------------------------------------------------------------------
    def notify_block(self, widget=None, data=None):
        """
        This method notify modifications in propertybox
        """
        # It is time to look for values
        self.__recursive_search(self.vbox)
        # we have a returnable dictionary, call the callback method
        self.block.set_properties(self.properties)

# ----------------------------------------------------------------------
    def __recursive_search(self, container):
        for widget in container.get_children():
            # If widget is a container, search inside it
            if isinstance(widget, Gtk.Container):
                self.__recursive_search(widget)
            # Once a component is found, search for it on the component list
            if widget.get_name() in self.properties:
                self.properties[widget.get_name()] = widget.get_value()

# ----------------------------------------------------------------------
    def __generate_fields(self, props, callback):
        self.properties = {}
        for prop in props:
            field = component_list[prop["type"]](prop, callback)
            self.properties[prop.get("name")] = ""
            if prop["type"] == MOSAICODE_OPEN_FILE or \
                    prop["type"] == MOSAICODE_SAVE_FILE:
                field.set_parent_window(self.main_window)
            self.vbox.pack_start(field, False, False, 0)
        if len(props) == 0:
            data1 = {"label": "No property is available",
                "name": "",
                "value": ""}
            field = LabelField(data1, None)
            self.vbox.pack_start(field, False, False, 0)

# ----------------------------------------------------------------------
