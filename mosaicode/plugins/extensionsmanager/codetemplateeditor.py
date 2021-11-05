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
from mosaicode.GUI.fields.stringfield import StringField
from mosaicode.GUI.fields.combofield import ComboField
from mosaicode.GUI.fields.colorfield import ColorField
from mosaicode.GUI.fields.commentfield import CommentField
from mosaicode.GUI.fields.codefield import CodeField
from mosaicode.GUI.fields.openfilefield import OpenFileField
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.plugins.extensionsmanager.propertyeditor import PropertyEditor
from mosaicode.plugins.extensionsmanager.codetemplatecodeeditor import CodeTemplateCodeEditor
import gettext

_ = gettext.gettext


class CodeTemplateEditor(Gtk.Dialog):
    """
    This class contains methods related the CodeTemplateEditor class
    """

    # ----------------------------------------------------------------------
    def __init__(self, code_template_manager, code_template):
        Gtk.Dialog.__init__(
                        self,
                        title=_("Code Template Editor"),
                        transient_for=code_template_manager
                        )

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_buttons(Gtk.STOCK_SAVE, Gtk.ResponseType.OK)

        self.set_default_size(800, 300)
        self.code_template = code_template
        self.tabs = Gtk.Notebook()
        self.tabs.set_scrollable(True)
        box = self.get_content_area()
        box.pack_start(self.tabs, True, True, 0)

        common_tab = Gtk.VBox()
        property_tab =  PropertyEditor(self.code_template)
        code_tab = CodeTemplateCodeEditor(self.code_template)
        command_tab = Gtk.VBox()

        self.tabs.append_page(common_tab, Gtk.Label.new(_("Common")))
        self.tabs.append_page(property_tab, Gtk.Label.new(_("Properties")))
        self.tabs.append_page(code_tab, Gtk.Label.new(_("Codes")))
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


        # Third Tab: Command properties
        self.command = CodeField({"label": _("")}, None)
        command_tab.pack_start(self.command, True, True, 1)

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

    # ----------------------------------------------------------------------
    def __edit(self, data=None):
        language = self.language.get_value()
        name = self.name.get_value()
        extension = self.extension.get_value()
        self.type.set_value("" + language + \
                "." + name + "." + extension)

    # ----------------------------------------------------------------------
    def get_element(self):
        self.code_template.name = self.name.get_value()
        self.code_template.language = self.language.get_value()
        self.code_template.type = self.type.get_value()
        self.code_template.description = self.description.get_value()
        self.code_template.command = self.command.get_value()
        self.code_template.extension = self.extension.get_value()
        self.code_template.code_parts = self.code_parts.get_value().split(",")
        # Removing trailing spaces
        self.code_template.code_parts = [s.strip() for s in self.code_template.code_parts]
        return self.code_template

    # ----------------------------------------------------------------------
    def __on_select(self, widget=None, data=None):
        value = widget.get_parent().get_value()
        self.code.insert_at_cursor(value)

# ----------------------------------------------------------------------
