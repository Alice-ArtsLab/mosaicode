#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the BlockEditor class.
"""
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource
from mosaicode.GUI.blocknotebook import BlockNotebook
from mosaicomponents.codefield import CodeField
from mosaicomponents.colorfield import ColorField
from mosaicomponents.combofield import ComboField
from mosaicomponents.commentfield import CommentField
from mosaicomponents.openfilefield import OpenFileField
from mosaicomponents.stringfield import StringField
from mosaicode.GUI.fieldtypes import *
from mosaicode.plugins.extensionsmanager.GUI.blockporteditor import BlockPortEditor
from mosaicode.plugins.extensionsmanager.GUI.blockcommoneditor import BlockCommonEditor
from mosaicode.plugins.extensionsmanager.GUI.blockpropertyeditor import BlockPropertyEditor
from mosaicode.plugins.extensionsmanager.GUI.blockcodeeditor import BlockCodeEditor
from mosaicode.system import *
import gettext

_ = gettext.gettext


class BlockEditor(Gtk.Dialog):
    """
    This class contains methods related the BlockEditor class
    """

    # ----------------------------------------------------------------------
    def __init__(self, block_manager, block):
        Gtk.Dialog.__init__(
                        self,
                        title=_("Block Editor"),
                        transient_for=block_manager,
                        destroy_with_parent=True)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_buttons(Gtk.STOCK_SAVE, Gtk.ResponseType.OK)

        self.block_manager = block_manager
        self.block = block
        self.set_default_size(800, 600)
        box = self.get_content_area()

        self.tabs = Gtk.Notebook()
        self.tabs.set_scrollable(True)
        box.pack_start(self.tabs, True, True, 0)

        self.tabs.append_page(BlockCommonEditor(self, self.block),
                    Gtk.Label.new(_("Common Properties")))
        self.tabs.append_page(BlockPropertyEditor(self, self.block),
                    Gtk.Label.new(_("Properties")))
        self.tabs.append_page(BlockPortEditor(self, self.block),
                    Gtk.Label.new(_("Ports")))
        self.tabs.append_page(BlockCodeEditor(self, self.block),
                    Gtk.Label.new(_("Code")))
        self.show_all()

    def run(self):
        result = super(Gtk.Dialog, self).run()
        if result == Gtk.ResponseType.OK:
            self.block_manager.main_control.add_new_block(self.block)
            self.block_manager.update()
        self.close()
        self.destroy()

# ----------------------------------------------------------------------
