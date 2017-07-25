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
from mosaicode.system import System as System
import gettext

_ = gettext.gettext


class CodeTemplateEditor(Gtk.Dialog):
    """
    This class contains methods related the CodeTemplateEditor class
    """

    # ----------------------------------------------------------------------
    def __init__(self, code_template_manager, code_template_name):
        self.code_template_manager = code_template_manager
        Gtk.Dialog.__init__(self, _("Code Template Editor"),
                            self.code_template_manager,
                            0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        self.main_control = self
        self.set_default_size(600, 300)

        vbox = Gtk.VBox()
        box = self.get_content_area()
        box.pack_start(vbox, True, True, 0)

        self.name = StringField({"label": _("Name")}, None)
        self.type = StringField({"label": _("Type")}, None)
        self.description = StringField({"label": _("Description")}, None)
        self.language = StringField({"label": _("Language")}, None)
        self.command = CodeField({"label": _("")}, None)
        self.extension = StringField({"label": _("Extension")}, None)
        self.code = CodeField({"label": _("")}, None)

        if code_template_name is not None:
            System()
            self.name.set_value(System.code_templates[code_template_name].name)
            self.type.set_value(System.code_templates[code_template_name].type)
            self.description.set_value(System.code_templates[code_template_name].description)
            self.language.set_value(System.code_templates[code_template_name].language)
            self.command.set_value(System.code_templates[code_template_name].command)
            self.extension.set_value(System.code_templates[code_template_name].extension)
            self.code.set_value(System.code_templates[code_template_name].code)

        vbox.pack_start(self.name, False, False, 1)
        vbox.pack_start(self.type, False, False, 1)
        vbox.pack_start(self.description, False, False, 1)
        vbox.pack_start(self.language, False, False, 1)
        vbox.pack_start(self.extension, False, False, 1)

        self.codes = Gtk.Notebook()
        self.codes.set_scrollable(True)
        vbox.pack_start(self.codes, True, True, 1)

        self.codes.append_page(self.code, Gtk.Label(_("Code")))
        self.codes.append_page(self.command, Gtk.Label(_("Command")))


        self.show_all()
        result = self.run()
        if result == Gtk.ResponseType.OK:
            self.__save()
        self.close()
        self.destroy()

    # ----------------------------------------------------------------------
    def __save(self):
        code_template = CodeTemplate()
        code_template.name = self.name.get_value()
        code_template.type = self.type.get_value()
        code_template.description = self.description.get_value()
        code_template.language = self.language.get_value()
        code_template.command = self.command.get_value()
        code_template.extension = self.extension.get_value()
        code_template.code = self.code.get_value()
        self.code_template_manager.add_code_template(code_template)

# ----------------------------------------------------------------------
