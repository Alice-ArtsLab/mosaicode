#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the CodeTemplateCodeEditor class.
"""
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource
from mosaicode.GUI.fields.codefield import CodeField
from mosaicode.GUI.fields.colorfield import ColorField
from mosaicode.GUI.fields.combofield import ComboField
from mosaicode.GUI.fields.commentfield import CommentField
from mosaicode.GUI.fields.openfilefield import OpenFileField
from mosaicode.GUI.fields.stringfield import StringField
from mosaicode.GUI.messagedialog import MessageDialog
from mosaicode.GUI.confirmdialog import ConfirmDialog
from mosaicode.GUI.fieldtypes import *
from mosaicode.GUI.buttonbar import ButtonBar
from mosaicode.GUI.treeview import TreeView
from mosaicode.system import *
import gettext

_ = gettext.gettext


class CodeTemplateCodeEditor(Gtk.ScrolledWindow):
    """
    This class contains methods related the CodeTemplateCodeEditor class
    """

    # ----------------------------------------------------------------------
    def __init__(self, code_template):
        Gtk.ScrolledWindow.__init__(self)

        self.code_template = code_template

        vbox = Gtk.VBox()
        self.add(vbox)

        # Generated files
        content_pane = Gtk.HBox()
        vbox.pack_start(content_pane, True, True, 1)

        self.tree_view = TreeView(_("Generated files"), self.__on_row_activated)
        content_pane.pack_start(self.tree_view, True, True, 1)

        button_bar = ButtonBar()
        button_bar.add_button({
                "icone":Gtk.STOCK_NEW,
                "action": self.__new,
                "data":None
                })
        button_bar.add_button({
                "icone":Gtk.STOCK_DELETE,
                "action": self.__delete,
                "data":None
                })
        vbox.pack_start(button_bar, False, False, 1)

        self.codes = self.code_template.codes
        self.__populate_list()

        self.side_panel = Gtk.VBox()
        content_pane.pack_start(self.side_panel, True, True, 1)

        self.show_all()

    # ----------------------------------------------------------------------
    def __on_edit(self, widget=None, data=None):
        """
        This method save the code_template.
            Parameters:
                * **code_template** (:class:`<>`)
        """
        count = 0
        for code_widget in self.code_widgets:
            self.code_template.codes[count] = self.code_widgets[count].get_value()
            count = count + 1

    # ----------------------------------------------------------------------
    def __create_menu(self, widget, values, name):
        menu_item = Gtk.MenuItem(name)
        widget.append(menu_item)
        menu = Gtk.Menu()
        menu_item.set_submenu(menu)
        for value in values:
            item = Gtk.MenuItem(value)
            item.connect("activate", self.__on_select, None)
            menu.append(item)

    # ----------------------------------------------------------------------
    def __populate_menu(self, entry, widget):

        # code_template Common Properties
        values = ["$author$",
                   "$license$",
                   "$dir_name$",
                   "$command$",
                   "$name$",
                   "$description$"]
        self.__create_menu(widget, values, "Common Properties")

        # Code Parts
        values = []
        for code_part in self.code_template.code_parts:
            values.append("$single_code[" + code_part + "]$")
            values.append("$code[" + code_part + "]$")
            values.append("$code[" + code_part + ",connection]$")
        values.append("$connections$")
        values.sort()
        self.__create_menu(widget, values, "Code Parts")


        # code_template Properties
        values = []
        for prop in self.code_template.get_properties():
            values.append("$prop[" + prop["name"] + "]$")
        values.sort()
        self.__create_menu(widget, values, "Code Template Properties")

        widget.show_all()

    # ----------------------------------------------------------------------
    def __get_current_code_area(self):
        current_tab = None
        for widget in self.side_panel.get_children():
            if widget.get_name() == "code":
                current_tab = widget
                break
        return current_tab

    # ----------------------------------------------------------------------
    def __on_select(self, widget=None, data=None):
        code_area = self.__get_current_code_area()
        if code_area is None:
            return
        value = widget.get_label()
        code_area.insert_at_cursor(value)

    # ----------------------------------------------------------------------
    def __populate_list(self):
        labels = []
        for key in self.codes:
            labels.append(key)
        self.tree_view.populate(labels)

    # ----------------------------------------------------------------------
    def __on_row_activated(self, tree_view, path, column, data):
        treeselection = tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        if iterac is None:
            return None
        name = model.get_value(model.get_iter(path), 0)

        configuration = {}
        configuration["name"] = name
        configuration["code"] = self.codes[name]
        self.__create_side_panel(configuration)

    # ----------------------------------------------------------------------
    def __new(self, widget=None, data=None):
        self.__create_side_panel(None)

    # ----------------------------------------------------------------------
    def __delete(self, widget=None, data=None):
        treeselection = None
        treeselection = self.tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        if iterac is None:
            return None
        path = model.get_path(iterac)
        name = model.get_value(model.get_iter(path), 0)

        result = ConfirmDialog(_("Are you sure?"), self).run()
        if result != Gtk.ResponseType.OK:
            return
        path = model.get_path(iterac)

        del self.codes[name]
        self.__populate_list()
        self.__clean_side_panel()

    # ----------------------------------------------------------------------
    def __clean_side_panel(self):
        for widget in self.side_panel.get_children():
            self.side_panel.remove(widget)

    # ----------------------------------------------------------------------
    def __create_side_panel(self, configuration):
        self.__clean_side_panel()


        data = {"label": _("File Name"), "name":"name"}
        field = StringField(data, None)
        self.side_panel.pack_start(field, False, False, 1)
        try:
            field.set_value(configuration["name"])
        except:
            pass

        data = {"label": _("Code"), "name":"code"}
        field = CodeField(data, None)
        self.side_panel.pack_start(field, True, True, 1)
        try:
            field.set_value(configuration["code"])
        except:
            pass

        field.field.connect("populate-popup", self.__populate_menu)

        button = Gtk.Button.new_with_label("Save")
        button.connect("clicked", self.__add_code_part)
        self.side_panel.pack_start(button, False, False, 1)
        self.side_panel.show_all()

    # ----------------------------------------------------------------------
    def __add_code_part(self, widget=None, data=None):
        name = ""
        code = ""
        for widget in self.side_panel.get_children():
            if widget.get_name() == "name":
                name = widget.get_value()
            if widget.get_name() == "code":
                code = widget.get_value()
        if name == "":
            message = "File Name can not be empty"
            MessageDialog("Error", message, self).run()
            return
        if code == "":
            message = "Code can not be empty"
            MessageDialog("Error", message, self).run()
            return
        contains = False
        i = 0
        self.codes[name] = code
        self.__populate_list()
        self.__clean_side_panel()


# ----------------------------------------------------------------------
