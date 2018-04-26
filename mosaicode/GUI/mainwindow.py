#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the MainWindow class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

from menu import Menu
from status import Status
from toolbar import Toolbar
from workarea import WorkArea
from searchbar import SearchBar
from blocknotebook import BlockNotebook
from mosaicode.system import System as System
from blockproperties import BlockProperties
from mosaicode.control.maincontrol import MainControl
from mosaicode.GUI.blockmenu import BlockMenu

class MainWindow(Gtk.Window):
    """
    This class contains methods related the MainWindow class.
    """

    def __init__(self):
        """
        This method is constructor.
        """
        System()
        Gtk.Window.__init__(self, title="Mosaicode")
        # self.set_default_size(800,600)
        self.resize(
            System.properties.width,
            System.properties.height)
        self.main_control = MainControl(self)

        # GUI components
        self.menu = Menu(self)
        self.toolbar = Toolbar(self)
        self.search = SearchBar(self)
        self.block_notebook = BlockNotebook(self)
        self.block_properties = BlockProperties(self)
        self.work_area = WorkArea(self)
        self.status = Status(self)
        self.block_menu = BlockMenu()

        # Load plugins
        for plugin in System.instance.plugins:
            plugin.load(self)

        self.menu.add_help()

        System.set_log(self.status)

        # vbox main
        # -----------------------------------------------------
        # | Menu
        # -----------------------------------------------------
        # | Toolbar
        # -----------------------------------------------------
        # | V Paned bottom
        # -----------------------------------------------------

        # First Vertical Box
        vbox_main = Gtk.VBox()
        self.add(vbox_main)
        vbox_main.pack_start(self.menu, False, True, 0)
        vbox_main.pack_start(self.toolbar, False, False, 0)
        self.vpaned_bottom = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
        vbox_main.add(self.vpaned_bottom)

        # vpaned_bottom
        # -----------------------------------------------------
        # | hpaned_work_area
        # =====================================================
        # | status
        # -----------------------------------------------------

        self.hpaned_work_area = Gtk.HPaned()
        self.hpaned_work_area.connect("accept-position", self.__resize)
        self.hpaned_work_area.set_position(System.properties.hpaned_work_area)

        self.vpaned_bottom.add1(self.hpaned_work_area)
        self.vpaned_bottom.add2(self.__create_frame(self.status))
        self.vpaned_bottom.set_position(System.properties.vpaned_bottom)
        self.vpaned_bottom.set_size_request(50, 50)

        # hpaned_work_area
        # -----------------------------------------------------
        # | vbox_left      ||   work_area
        # -----------------------------------------------------
        vbox_left = Gtk.VBox(False, 0)
        self.hpaned_work_area.add1(vbox_left)
        self.hpaned_work_area.add2(self.work_area)

        # vbox_left
        # -----------------------------------------------------
        # |search
        # -----------------------------------------------------
        # |vpaned_left
        # -----------------------------------------------------

        vbox_left.pack_start(self.search, False, False, 0)
        self.vpaned_left = Gtk.VPaned()
        vbox_left.pack_start(self.vpaned_left, True, True, 0)

        # vpaned_left
        # -----------------------------------------------------
        # |blocks_tree_view
        # =====================================================
        # | block_properties
        # -----------------------------------------------------

        self.vpaned_left.add1(self.__create_frame(self.block_notebook))
        self.vpaned_left.add2(self.__create_frame(self.block_properties))
        self.vpaned_left.set_position(System.properties.vpaned_left)

        self.connect("delete-event", self.main_control.exit)
        self.connect("key-press-event", self.__on_key_press)
        self.connect("check-resize", self.__resize)

        self.main_control.init()

    # ----------------------------------------------------------------------
    def __on_key_press(self, widget, event=None):
        if event.state == \
                Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK:
            if event.keyval == Gdk.KEY_a:
                self.main_control.select_all()
                return True

    # ----------------------------------------------------------------------
    def __create_frame(self, widget):
        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        frame.add(widget)
        frame.set_property("border-width", 4)
        return frame

    # ----------------------------------------------------------------------
    def __resize(self, data):
        width, height = self.get_size()
        System.properties.width = width
        System.properties.height = height
        System.properties.hpaned_work_area = self.hpaned_work_area.get_position()
        System.properties.vpaned_bottom = self.vpaned_bottom.get_position()
        System.properties.vpaned_left = self.vpaned_left.get_position()
        self.work_area.resize(data)

    # ----------------------------------------------------------------------
    def update(self):
        self.main_control.update_all()

    # ----------------------------------------------------------------------
    def set_title(self, title):
        """
        This method set title.

            Parameters:
                * **title** (:class:`str<str>`)

        """
        Gtk.Window.set_title(self, "Mosaicode (" + title + ")")
# ----------------------------------------------------------------------
