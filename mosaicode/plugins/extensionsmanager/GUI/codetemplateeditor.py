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
from mosaicomponents.stringfield import StringField
from mosaicomponents.combofield import ComboField
from mosaicomponents.colorfield import ColorField
from mosaicomponents.commentfield import CommentField
from mosaicomponents.codefield import CodeField
from mosaicomponents.openfilefield import OpenFileField
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.system import *
import gettext

_ = gettext.gettext


class CodeTemplateEditor(Gtk.Dialog):
    """
    This class contains methods related the CodeTemplateEditor class
    """

    # ----------------------------------------------------------------------
    def __init__(self, code_template_manager, code_template_name):
        Gtk.Dialog.__init__(
                        self,
                        title=_("Code Template Editor"),
                        transient_for=code_template_manager)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_buttons(Gtk.STOCK_SAVE, Gtk.ResponseType.OK)

        self.code_template_manager = code_template_manager
        system_code_template = System.get_code_templates()
        if code_template_name is not None \
                and code_template_name in system_code_template:
            self.code_template = system_code_template[code_template_name]
        else:
            self.code_template = CodeTemplate()

        self.main_control = self
        self.set_default_size(800, 300)

        self.tabs = Gtk.Notebook()
        self.tabs.set_scrollable(True)
        box = self.get_content_area()
        box.pack_start(self.tabs, True, True, 0)

        common_tab = Gtk.VBox()
        code_tab = Gtk.VBox()
        command_tab = Gtk.VBox()

        self.tabs.append_page(common_tab, Gtk.Label.new(_("Common")))
        self.tabs.append_page(code_tab, Gtk.Label.new(_("Code")))
        self.tabs.append_page(command_tab, Gtk.Label.new(_("Command")))

        # First Tab: Common properties
        self.name = StringField({"label": _("Name")}, self.__edit)
        self.language = StringField({"label": _("Language")}, self.__edit)
        self.extension = StringField({"label": _("Extension")}, self.__edit)
        self.type = StringField({"label": _("Type")}, None)
        self.description = StringField({"label": _("Description")}, None)
        self.code_parts = StringField({"label": _("Code Parts")}, None)

        common_tab.pack_start(self.language, False, False, 1)
        common_tab.pack_start(self.name, False, False, 1)
        common_tab.pack_start(self.extension, False, False, 1)
        common_tab.pack_start(self.type, False, False, 1)
        common_tab.pack_start(self.description, False, False, 1)
        common_tab.pack_start(self.code_parts, False, False, 1)

        # Second Tab: Code properties

        # Button bar
        button_bar = Gtk.HBox()
        code_tab.pack_start(button_bar, False, False, 1)
        self.__populate_combos(button_bar)

        self.code = CodeField({"label": _("")}, None)
        code_tab.pack_start(self.code, True, True, 1)

        # Third Tab: Command properties
        self.command = CodeField({"label": _("")}, None)
        command_tab.pack_start(self.command, True, True, 1)

        if code_template_name is not None:
            System()
            self.name.set_value(self.code_template.name)
            self.type.set_value(self.code_template.type)
            self.description.set_value(self.code_template.description)
            self.language.set_value(self.code_template.language)
            self.command.set_value(self.code_template.command)
            #self.extension.set_value(self.code_template.extension)
            #self.code.set_value(self.code_template.code)
            code_parts_string = ', '.join(self.code_template.code_parts)
            self.code_parts.set_value(code_parts_string)

        self.show_all()
        result = self.show()
        if result == Gtk.ResponseType.OK:
            self.__save()
        self.close()
        self.destroy()

    # ----------------------------------------------------------------------
    def __edit(self, data=None):
        language = self.language.get_value()
        name = self.name.get_value()
        extension = self.extension.get_value()
        self.type.set_value("mosaicode_Extensions_" + language + \
                "_" + name + ".extensions" + extension)

    # ----------------------------------------------------------------------
    def __save(self):
        code_template = CodeTemplate()
        code_template.name = self.name.get_value()
        code_template.language = self.language.get_value()
        code_template.type = self.type.get_value()
        code_template.description = self.description.get_value()
        code_template.command = self.command.get_value()
        code_template.extension = self.extension.get_value()
        code_template.code = self.code.get_value()
        code_template.code_parts = self.code_parts.get_value().split(",")
        self.code_template_manager.add_code_template(code_template)

    # ----------------------------------------------------------------------
    def __populate_combos(self, button_bar):
        # clean the bar
        for widget in button_bar.get_children():
            button_bar.remove(widget)

        # Code Parts
        values = []
        for code_part in self.code_template.code_parts:
            values.append("$single_code[" + code_part + "]$")
            values.append("$code[" + code_part + "]$")
            values.append("$code[" + code_part + ",connection]$")
        values.append("$connections$")
        values.sort()
        data = {"label": _("Code Parts"),
                "name":"code_parts",
                "values": values}
        self.select_code_parts = ComboField(data, self.__on_select)
        button_bar.pack_start(self.select_code_parts, False, False, 0)

        # Refresh Button
        button = Gtk.Button.new_with_label("Refresh")
        button.connect("clicked", self.__refresh, button_bar)
        button_bar.pack_start(button, False, False, 0)

        button_bar.show_all()

    # ----------------------------------------------------------------------
    def __refresh(self, widget, button_bar):
        """
        This method monitors if the button was clicked.

            Parameters:

        """
        self.__populate_combos(button_bar)

    # ----------------------------------------------------------------------
    def __on_select(self, widget=None, data=None):
        value = widget.get_parent().get_value()
        self.code.insert_at_cursor(value)

# ----------------------------------------------------------------------
