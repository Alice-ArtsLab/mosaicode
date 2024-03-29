#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the MainWindow class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, Gtk
import os

from mosaicode.system import System as System
from mosaicode.control.maincontrol import MainControl
from mosaicode.GUI.blockmenu import BlockMenu
from mosaicode.GUI.diagrammenu import DiagramMenu
from mosaicode.GUI.blocknotebook import BlockNotebook
from mosaicode.GUI.menu import Menu
from mosaicode.GUI.propertybox import PropertyBox
from mosaicode.GUI.searchbar import SearchBar
from mosaicode.GUI.status import Status
from mosaicode.GUI.toolbar import Toolbar
from mosaicode.GUI.workarea import WorkArea

class MainWindow(Gtk.Window):
    """
    This class contains methods related the MainWindow class.
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        """
        This method is constructor.
        """
        System()
        Gtk.Window.__init__(self, title="Mosaicode")
        self.resize(
            System.get_preferences().width,
            System.get_preferences().height)
        self.main_control = MainControl(self)
        
        # GUI components
        self.menu = Menu(self)
        self.toolbar = Toolbar(self)
        self.search = SearchBar(self)
        self.block_notebook = BlockNotebook(self)
        self.property_box = PropertyBox(self)
        self.work_area = WorkArea(self)
        self.status = Status(self)
        self.diagram_menu = DiagramMenu()
        self.menu.add_help()
        self.block_menu = BlockMenu()

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
        self.hpaned_work_area.set_position(
            System.get_preferences().hpaned_work_area)

        self.vpaned_bottom.add1(self.hpaned_work_area)
        self.vpaned_bottom.add2(self.__create_frame(self.status))
        self.vpaned_bottom.set_position(System.get_preferences().vpaned_bottom)
        self.vpaned_bottom.set_size_request(50, 50)

        # hpaned_work_area
        # -----------------------------------------------------
        # | vbox_left      ||   work_area
        # -----------------------------------------------------
        vbox_left = Gtk.VBox(homogeneous=False, spacing=0)
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
        # |property_box
        # -----------------------------------------------------

        self.vpaned_left.add1(self.__create_frame(self.block_notebook))
        self.vpaned_left.add2(self.__create_frame(self.property_box))
        self.vpaned_left.set_position(System.get_preferences().vpaned_left)

        self.connect("key-press-event", self.__on_key_press)
        self.connect("check-resize", self.__resize)
        self.connect("delete-event", self.main_control.exit)

        self.main_control.init()

        # Load the plugin
        from mosaicode.plugins.extensionsmanager.extensionsmanager \
            import ExtensionsManager as em
        em().load(self)
        
    # ----------------------------------------------------------------------
    def __on_key_press(self, widget, event=None):
        if event.state == \
                Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK \
                and event.keyval == Gdk.KEY_a:
            self.main_control.select_all()
            return True
        else:
            return False

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
        System.get_preferences().width = width
        System.get_preferences().height = height
        System.get_preferences().hpaned_work_area = self.hpaned_work_area.get_position()
        System.get_preferences().vpaned_bottom = self.vpaned_bottom.get_position()
        System.get_preferences().vpaned_left = self.vpaned_left.get_position()
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
