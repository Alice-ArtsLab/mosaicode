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
from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin
from harpia.system import System as System
import gettext

_ = gettext.gettext
class PluginManager(Gtk.Dialog):

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        Gtk.Dialog.__init__(self, _("Plugin Manager"), main_window,
                            0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        self.plugin = Plugin()
        self.main_control = self
        self.set_default_size(800, 600)
        System()
        box = self.get_content_area()

        hbox = Gtk.HPaned()
        box.pack_start(hbox, True, True, 0)

        # Plugin List
        blocks = BlockNotebook(self)

        button_bar = Gtk.HBox()
        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_NEW)
        button.connect("clicked", self.__new_plugin, None)
        button_bar.pack_start(button, False, False, 0)

        vbox = Gtk.VBox()
        vbox.pack_start(blocks, True, True, 0)
        vbox.pack_start(button_bar, False, False, 0)

        hbox.add1(vbox)
        self.tabs = Gtk.Notebook()
        self.tabs.set_scrollable(True)
        hbox.add2(self.tabs)

        # ----------------------------------------------------------------------
        # Common properties Section
        # ----------------------------------------------------------------------
        self.common_properties = Gtk.ScrolledWindow()
        self.common_properties.set_shadow_type(Gtk.ShadowType.IN)
        self.tabs.append_page(self.common_properties, Gtk.Label(_("Common Properties")))
        self.__create_common_properties_tab()
        # ----------------------------------------------------------------------
        # Appearance Section
        # ----------------------------------------------------------------------
        self.appearance = Gtk.ScrolledWindow()
        self.appearance.set_shadow_type(Gtk.ShadowType.IN)
        self.tabs.append_page(self.appearance, Gtk.Label(_("Appearance")))
        self.__create_appearance_tab()
        # ----------------------------------------------------------------------
        # Connections Section
        # ----------------------------------------------------------------------
        self.connections = Gtk.ScrolledWindow()
        self.connections.set_shadow_type(Gtk.ShadowType.IN)
        self.tabs.append_page(self.connections, Gtk.Label(_("Connections")))
        self.__create_connection_tab()
        # ----------------------------------------------------------------------
        # Configuration section
        # ----------------------------------------------------------------------
        self.configuration = Gtk.ScrolledWindow()
        self.configuration.set_shadow_type(Gtk.ShadowType.IN)
        self.tabs.append_page(self.configuration, Gtk.Label(_("Configuration")))
        self.__create_configuration_tab()
        # ----------------------------------------------------------------------
        # Code section
        # ----------------------------------------------------------------------
        self.code = Gtk.ScrolledWindow()
        self.code.set_shadow_type(Gtk.ShadowType.IN)
        self.tabs.append_page(self.code, Gtk.Label(_("Code")))
        self.__create_code_tab()

        self.show_all()
        result = self.run()
        if result == Gtk.ResponseType.OK:
            print "Good Save the Queen"
        self.close()

    # ----------------------------------------------------------------------
    def set_block(self, plugin):
        self.add_block(plugin)

    # ----------------------------------------------------------------------
    def add_block(self, plugin):
        self.plugin = plugin
        self.__create_common_properties_tab()
        self.__create_appearance_tab()
        self.__create_connection_tab()
        self.__create_configuration_tab()
        self.__create_code_tab()

    # ----------------------------------------------------------------------
    def __create_common_properties_tab(self):
        for widget in self.common_properties.get_children():
            self.common_properties.remove(widget)
        vbox = Gtk.VBox()
        self.common_properties.add(vbox)
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
        self.type.set_value(self.plugin.get_type())
        self.language.set_value(self.plugin.get_language())
        self.language.set_value(self.plugin.language)
        self.framework.set_value(self.plugin.framework)
        self.common_properties.show_all()

    # ----------------------------------------------------------------------
    def __create_appearance_tab(self):
        for widget in self.appearance.get_children():
            self.appearance.remove(widget)
        vbox = Gtk.VBox()
        self.appearance.add(vbox)
        # Default directory
        self.label = StringField({"label": _("Label")}, None)
        vbox.pack_start(self.label, False, False, 1)
        self.group = StringField({"label": _("Group")}, None)
        vbox.pack_start(self.group, False, False, 1)
        self.icon = OpenFileField({"label": _("Icon")}, None)
        self.icon.set_parent_window(self)
        vbox.pack_start(self.icon, False, False, 1)
        self.color = ColorField({"label": _("Color")}, None)
        self.color.set_parent_window(self)
        vbox.pack_start(self.color, False, False, 1)
        self.help = CommentField({"label": _("Help")}, None)
        vbox.pack_start(self.help, False, False, 1)
        self.label.set_value(self.plugin.get_label())
        self.group.set_value(self.plugin.get_group())
        self.icon.set_value(os.environ['HARPIA_DATA_DIR'] + self.plugin.get_icon())
        print self.plugin.get_color()
        self.color.set_value(self.plugin.get_color())
        self.help.set_value(self.plugin.get_help())
        self.appearance.show_all()

    # ----------------------------------------------------------------------
    def __create_configuration_tab(self):
        for widget in self.configuration.get_children():
            self.configuration.remove(widget)
        hbox = Gtk.HBox()
        vbox2 = Gtk.VBox()
        self.configuration.add(hbox)
        sw = Gtk.ScrolledWindow()
        self.configuration_store = Gtk.ListStore(str)
        self.configuration_tree_view = Gtk.TreeView(self.configuration_store)
        self.configuration_tree_view.connect("row-activated", self.__on_configuration_row_activated)
        sw.add(self.configuration_tree_view)

        col = Gtk.TreeViewColumn(_("Configuration"))
        self.configuration_tree_view.append_column(col)

        cellrenderertext = Gtk.CellRendererText()
        col.pack_end(cellrenderertext, True)
        col.add_attribute(cellrenderertext, "text", 0)

        vbox2.pack_start(sw, True, True, 1)

        # Button bar
        button_bar = Gtk.HBox()

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_NEW)
        button.connect("clicked", self.__new_configuration_panel, None)
        button_bar.pack_start(button, False, False, 0)

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_DELETE)
        button.connect("clicked", self.__new_configuration_panel, None)
        button_bar.pack_start(button, False, False, 0)

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_GO_UP)
        button.connect("clicked", self.__new_configuration_panel, None)
        button_bar.pack_start(button, False, False, 0)

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_GO_DOWN)
        button.connect("clicked", self.__new_configuration_panel, None)
        button_bar.pack_start(button, False, False, 0)

        vbox2.pack_start(button_bar, False, False, 1)

        hbox.pack_start(vbox2, True, True, 2)
        vbox = Gtk.VBox()
        hbox.pack_start(vbox, True, True, 2)
        self.configuration_panel = Gtk.VBox()
        vbox.pack_start(self.configuration_panel, True, True, 1)

        for prop in self.plugin.get_properties():
            self.configuration_store.append([prop.get("label")])
        self.configuration.show_all()

    # ----------------------------------------------------------------------
    def __create_code_tab(self):
        for widget in self.code.get_children():
            self.code.remove(widget)
        vbox = Gtk.VBox()
        self.code.add(vbox)

        # Button bar
        button_bar = Gtk.HBox()
        data = {"label": _("Properties"), "values": ["id", "language", "framework"]}
        properties = ComboField(data, None)
        button_bar.pack_start(properties, False, False, 0)
        vbox.pack_start(button_bar, False, False, 1)

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

        self.header.set_value(self.plugin.generate_header())
        self.vars.set_value(self.plugin.generate_vars())
        self.function_call.set_value(self.plugin.generate_function_call())
        self.dealloc.set_value(self.plugin.generate_dealloc())
        self.out_dealloc.set_value(self.plugin.generate_out_dealloc())

        self.code.show_all()

    # ----------------------------------------------------------------------
    def __create_connection_tab(self):
        for widget in self.connections.get_children():
            self.connections.remove(widget)
        vbox = Gtk.VBox()
        self.connections.add(vbox)
        connectors = []
        for key in System.connectors:
            connectors.append(key)
        data = {"label": _("Connectors"), "values": connectors}
        self.connectors = ComboField(data, None)
        vbox.pack_start(self.connectors, False, False, 1)

        self.connections.show_all()

    # ----------------------------------------------------------------------
    def __new_configuration_panel(self, widget=None, data=None):
        fieldtypes = []
        for key in component_list:
            fieldtypes.append(key)
        data = {"label": _("Field Type"), "values": fieldtypes}
        self.field_type = ComboField(data, self.__select_field_type)
        self.configuration_panel.pack_start(self.field_type, False, False, 1)

    # ----------------------------------------------------------------------
    def __select_field_type(self, widget=None, data=None):
        # Clean configuration panel
        for widget in self.configuration_panel.get_children():
            self.configuration_panel.remove(widget)
        field_type = self.field_type.get_value()
        configuration = component_list[field_type].get_configuration()
        for key in configuration:
            data = {"label": _(key), "value":str(configuration[key])}
            field = StringField(data, None)
            self.configuration_panel.pack_start(field, False, False, 1)

    # ----------------------------------------------------------------------
    def __on_configuration_row_activated(self, tree_view, path, column):
        configuration = self.plugin.get_properties()[int(str(path))]
        for widget in self.configuration_panel.get_children():
            self.configuration_panel.remove(widget)
        for key in configuration:
            data = {"label": _(key), "value":str(configuration[key])}
            field = StringField(data, None)
            self.configuration_panel.pack_start(field, False, False, 1)

    # ----------------------------------------------------------------------
    def __new_plugin(self, widget=None, data=None):
        # Add new plugin to be configurated
        self.add_block(Plugin())
# ----------------------------------------------------------------------
