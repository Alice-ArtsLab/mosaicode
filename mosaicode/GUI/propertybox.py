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
        self.diagram = None
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
        self.diagram = diagram
        if diagram.code_template is None:
            data3 = {"label": _("Choose a Code Template"),
                    "name": "code_template",
                    "value": ""}
            return
        self.__generate_fields(diagram.code_template.get_properties(),
                    self.notify_diagram)

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
        self.__generate_fields(self.comment.get_properties(), self.notify_comment)

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
        self.__generate_fields(self.block.get_properties(), self.notify_block)

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
        for widget in self.vbox.get_children():
            self.vbox.remove(widget)
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
    def notify_block(self, widget=None, data=None):
        """
        This method notify modifications in propertybox
        """
        self.__recursive_search(self.vbox)
        self.block.set_properties(self.properties)

# ----------------------------------------------------------------------
    def notify_comment(self, widget=None, data=None):
        """
        This method notify modifications in propertybox
        """
        self.__recursive_search(self.vbox)
        self.comment.set_properties(self.properties)

# ----------------------------------------------------------------------
    def notify_diagram(self, widget=None, data=None):
        """
        This method notify modifications in propertybox
        """
        self.__recursive_search(self.vbox)
        self.diagram.code_template.set_properties(self.properties)

# ----------------------------------------------------------------------
