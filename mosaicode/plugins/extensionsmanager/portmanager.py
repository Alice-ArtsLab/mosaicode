#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the PortManager class.
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
from mosaicode.plugins.extensionsmanager.porteditor import PortEditor
from mosaicode.GUI.confirmdialog import ConfirmDialog
from mosaicode.GUI.buttonbar import ButtonBar
from mosaicode.system import *
import gettext

_ = gettext.gettext


class PortManager(Gtk.Dialog):
    """
    This class contains methods related the PortManager class
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        Gtk.Dialog.__init__(
                self,
                title=_("Port Manager"),
                transient_for=main_window)

        self.main_window = main_window
        self.set_default_size(400, 300)
        box = self.get_content_area()
        vbox = Gtk.VBox()
        box.pack_start(vbox, True, True, 0)

        # Port List
        sw = Gtk.ScrolledWindow()
        self.tree_store = Gtk.TreeStore(str)
        self.tree_view = Gtk.TreeView.new_with_model(self.tree_store)

        col = Gtk.TreeViewColumn(_("Available Ports"))
        self.tree_view.append_column(col)
        self.tree_view.connect("row-activated", self.__on_row_activated)
        cellrenderertext = Gtk.CellRendererText()
        col.pack_end(cellrenderertext, True)
        col.add_attribute(cellrenderertext, "text", 0)
        sw.add(self.tree_view)
        vbox.pack_start(sw, True, True, 0)

        # Button bar
        button_bar = ButtonBar()
        button_bar.add_button({
                "icone":Gtk.STOCK_NEW,
                "action": self.__new,
                "data":None
                })
        button_bar.add_button({
                "icone":Gtk.STOCK_EDIT,
                "action": self.__edit,
                "data":None
                })
        button_bar.add_button({
                "icone":Gtk.STOCK_DELETE,
                "action": self.__delete,
                "data":None
                })
        vbox.pack_start(button_bar, False, False, 0)

        self.__update()
        self.show_all()
        self.show()

    # ----------------------------------------------------------------------
    def __on_row_activated(self, tree_view, path, column):
        self.__edit()

    # ----------------------------------------------------------------------
    def __get_selected(self):
        treeselection = self.tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        if iterac is None:
            return None
        path = model.get_path(iterac)
        name = model.get_value(model.get_iter(path), 0)
        return name

    # ----------------------------------------------------------------------
    def __new(self, widget=None, data=None):
        self.__run_editor(Port())

    # ----------------------------------------------------------------------
    def __run_editor(self, element):
        editor = PortEditor(self, element)
        result = editor.run()
        if result == Gtk.ResponseType.OK:
            port = editor.get_port()
            self.main_window.main_control.add_extension(element)
            self.__update()
        editor.close()
        editor.destroy()

    # ----------------------------------------------------------------------
    def __edit(self, widget=None, data=None):
        name = self.__get_selected()
        if name is None:
            return
        port = System.get_ports()[name]
        self.__run_editor(port)

    # ----------------------------------------------------------------------
    def __delete(self, widget=None, data=None):
        name = self.__get_selected()
        if name is None:
            return
        result = ConfirmDialog(_("Are you sure?"), self).run()
        if result == Gtk.ResponseType.OK:
            self.main_window.main_control.delete_extension(name, Port())
            self.__update()

    # ----------------------------------------------------------------------
    def __update(self):
        System()
        port_list = []
        ports = System.get_ports()
        for x in ports:
            port_list.append([x])
        port_list.sort()
        self.tree_store.clear()
        for x in port_list:
            self.tree_store.append(None, x)

# ----------------------------------------------------------------------
