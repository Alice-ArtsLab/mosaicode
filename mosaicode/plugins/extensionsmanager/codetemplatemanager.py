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
from mosaicode.GUI.fieldtypes import *
from mosaicode.plugins.extensionsmanager.codetemplateeditor import CodeTemplateEditor
from mosaicode.GUI.confirmdialog import ConfirmDialog
from mosaicode.GUI.buttonbar import ButtonBar
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.plugins.extensionsmanager.manager import Manager
from mosaicode.system import *

import gettext

_ = gettext.gettext


class CodeTemplateManager(Manager):
    """
    This class contains methods related the CodeTemplateManager class
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        Manager.__init__(self, main_window, "Code Template Manager")

        self.element = CodeTemplate()
        self.get_items = System.get_code_templates
        self.editor = CodeTemplateEditor
        self.update()
        self.show_all()
        self.show()

# ----------------------------------------------------------------------
