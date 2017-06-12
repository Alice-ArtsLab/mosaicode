#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the CodeTemplateManager class.
"""
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource
from mosaicode.GUI.components.stringfield import StringField
from mosaicode.GUI.components.combofield import ComboField
from mosaicode.GUI.components.colorfield import ColorField
from mosaicode.GUI.components.commentfield import CommentField
from mosaicode.GUI.components.codefield import CodeField
from mosaicode.GUI.components.openfilefield import OpenFileField
from mosaicode.GUI.fieldtypes import *
from mosaicode.GUI.codetemplateeditor import CodeTemplateEditor
from mosaicode.GUI.dialog import Dialog
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.system import System as System
import gettext

_ = gettext.gettext


class CodeTemplateManager(Gtk.Dialog):
    """
    This class contains methods related the CodeTemplateManager class
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        Gtk.Dialog.__init__(self, _("Code Template Manager"), main_window, 0, ())

        self.main_window = main_window
        self.set_default_size(400, 300)
        box = self.get_content_area()

        vbox = Gtk.VBox()
        box.pack_start(vbox, True, True, 0)

        # CodeTemplate List
        sw = Gtk.ScrolledWindow()
        self.tree_store = Gtk.TreeStore(str)
        self.tree_view = Gtk.TreeView(self.tree_store)

        col = Gtk.TreeViewColumn(_("Available Code Templates"))
        self.tree_view.append_column(col)
        self.tree_view.connect("row-activated", self.__on_row_activated)
        cellrenderertext = Gtk.CellRendererText()
        col.pack_end(cellrenderertext, True)
        col.add_attribute(cellrenderertext, "text", 0)
        sw.add(self.tree_view)
        vbox.pack_start(sw, True, True, 0)

        # Button bar
        button_bar = Gtk.HBox()
        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_NEW)
        button.connect("clicked", self.__new, None)
        button_bar.pack_start(button, False, False, 0)

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_EDIT)
        button.connect("clicked", self.__edit, None)
        button_bar.pack_start(button, False, False, 0)

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_DELETE)
        button.connect("clicked", self.__delete, None)
        button_bar.pack_start(button, False, False, 0)

        vbox.pack_start(button_bar, False, False, 0)

        self.__update()
        self.show_all()
        self.show()

    # ----------------------------------------------------------------------
    def add_code_template(self, code_template):
        self.main_window.main_control.add_code_template(code_template)
        self.__update()

    # ----------------------------------------------------------------------
    def __on_row_activated(self, tree_view, path, column):
        CodeTemplateEditor(self, self.__get_selected())

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
        CodeTemplateEditor(self, None)

    # ----------------------------------------------------------------------
    def __edit(self, widget=None, data=None):
        name = self.__get_selected()
        if name is None:
            return
        CodeTemplateEditor(self, name)

    # ----------------------------------------------------------------------
    def __delete(self, widget=None, data=None):
        name = self.__get_selected()
        if name is None:
            return
        dialog = Dialog().confirm_dialog(_("Are you sure?"), self)
        result = dialog.run()
        dialog.destroy()
        if result == Gtk.ResponseType.OK:
            self.main_window.main_control.delete_code_template(name)
            self.__update()

    # ----------------------------------------------------------------------
    def __update(self):
        System()
        code_template_list = []
        for x in System.code_templates:
            code_template_list.append([x])
        code_template_list.sort()
        self.tree_store.clear()
        for x in code_template_list:
            self.tree_store.append(None, x)

# ----------------------------------------------------------------------
