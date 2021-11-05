#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the BlockManager class.
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
from mosaicode.plugins.extensionsmanager.blockeditor import BlockEditor
from mosaicode.GUI.confirmdialog import ConfirmDialog
from mosaicode.GUI.buttonbar import ButtonBar
from mosaicode.model.blockmodel import BlockModel
from mosaicode.system import System
from mosaicode.plugins.extensionsmanager.manager import Manager
import gettext

_ = gettext.gettext


class BlockManager(Manager):
    """
    This class contains methods related the BlockManager class
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        Manager.__init__(self, main_window, "Block Manager")

        self.element = BlockModel()
        self.get_items = System.get_blocks
        self.editor = BlockEditor
        self.update()
        self.show_all()
        self.show()
# ----------------------------------------------------------------------
