#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402

import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk
from gi.repository import GtkSource
from harpia.GUI.components.stringfield import StringField
from harpia.GUI.components.combofield import ComboField
from harpia.GUI.components.colorfield import ColorField
from harpia.GUI.components.commentfield import CommentField
from harpia.GUI.components.codefield import CodeField
from harpia.GUI.components.openfilefield import OpenFileField
from harpia.GUI.blocknotebook import BlockNotebook
from harpia.system import System as System
import gettext

_ = gettext.gettext
class PluginManager(Gtk.Dialog):

    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        Gtk.Dialog.__init__(self, _("Plugin Manager"), main_window,
                            0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        self.main_control = self
        self.set_default_size(800, 600)
        System()
        box = self.get_content_area()

        hbox = Gtk.HPaned()
        box.pack_start(hbox, True, True, 0)

        blocks = BlockNotebook(self)
        hbox.add1(blocks)
        tabs = Gtk.Notebook()
        tabs.set_scrollable(True)
        hbox.add2(tabs)

        # ----------------------------------------------------------------------
        common_properties = Gtk.ScrolledWindow()
        common_properties.set_shadow_type(Gtk.ShadowType.IN)
        tabs.append_page(common_properties, Gtk.Label(_("Common Properties")))
        vbox = Gtk.VBox()
        common_properties.add(vbox)
        languages = []
        for key in System.generators:
            if key == "codegenerator":
                continue
            languages.append(key)
        data = {"label": _("Language"), "values": languages}
        self.type = StringField({"label": _("Plugin Type")}, None)
        self.language = ComboField(data, None)
        self.framework = StringField({"label": _("Framework")}, None)
        vbox.pack_start(self.type, False, False, 1)
        vbox.pack_start(self.language, False, False, 1)
        vbox.pack_start(self.framework, False, False, 1)

        # ----------------------------------------------------------------------
        appearance = Gtk.ScrolledWindow()
        appearance.set_shadow_type(Gtk.ShadowType.IN)
        tabs.append_page(appearance, Gtk.Label(_("Appearance")))
        vbox = Gtk.VBox()
        appearance.add(vbox)
        # Default directory
        self.label = StringField({"label": _("Label")}, None)
        vbox.pack_start(self.label, False, False, 1)
        self.group = StringField({"label": _("Group")}, None)
        vbox.pack_start(self.group, False, False, 1)
        self.icon = OpenFileField({"label": _("Icon")}, None)
        vbox.pack_start(self.icon, False, False, 1)
        self.color = ColorField({"label": _("Color")}, None)
        vbox.pack_start(self.color, False, False, 1)
        self.help = CommentField({"label": _("Help")}, None)
        vbox.pack_start(self.help, False, False, 1)

        # ----------------------------------------------------------------------
        connections = Gtk.ScrolledWindow()
        connections.set_shadow_type(Gtk.ShadowType.IN)
        tabs.append_page(connections, Gtk.Label(_("Connections")))
        vbox = Gtk.VBox()
        connections.add(vbox)
        connectors = []
        for key in System.connectors:
            connectors.append(key)
        data = {"label": _("Connectors"), "values": connectors}
        self.connectors = ComboField(data, None)
        vbox.pack_start(self.connectors, False, False, 1)

        # ----------------------------------------------------------------------
        configuration = Gtk.ScrolledWindow()
        configuration.set_shadow_type(Gtk.ShadowType.IN)
        tabs.append_page(configuration, Gtk.Label(_("Configuration")))
        vbox = Gtk.VBox()
        configuration.add(vbox)

        # ----------------------------------------------------------------------
        code = Gtk.ScrolledWindow()
        code.set_shadow_type(Gtk.ShadowType.IN)
        tabs.append_page(code, Gtk.Label(_("Code")))
        vbox = Gtk.VBox()
        code.add(vbox)
        codes = Gtk.Notebook()
        codes.set_scrollable(True)
        vbox.pack_start(codes, True, True, 1)
        self.header = CodeField({"label": _("Header")}, None)
        codes.append_page(self.header, Gtk.Label(_("Header")))
        self.vars = CodeField({"label": _("Vars")}, None)
        codes.append_page(self.vars, Gtk.Label(_("Vars")))
        self.function_call = CodeField({"label": _("Function Call")}, None)
        codes.append_page(self.function_call, Gtk.Label(_("Function Call")))
        self.dealloc = CodeField({"label": _("Dealloc")}, None)
        codes.append_page(self.dealloc, Gtk.Label(_("Dealloc")))
        self.out_dealloc = CodeField({"label": _("Out Dealloc")}, None)
        codes.append_page(self.out_dealloc, Gtk.Label(_("Out Dealloc")))

        self.show_all()
        result = self.run()
        if result == Gtk.ResponseType.OK:
            print "Good Save the Queen"
        self.close()
        self.destroy()

    # ----------------------------------------------------------------------
    def set_block(self, plugin):
        self.add_block(plugin)

    # ----------------------------------------------------------------------
    def add_block(self, plugin):
        self.type.set_value(plugin.get_type())
        self.language.set_value(plugin.get_language())
        self.language.set_value(plugin.language)
        self.framework.set_value(plugin.framework)

        self.label.set_value(plugin.get_label())
        self.group.set_value(plugin.get_group())
        self.icon.set_value(os.environ['HARPIA_DATA_DIR'] + plugin.get_icon())
        self.color.set_value(plugin.get_color())
        self.help.set_value(plugin.get_help())

        self.header.set_value(plugin.generate_header())
        self.vars.set_value(plugin.generate_vars())
        self.function_call.set_value(plugin.generate_function_call())
        self.dealloc.set_value(plugin.generate_dealloc())
        self.out_dealloc.set_value(plugin.generate_out_dealloc())
# ----------------------------------------------------------------------
