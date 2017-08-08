#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the BlockPortEditor class.
"""
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource
from mosaicomponents.stringfield import StringField
from mosaicomponents.combofield import ComboField
from mosaicomponents.colorfield import ColorField
from mosaicomponents.commentfield import CommentField
from mosaicomponents.codefield import CodeField
from mosaicomponents.openfilefield import OpenFileField
from mosaicode.GUI.blocknotebook import BlockNotebook
from mosaicode.GUI.fieldtypes import *
from mosaicode.GUI.dialog import Dialog
from mosaicode.GUI.buttonbar import ButtonBar
from mosaicode.system import System as System
import gettext

_ = gettext.gettext


class BlockPortEditor(Gtk.ScrolledWindow):
    """
    This class contains methods related the BlockPortEditor class
    """

    # ----------------------------------------------------------------------
    def __init__(self, block_editor, block):
        Gtk.ScrolledWindow.__init__(self)

        self.block_editor = block_editor
        self.block = block

        self.selected_port = None

        for widget in self.get_children():
            self.remove(widget)
        hbox = Gtk.HBox()
        vbox2 = Gtk.VBox()
        self.add(hbox)

        # INPUT PORTS ----------------------------------------------------------
        sw = Gtk.ScrolledWindow()
        self.input_list_store = Gtk.ListStore(str)
        self.input_tree_view = Gtk.TreeView(self.input_list_store)
        self.input_tree_view.connect("row-activated",
                self.__on_row_activated, "Input")
        sw.add(self.input_tree_view)

        col = Gtk.TreeViewColumn(_("Input Ports"))
        self.input_tree_view.append_column(col)

        cellrenderertext = Gtk.CellRendererText()
        col.pack_end(cellrenderertext, True)
        col.add_attribute(cellrenderertext, "text", 0)

        vbox2.pack_start(sw, True, True, 1)

        # Button bar
        button_bar = ButtonBar()
        button_bar.add_button({"icone":Gtk.STOCK_NEW, "action": self.__new, "data":"Input"})
        button_bar.add_button({"icone":Gtk.STOCK_DELETE, "action": self.__delete, "data":"Input"})
        button_bar.add_button({"icone":Gtk.STOCK_GO_UP, "action": self.__up, "data":"Input"})
        button_bar.add_button({"icone":Gtk.STOCK_GO_DOWN, "action": self.__down, "data":"Input"})
        vbox2.pack_start(button_bar, False, False, 1)

        # OUTPUT PORTS ---------------------------------------------------------
        sw = Gtk.ScrolledWindow()
        self.output_list_store = Gtk.ListStore(str)
        self.output_tree_view = Gtk.TreeView(self.output_list_store)
        self.output_tree_view.connect("row-activated",
                self.__on_row_activated, "Output")
        sw.add(self.output_tree_view)

        col = Gtk.TreeViewColumn(_("Output Ports"))
        self.output_tree_view.append_column(col)

        cellrenderertext = Gtk.CellRendererText()
        col.pack_end(cellrenderertext, True)
        col.add_attribute(cellrenderertext, "text", 0)

        vbox2.pack_start(sw, True, True, 1)

        # Button bar
        button_bar = ButtonBar()
        button_bar.add_button({"icone":Gtk.STOCK_NEW, "action": self.__new, "data":"Output"})
        button_bar.add_button({"icone":Gtk.STOCK_DELETE, "action": self.__delete, "data":"Output"})
        button_bar.add_button({"icone":Gtk.STOCK_GO_UP, "action": self.__up, "data":"Output"})
        button_bar.add_button({"icone":Gtk.STOCK_GO_DOWN, "action": self.__down, "data":"Output"})
        vbox2.pack_start(button_bar, False, False, 1)
        # ---------------------------------------------------------

        hbox.pack_start(vbox2, True, True, 2)
        vbox = Gtk.VBox()
        hbox.pack_start(vbox, True, True, 2)
        self.side_panel = Gtk.VBox()
        vbox.pack_start(self.side_panel, True, True, 1)
        self.__populate_lists()

        self.set_shadow_type(Gtk.ShadowType.IN)
        self.show_all()

    # ----------------------------------------------------------------------
    def __populate_lists(self):
        self.input_list_store.clear()
        for port in self.block.in_ports:
            self.input_list_store.append([port.get("label")])

        self.output_list_store.clear()
        for port in self.block.out_ports:
            self.output_list_store.append([port.get("label")])

    # ----------------------------------------------------------------------
    def __new(self, widget=None, data=None):
        self.selected_port = data
        configuration = None
        self.__create_side_panel(configuration)

    # ----------------------------------------------------------------------
    def __delete(self, widget=None, data=None):
        treeselection = None
        if data == "Input":
            treeselection = self.input_tree_view.get_selection()
        else:
            treeselection = self.output_tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        if iterac is None:
            return None
        dialog = Dialog().confirm_dialog(_("Are you sure?"),
                self.block_editor)
        result = dialog.run()
        dialog.destroy()
        if result != Gtk.ResponseType.OK:
            return
        path = model.get_path(iterac)

        if data == "Input":
            del self.block.in_ports[int(str(path))]
        else:
            del self.block.out_ports[int(str(path))]
        self.__populate_lists()
        self.__clean_side_panel()

    # ----------------------------------------------------------------------
    def __up(self, widget=None, data=None):
        treeselection = None
        if data == "Input":
            treeselection = self.input_tree_view.get_selection()
        else:
            treeselection = self.output_tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        if iterac is None:
            return None
        path = model.get_path(iterac)
        if int(str(path)) == 0:
            return

        if data == "Input":
            self.block.in_ports[int(str(path))], \
                self.block.in_ports[int(str(path)) - 1] = \
                self.block.in_ports[int(str(path)) - 1], \
                self.block.in_ports[int(str(path))]
        else:
            self.block.out_ports[int(str(path))], \
                self.block.out_ports[int(str(path)) - 1] = \
                self.block.out_ports[int(str(path)) - 1], \
                self.block.out_ports[int(str(path))]
        self.__populate_lists()

    # ----------------------------------------------------------------------
    def __down(self, widget=None, data=None):
        treeselection = None
        if data == "Input":
            treeselection = self.input_tree_view.get_selection()
        else:
            treeselection = self.output_tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        if iterac is None:
            return None
        path = model.get_path(iterac)

        if data == "Input":
            if int(str(path)) == len(self.block.in_ports) - 1:
                return
            self.block.in_ports[int(str(path))], \
                self.block.in_ports[int(str(path)) + 1] = \
                self.block.in_ports[int(str(path)) + 1], \
                self.block.in_ports[int(str(path))]
        else:
            if int(str(path)) == len(self.block.out_ports) - 1:
                return
            self.block.out_ports[int(str(path))], \
                self.block.out_ports[int(str(path)) + 1] = \
                self.block.out_ports[int(str(path)) + 1], \
                self.block.out_ports[int(str(path))]
        self.__populate_lists()

    # ----------------------------------------------------------------------
    def __clean_side_panel(self):
        for widget in self.side_panel.get_children():
            self.side_panel.remove(widget)

    # ----------------------------------------------------------------------
    def __create_side_panel(self, configuration):
        self.__clean_side_panel()

        connectors = []
        for key in System.ports:
            if System.ports[key].language == self.block.language:
                connectors.append(key)

        data = {"label": _("Type"), "name":"type", "values": connectors}
        field = ComboField(data, None)
        self.side_panel.pack_start(field, False, False, 1)
        if configuration is not None: field.set_value(configuration["type"])

        data = {"label": _("Label"), "name":"label"}
        field = StringField(data, None)
        self.side_panel.pack_start(field, False, False, 1)
        if configuration is not None: field.set_value(configuration["label"])

        data = {"label": _("Name"), "name":"name"}
        field = StringField(data, None)
        self.side_panel.pack_start(field, False, False, 1)
        if configuration is not None: field.set_value(configuration["name"])

        button = Gtk.Button.new_with_label("Save")
        button.connect("clicked", self.__on_save, None)
        self.side_panel.pack_start(button, False, False, 1)
        self.side_panel.show_all()

    # ----------------------------------------------------------------------
    def __on_row_activated(self, tree_view, path, column, data):
        self.selected_port = data
        configuration = None
        if data == "Input":
            configuration = self.block.in_ports[int(str(path))]
        else:
            configuration = self.block.out_ports[int(str(path))]
        self.__create_side_panel(configuration)

    # ----------------------------------------------------------------------
    def __on_save(self, widget=None, data=None):
        new_port = {}
        for widget in self.side_panel.get_children():
            try:
                new_port[widget.get_name()] = widget.get_value()
            except:
                pass
        if "label" not in new_port or "name" not in new_port or \
                "type" not in new_port:
            return
        if new_port["type"] == "":
            message = "Type can not be empty"
            Dialog().message_dialog("Error", message, self.block_editor)
            return
        if new_port["label"] == "":
            message = "Label can not be empty"
            Dialog().message_dialog("Error", message, self.block_editor)
            return
        if new_port["name"] == "":
            message = "Name can not be empty"
            Dialog().message_dialog("Error", message, self.block_editor)
            return
        contains = False
        i = 0
        collection = None
        if self.selected_port == "Input":
            collection = self.block.in_ports
        else:
            collection = self.block.out_ports
        for port in collection:
            if port["label"] == new_port["label"]:
                collection[i] = new_port
                contains = True
            i += 1
        if not contains:
            collection.append(new_port)
        self.__populate_lists()
        self.__clean_side_panel()

# ----------------------------------------------------------------------
