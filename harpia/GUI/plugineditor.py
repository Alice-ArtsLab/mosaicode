#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the PluginManager class.
"""
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


class PluginEditor(Gtk.Dialog):
    """
    This class contains methods related the PluginManager class
    """

    # ----------------------------------------------------------------------
    def __init__(self, plugin_manager, plugin):
        Gtk.Dialog.__init__(self, _("Plugin Editor"),
                            plugin_manager,
                            0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        self.plugin_manager = plugin_manager
        self.plugin = plugin
        self.main_control = self
        self.set_default_size(800, 600)
        box = self.get_content_area()

        self.tabs = Gtk.Notebook()
        self.tabs.set_scrollable(True)
        box.pack_start(self.tabs, True, True, 0)

        # ----------------------------------------------------------------------
        # Common properties Section
        # ----------------------------------------------------------------------
        self.common_properties = Gtk.ScrolledWindow()
        self.common_properties.set_shadow_type(Gtk.ShadowType.IN)
        self.tabs.append_page(self.common_properties, Gtk.Label(_("Common Properties")))
        self.__create_common_properties_tab()
        # ----------------------------------------------------------------------
        # Properties section
        # ----------------------------------------------------------------------
        self.props = Gtk.ScrolledWindow()
        self.props.set_shadow_type(Gtk.ShadowType.IN)
        self.tabs.append_page(self.props, Gtk.Label(_("Properties")))
        self.__create_props_tab()
        # ----------------------------------------------------------------------
        # Connections Section
        # ----------------------------------------------------------------------
        self.connections = Gtk.ScrolledWindow()
        self.connections.set_shadow_type(Gtk.ShadowType.IN)
        self.tabs.append_page(self.connections, Gtk.Label(_("Ports")))
        self.__create_connection_tab()
        # ----------------------------------------------------------------------
        # Code section
        # ----------------------------------------------------------------------
        self.code = Gtk.ScrolledWindow()
        self.code.set_shadow_type(Gtk.ShadowType.IN)
        self.tabs.append_page(self.code, Gtk.Label(_("Code")))
        self.__create_code_tab()

        self.show_all()
        self.__set_plugin(plugin)
        result = self.run()
        if result == Gtk.ResponseType.OK:
            self.__save()
        self.close()
        self.destroy()

    # ----------------------------------------------------------------------
    def __create_common_properties_tab(self):
        for widget in self.common_properties.get_children():
            self.common_properties.remove(widget)
        vbox = Gtk.VBox()
        self.common_properties.add(vbox)

        self.label = StringField({"label": _("Label")}, self.notify)
        self.language = StringField({"label": _("Language")}, self.notify)
        self.framework = StringField({"label": _("Framework")}, self.notify)
        self.type = StringField({"label": _("Plugin Type")}, None)
        self.group = StringField({"label": _("Group")}, None)
        self.color = ColorField({"label": _("Color")}, None)
        self.help = CommentField({"label": _("Help")}, None)

        self.color.set_parent_window(self)

        vbox.pack_start(self.label, False, False, 1)
        vbox.pack_start(self.language, False, False, 1)
        vbox.pack_start(self.framework, False, False, 1)
        vbox.pack_start(self.type, False, False, 1)
        vbox.pack_start(self.group, False, False, 1)
        vbox.pack_start(self.color, False, False, 1)
        vbox.pack_start(self.help, False, False, 1)

    # ----------------------------------------------------------------------
    def notify(self, widget=None, data=None):
        self.type.set_value("harpia.plugins." + \
                self.language.get_value().lower() + "." + \
                self.framework.get_value().lower() + "." + \
                self.label.get_value().lower().replace(" ","")
                )

    # ----------------------------------------------------------------------
    def __create_props_tab(self):
        for widget in self.props.get_children():
            self.props.remove(widget)
        hbox = Gtk.HBox()
        vbox2 = Gtk.VBox()
        self.props.add(hbox)
        sw = Gtk.ScrolledWindow()
        self.props_store = Gtk.ListStore(str)
        self.props_tree_view = Gtk.TreeView(self.props_store)
        self.props_tree_view.connect("row-activated",
                self.__on_props_row_activated)
        sw.add(self.props_tree_view)

        col = Gtk.TreeViewColumn(_("Properties"))
        self.props_tree_view.append_column(col)

        cellrenderertext = Gtk.CellRendererText()
        col.pack_end(cellrenderertext, True)
        col.add_attribute(cellrenderertext, "text", 0)

        vbox2.pack_start(sw, True, True, 1)

        # Button bar
        button_bar = Gtk.HBox()

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_NEW)
        button.connect("clicked", self.__property_new, None)
        button_bar.pack_start(button, False, False, 0)

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_DELETE)
        button.connect("clicked", self.__property_delete, None)
        button_bar.pack_start(button, False, False, 0)

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_GO_UP)
        button.connect("clicked", self.__property_up, None)
        button_bar.pack_start(button, False, False, 0)

        button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_GO_DOWN)
        button.connect("clicked", self.__property_down, None)
        button_bar.pack_start(button, False, False, 0)

        vbox2.pack_start(button_bar, False, False, 1)

        hbox.pack_start(vbox2, True, True, 2)
        vbox = Gtk.VBox()
        hbox.pack_start(vbox, True, True, 2)
        self.props_panel = Gtk.VBox()
        vbox.pack_start(self.props_panel, True, True, 1)

        for prop in self.plugin.get_properties():
            self.props_store.append([prop.get("label")])

    # ----------------------------------------------------------------------
    def __property_new(self, widget=None, data=None):
        fieldtypes = []
        for key in component_list:
            fieldtypes.append(key)
        data = {"label": _("Field Type"), "values": fieldtypes}
        self.field_type = ComboField(data, self.__select_property_field_type)
        self.props_panel.pack_start(self.field_type, False, False, 1)

    # ----------------------------------------------------------------------
    def __property_delete(self, widget=None, data=None):
        pass

    # ----------------------------------------------------------------------
    def __property_up(self, widget=None, data=None):
        pass

    # ----------------------------------------------------------------------
    def __property_down(self, widget=None, data=None):
        pass

    # ----------------------------------------------------------------------
    def __select_property_field_type(self, widget=None, data=None):
        # Clean configuration panel
        for widget in self.props_panel.get_children():
            self.props_panel.remove(widget)
        field_type = self.field_type.get_value()
        configuration = component_list[field_type].get_configuration()
        for key in configuration:
            data = {"label": _(key), "value": str(configuration[key])}
            field = StringField(data, None)
            self.props_panel.pack_start(field, False, False, 1)

    # ----------------------------------------------------------------------
    def __on_props_row_activated(self, tree_view, path, column):
        configuration = self.plugin.get_properties()[int(str(path))]
        for widget in self.props_panel.get_children():
            self.props_panel.remove(widget)
        for key in configuration:
            data = {"label": _(key),
                    "name":key,
                    "value":str(configuration[key])}
            field = StringField(data, None)
            self.props_panel.pack_start(field, False, False, 1)
        button = Gtk.Button.new_with_label("Save")
        button.connect("clicked", self.__on_props_edit_ok, path)
        self.props_panel.pack_start(button, False, False, 1)

    # ----------------------------------------------------------------------
    def __on_props_edit_ok(self, widget=None, data=None):
        pass

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
        self.vars = CodeField({"label": _("Vars")}, None)
        self.function_call = CodeField({"label": _("Function Call")}, None)
        self.dealloc = CodeField({"label": _("Dealloc")}, None)
        self.out_dealloc = CodeField({"label": _("Out Dealloc")}, None)

        codes.append_page(self.header, Gtk.Label(_("Header")))
        codes.append_page(self.vars, Gtk.Label(_("Vars")))
        codes.append_page(self.function_call, Gtk.Label(_("Function Call")))
        codes.append_page(self.dealloc, Gtk.Label(_("Dealloc")))
        codes.append_page(self.out_dealloc, Gtk.Label(_("Out Dealloc")))

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

    # ----------------------------------------------------------------------
    def __set_plugin(self, plugin):
        """
        This method add a plugin.

            Parameters:
                * **plugin** (:class:`<>`)
        """
        self.type.set_value(plugin.get_type())
        self.language.set_value(plugin.language)
        self.framework.set_value(plugin.framework)

        self.label.set_value(plugin.get_label())
        self.group.set_value(plugin.get_group())
        self.color.set_value(plugin.get_color())
        self.help.set_value(plugin.get_help())

        self.header.set_value(plugin.generate_header())
        self.vars.set_value(plugin.generate_vars())
        self.function_call.set_value(plugin.generate_function_call())
        self.dealloc.set_value(plugin.generate_dealloc())
        self.out_dealloc.set_value(plugin.generate_out_dealloc())

    # ----------------------------------------------------------------------
    def __save(self):
        """
        This method save the plugin.
            Parameters:
                * **plugin** (:class:`<>`)
        """

        self.plugin.type = self.type.get_value()
        self.plugin.language = self.language.get_value()
        self.plugin.framework = self.framework.get_value()

        self.plugin.label = self.label.get_value()
        self.plugin.group = self.group.get_value()
        self.plugin.color = self.color.get_value()
        self.plugin.help = self.help.get_value()

        self.plugin.header = self.header.get_value()
        self.plugin.vars = self.vars.get_value()
        self.plugin.function_call = self.function_call.get_value()
        self.plugin.dealloc = self.dealloc.get_value()
        self.plugin.out_dealloc = self.out_dealloc.get_value()
        self.plugin_manager.add_plugin(self.plugin)

# ----------------------------------------------------------------------
