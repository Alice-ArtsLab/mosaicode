#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os

from menu import Menu
from toolbar import Toolbar
from searchbar import SearchBar
from harpia.control.maincontrol import MainControl
from blockstreeview import BlocksTreeView
from blockproperties import BlockProperties
from status import Status
from workarea import WorkArea

class MainWindow(Gtk.Window):

    def __init__(self):
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
        # |vpaned_left
        # -----------------------------------------------------

        vpaned_left.add1(self.__create_frame(self.blocks_tree_view))
        vpaned_left.add2(self.__create_frame(self.block_properties))
        vpaned_left.set_position(300)

        self.connect("delete-event", self.quit)

        self.main_control.append_status_log("123 \n test")
        self.main_control.set_help("123 testando\n\n Novidades")
        self.status.append_text("Eu tu ele \n Nós vós eles")
        self.blocks_tree_view.add_item("Teste", "Nostradamus")
        self.blocks_tree_view.add_item("Teste 2", "Nostradamus")
        self.blocks_tree_view.add_item("Teste 3", "Nostradamus")
        self.blocks_tree_view.add_item("Ficção", "Éramos 6")
        self.blocks_tree_view.add_item("Romance", "Éramos 6")
        self.blocks_tree_view.add_item("Multiplicação", "Aritmética")
        self.blocks_tree_view.add_item("Divisão", "Aritmética")
        self.blocks_tree_view.add_item("Subtração", "Aritmética")
        self.blocks_tree_view.add_item("Romance", "Aritmética")

        self.menu.add_example("123 mudar")
        self.menu.add_example("/home/flavio/teste123")

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
