#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

from menu import Menu
from toolbar import Toolbar
from searchbar import SearchBar
from harpia.control.maincontrol import MainControl
from blockstreeview import BlocksTreeView
from blockproperties import BlockProperties
from status import Status
from workarea import WorkArea

from harpia.constants import *
from harpia import s2idirectory

class MainWindow(Gtk.Window):

    def __init__(self):
        s2idirectory.load()
        Gtk.Window.__init__(self, title="Harpia")
        #self.set_default_size(800,600)
        self.resize(
                s2idirectory.properties.get_width(),
                s2idirectory.properties.get_height())
        self.main_control = MainControl(self)
        self.connect("check-resize", self.__resize)

        #GUI components
        self.menu = Menu(self)
        self.toolbar = Toolbar(self)
        self.search = SearchBar(self)
        self.blocks_tree_view = BlocksTreeView(self)
        self.block_properties = BlockProperties(self)
        self.work_area = WorkArea(self)
        self.status = Status(self)
        s2idirectory.Log = self.status

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
        self.hpaned_work_area.set_position(s2idirectory.properties.get_hpaned_work_area())

        self.vpaned_bottom.add1(self.hpaned_work_area)
        self.vpaned_bottom.add2(self.__create_frame(self.status))
        self.vpaned_bottom.set_position(s2idirectory.properties.get_vpaned_bottom())
        self.vpaned_bottom.set_size_request(50,50)

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

        self.vpaned_left.add1(self.__create_frame(self.blocks_tree_view))
        self.vpaned_left.add2(self.__create_frame(self.block_properties))
        self.vpaned_left.set_position(s2idirectory.properties.get_vpaned_left())

        self.connect("delete-event", self.main_control.exit)
        self.connect("key-press-event", self.__on_key_press)

        for example in s2idirectory.list_of_examples:
            self.menu.add_example(example)
        self.menu.update_recent_file()

    #----------------------------------------------------------------------
    def __on_key_press(self, widget, event=None):
        if event.state == Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK:
            if event.keyval == Gdk.KEY_a:
                self.main_control.select_all()
                return True

    #----------------------------------------------------------------------
    def __create_frame(self, widget):
        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        frame.add(widget)
        frame.set_property("border-width", 4)
        return frame

    #----------------------------------------------------------------------
    def __resize(self, data):
        width, height = self.get_size()
        s2idirectory.properties.set_width(width)
        s2idirectory.properties.set_height(height)
        s2idirectory.properties.set_hpaned_work_area(self.hpaned_work_area.get_position())
        s2idirectory.properties.set_vpaned_bottom(self.vpaned_bottom.get_position())
        s2idirectory.properties.set_vpaned_left(self.vpaned_left.get_position())
        self.work_area.resize(data)

    def set_title(self, title):
        Gtk.Window.set_title(self, "Harpia (" + title + ")")
#----------------------------------------------------------------------
