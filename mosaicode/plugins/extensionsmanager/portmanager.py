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
from mosaicode.plugins.extensionsmanager.manager import Manager
import gettext

_ = gettext.gettext


class PortManager(Manager):
    """
    This class contains methods related the PortManager class
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        Manager.__init__(self, main_window, "Code Template Manager")

        self.element = Port()
        self.get_items = System.get_ports
        self.editor = PortEditor
        self.update()
        self.show_all()
        self.show()

# ----------------------------------------------------------------------
