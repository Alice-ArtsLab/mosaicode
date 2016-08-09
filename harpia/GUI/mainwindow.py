#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from glob import glob # To load examples
import os

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
        self.set_default_size(800,600)
        self.main_control = MainControl(self)

        #GUI components
        self.menu = Menu(self)
        self.toolbar = Toolbar(self)
        self.search = SearchBar(self)
        self.blocks_tree_view = BlocksTreeView(self)
        self.block_properties = BlockProperties(self)
        self.work_area = WorkArea(self)
        self.status = Status(self)

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
        vpaned_bottom = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
        vbox_main.add(vpaned_bottom)


        # vpaned_bottom 
        # -----------------------------------------------------
        # | hpaned_work_area
        # =====================================================
        # | status
        # -----------------------------------------------------

        hpaned_work_area = Gtk.HPaned()
        vpaned_bottom.add1(hpaned_work_area)
        vpaned_bottom.add2(self.__create_frame(self.status))
        vpaned_bottom.set_position(420)

        # hpaned_work_area
        # -----------------------------------------------------
        # | vbox_left      ||   work_area
        # -----------------------------------------------------
        vbox_left = Gtk.VBox(False, 0)
        hpaned_work_area.add1(vbox_left)
        hpaned_work_area.add2(self.work_area)

        # vbox_left
        # -----------------------------------------------------
        # |search
        # -----------------------------------------------------
        # |vpaned_left
        # -----------------------------------------------------

        vbox_left.pack_start(self.search, False, False, 0)
        vpaned_left = Gtk.VPaned()
        vbox_left.pack_start(vpaned_left, True, True, 0)


        # vpaned_left
        # -----------------------------------------------------
        # |blocks_tree_view
        # =====================================================
        # | block_properties
        # -----------------------------------------------------

        vpaned_left.add1(self.__create_frame(self.blocks_tree_view))
        vpaned_left.add2(self.__create_frame(self.block_properties))
        vpaned_left.set_position(300)

        self.connect("delete-event", self.quit)

        # Load Examples
        list_of_examples = glob(os.environ['HARPIA_DATA_DIR'] + "examples/*")
        list_of_examples.sort()

        for example in list_of_examples:
            self.menu.add_example(example)

        self.menu.add_recent_file("/home/flavio/Desktop/harpiaTest.hrp")
        self.menu.add_recent_file("/home/flavio/Desktop/harpiaTest2.hrp")

    def __create_frame(self, widget):
        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        frame.add(widget)
        frame.set_property("border-width", 4)
        return frame

    def quit(self, widget, data):
        print "Bye"
        Gtk.main_quit()
