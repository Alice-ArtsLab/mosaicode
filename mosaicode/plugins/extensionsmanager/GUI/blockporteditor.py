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
from mosaicode.GUI.messagedialog import MessageDialog
from mosaicode.GUI.confirmdialog import ConfirmDialog
from mosaicode.GUI.buttonbar import ButtonBar
from mosaicode.GUI.treeview import TreeView
from mosaicode.system import *
from mosaicode.model.port import Port
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

        self.tree_view = TreeView(_("Ports"), self.__on_row_activated)
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
        self.__populate_list()

        self.set_shadow_type(Gtk.ShadowType.IN)
        self.show_all()

    # ----------------------------------------------------------------------
    def __populate_list(self):
        labels = []
        for port in self.block.ports:
            labels.append(port.label)
        self.tree_view.populate(labels)

    # ----------------------------------------------------------------------
    def __new(self, widget=None, data=None):
        self.selected_port = data
        configuration = None
        self.__create_side_panel(configuration)

    # ----------------------------------------------------------------------
    def __delete(self, widget=None, data=None):
        treeselection = self.tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        if iterac is None:
            return None
        result = ConfirmDialog(_("Are you sure?"), self.block_editor).run()
        if result != Gtk.ResponseType.OK:
            return
        path = model.get_path(iterac)

        del self.block.ports[int(str(path))]
        self.__populate_list()
        self.__clean_side_panel()

    # ----------------------------------------------------------------------
    def __up(self, widget=None, data=None):
        treeselection = self.tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        if iterac is None:
            return
        path = model.get_path(iterac)
        if int(str(path)) == 0:
            return

        self.block.ports[int(str(path))], \
                self.block.ports[int(str(path)) - 1] = \
                self.block.ports[int(str(path)) - 1], \
                self.block.ports[int(str(path))]
        self.__populate_list()

    # ----------------------------------------------------------------------
    def __down(self, widget=None, data=None):
        treeselection = self.tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        if iterac is None:
            return
        path = model.get_path(iterac)

        if int(str(path)) == len(self.block.ports) - 1:
            return
        self.block.ports[int(str(path))], \
                self.block.ports[int(str(path)) + 1] = \
                self.block.ports[int(str(path)) + 1], \
                self.block.ports[int(str(path))]
        self.__populate_list()

    # ----------------------------------------------------------------------
    def __clean_side_panel(self):
        for widget in self.side_panel.get_children():
            self.side_panel.remove(widget)

    # ----------------------------------------------------------------------
    def __create_side_panel(self, configuration):
        self.__clean_side_panel()

        connectors = []
        ports = System.get_ports()
        for key in ports:
            if ports[key].language == self.block.language:
                connectors.append(key)

        data = {"label": _("Port Type"), "name":"type", "values": connectors}
        field = ComboField(data, None)
        self.side_panel.pack_start(field, False, False, 1)
        if configuration is not None: field.set_value(configuration.type)

        data = {"label": _("Connection Type"), "name":"conn_type", "values": [Port.INPUT, Port.OUTPUT]}
        field = ComboField(data, None)
        self.side_panel.pack_start(field, False, False, 1)
        if configuration is not None: field.set_value(configuration.conn_type)

        data = {"label": _("Label"), "name":"label"}
        field = StringField(data, None)
        self.side_panel.pack_start(field, False, False, 1)
        if configuration is not None: field.set_value(configuration.label)

        data = {"label": _("Name"), "name":"name"}
        field = StringField(data, None)
        self.side_panel.pack_start(field, False, False, 1)
        if configuration is not None: field.set_value(configuration.name)

        button = Gtk.Button.new_with_label("Save")
        button.connect("clicked", self.__on_save, None)
        self.side_panel.pack_start(button, False, False, 1)
        self.side_panel.show_all()

    # ----------------------------------------------------------------------
    def __on_row_activated(self, tree_view, path, column, data):
        self.selected_port = data
        configuration = self.block.ports[int(str(path))]
        self.__create_side_panel(configuration)

    # ----------------------------------------------------------------------
    def __on_save(self, widget=None, data=None):
        new_port = Port()
        for widget in self.side_panel.get_children():
            try:
                new_port.__dict__[widget.get_name()] = widget.get_value()
            except:
                pass

        if new_port.type == "":
            message = "Type can not be empty"
            MessageDialog("Error", message, self.block_editor).run()
            return
        if new_port.label == "":
            message = "Label can not be empty"
            MessageDialog("Error", message, self.block_editor).run()
            return
        if new_port.name == "":
            message = "Name can not be empty"
            MessageDialog("Error", message, self.block_editor).run()
            return
        contains = False
        i = 0
        for port in self.block.ports:
            if port.label == new_port.label:
                self.block.ports[i] = new_port
                contains = True
            i += 1
        if not contains:
            self.block.ports.append(new_port)
        self.__populate_list()
        self.__clean_side_panel()

# ----------------------------------------------------------------------
