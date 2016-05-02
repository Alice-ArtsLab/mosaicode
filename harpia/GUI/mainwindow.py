#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from menu import Menu
from toolbar import Toolbar
from searchbar import SearchBar
from maincontrol import MainControl
from blockstreeview import BlocksTreeView
from blockdescription import BlockDescription
from status import Status
from diagram import Diagram

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Mandragora")
        self.set_default_size(800,600)
        self.main_control = MainControl(self)

        #GUI components
        self.menu = Menu(self)
        self.toolbar = Toolbar(self)
        self.search = SearchBar(self)
        self.blocks_tree_view = BlocksTreeView(self)
        self.block_description = BlockDescription(self)
        self.diagram = Diagram(self)
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
        # | vbox_left      ||   diagram
        # -----------------------------------------------------
        vbox_left = Gtk.VBox(False, 0)
        hpaned_work_area.add1(vbox_left)
        hpaned_work_area.add2(self.diagram)

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
        vpaned_left.add2(self.__create_frame(self.block_description))
        vpaned_left.set_position(300)

        self.block_description.set_text("123 testando\n\n Novidades")
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

        self.diagram.add_tab("Teste 1")
        self.diagram.add_tab("Teste 2")
        self.diagram.add_tab("Teste 3")
        self.diagram.add_tab("Capricórnio bovino")

        self.menu.add_example("123 mudar")

    def __create_frame(self, widget):
        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        frame.add(widget)
        frame.set_property("border-width", 4)
        return frame

if __name__ == "__main__":
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
