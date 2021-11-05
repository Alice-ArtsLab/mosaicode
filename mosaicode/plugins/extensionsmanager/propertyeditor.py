#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the PropertyEditor class.
"""
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource
from mosaicode.GUI.fields.stringfield import StringField
from mosaicode.GUI.fields.combofield import ComboField
from mosaicode.GUI.fields.colorfield import ColorField
from mosaicode.GUI.fields.commentfield import CommentField
from mosaicode.GUI.fields.codefield import CodeField
from mosaicode.GUI.fields.openfilefield import OpenFileField
from mosaicode.GUI.fieldtypes import *
from mosaicode.GUI.messagedialog import MessageDialog
from mosaicode.GUI.confirmdialog import ConfirmDialog
from mosaicode.GUI.buttonbar import ButtonBar
from mosaicode.GUI.treeview import TreeView
from mosaicode.system import *
import gettext

_ = gettext.gettext


class PropertyEditor(Gtk.ScrolledWindow):
    """
    This class contains methods related the PropertyEditor class
    """

    # ----------------------------------------------------------------------
    def __init__(self, element):

        Gtk.ScrolledWindow.__init__(self)

        self.element = element

        for widget in self.get_children():
            self.remove(widget)

        hbox = Gtk.HBox()
        vbox2 = Gtk.VBox()
        self.add(hbox)

        self.tree_view = TreeView(_("Properties"), self.__on_props_row_activated)
        self.__populate_property()
        vbox2.pack_start(self.tree_view, True, True, 1)

        # Button bar
        button_bar = ButtonBar()
        button_bar.add_button({"icone":Gtk.STOCK_NEW, "action": self.__new, "data":None})
        button_bar.add_button({"icone":Gtk.STOCK_DELETE, "action": self.__delete, "data":None})
        button_bar.add_button({"icone":Gtk.STOCK_GO_UP, "action": self.__up, "data":None})
        button_bar.add_button({"icone":Gtk.STOCK_GO_DOWN, "action": self.__down, "data":None})
        vbox2.pack_start(button_bar, False, False, 1)

        hbox.pack_start(vbox2, True, True, 2)
        vbox = Gtk.VBox()
        hbox.pack_start(vbox, True, True, 2)
        self.side_panel = Gtk.VBox()
        vbox.pack_start(self.side_panel, True, True, 1)

        self.set_shadow_type(Gtk.ShadowType.IN)
        self.show_all()

    # ----------------------------------------------------------------------
    def __populate_property(self):
        label = []
        for prop in self.element.get_properties():
            label.append(prop.get("label"))
        self.tree_view.populate(label)

    # ----------------------------------------------------------------------
    def __new(self, widget=None, data=None):
        for widget in self.side_panel.get_children():
            self.side_panel.remove(widget)
        fieldtypes = []
        for key in component_list:
            fieldtypes.append(key)
        data = {"label": _("Field Type"), "values": fieldtypes}
        self.field_type = ComboField(data, self.__select_property_field_type)
        self.side_panel.pack_start(self.field_type, False, False, 1)

    # ----------------------------------------------------------------------
    def __delete(self, widget=None, data=None):
        treeselection = self.tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        if iterac is None:
            return None
        result = ConfirmDialog(_("Are you sure?"), self.get_toplevel()).run()
        if result != Gtk.ResponseType.OK:
            return
        path = model.get_path(iterac)
        del self.element.get_properties()[int(str(path))]
        self.__populate_property()
        self.__clean_side_panel()

    # ----------------------------------------------------------------------
    def __up(self, widget=None, data=None):
        treeselection = self.tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        if iterac is None:
            return None
        path = model.get_path(iterac)
        if int(str(path)) == 0:
            return
        self.element.get_properties()[int(str(path))], \
            self.element.get_properties()[int(str(path)) - 1] = \
            self.element.get_properties()[int(str(path)) - 1], \
            self.element.get_properties()[int(str(path))]
        self.__populate_property()

    # ----------------------------------------------------------------------
    def __down(self, widget=None, data=None):
        treeselection = self.tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        if iterac is None:
            return None
        path = model.get_path(iterac)
        if int(str(path)) == len(self.element.get_properties()) - 1:
            return
        self.element.get_properties()[int(str(path))], \
            self.element.get_properties()[int(str(path)) + 1] = \
            self.element.get_properties()[int(str(path)) + 1], \
            self.element.get_properties()[int(str(path))]
        self.__populate_property()

    # ----------------------------------------------------------------------
    def __clean_side_panel(self):
        for widget in self.side_panel.get_children():
            self.side_panel.remove(widget)

    # ----------------------------------------------------------------------
    def __create_side_panel(self, configuration):
        self.__clean_side_panel()
        for key in configuration:
            data = {"label": _(key),
                    "name":key,
                    "value":str(configuration[key])}
            field = StringField(data, None)
            if key == "type":
                field.field.set_property("editable", False)
            self.side_panel.pack_start(field, False, False, 1)
        button = Gtk.Button.new_with_label("Save")
        button.connect("clicked", self.__on_props_edit_ok, None)
        self.side_panel.pack_start(button, False, False, 1)
        self.side_panel.show_all()

    # ----------------------------------------------------------------------
    def __select_property_field_type(self, widget=None, data=None):
        field_type = self.field_type.get_value()
        configuration = component_list[field_type].get_configuration()
        configuration["type"] = field_type
        self.__create_side_panel(configuration)

    # ----------------------------------------------------------------------
    def __on_props_row_activated(self, tree_view, path, column, data=None):
        configuration = self.element.get_properties()[int(str(path))]
        self.__create_side_panel(configuration)

    # ----------------------------------------------------------------------
    def __on_props_edit_ok(self, widget=None, data=None):
        configuration = {}
        for widget in self.side_panel.get_children():
            try:
                configuration[widget.get_name()] = widget.get_value()
            except:
                pass
        if "label" not in configuration or "name" not in configuration or \
                "value" not in configuration:
            return
        if configuration["label"] == "":
            message = "Label can not be empty"
            MessageDialog("Error", message, self.get_toplevel()).run()
            return
        if configuration["name"] == "":
            message = "Name can not be empty"
            MessageDialog("Error", message, self.get_toplevel()).run()
            return
        contains = False
        i = 0
        for props in self.element.properties:
            if props["label"] == configuration["label"]:
                self.element.properties[i] = configuration
                contains = True
            i += 1
        if not contains:
            self.element.properties.append(configuration)
        self.__populate_property()
        self.__clean_side_panel()

# ----------------------------------------------------------------------
