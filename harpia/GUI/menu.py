#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Menu(Gtk.MenuBar):

    def __init__(self, main_window):
        Gtk.MenuBar.__init__(self)
        self.main_window = main_window
        # dictionary component: action
        self.actions = {}

        # -------------------------- File --------------------------------------
        file_menu = Gtk.Menu()
        self.__create_menu("New", file_menu, self.main_window.main_control.new)
        self.__create_menu("Open", file_menu, self.main_window.main_control.open)
        self.__create_menu("Close", file_menu, self.main_window.main_control.close)
        self.__create_menu("Recents", file_menu, self.main_window.main_control.recent)
        self.__create_menu("Save", file_menu, self.main_window.main_control.save)
        self.__create_menu("Save As...", file_menu, self.main_window.main_control.save_as)
        self.__create_menu("Export Diagram As PNG", file_menu, self.main_window.main_control.export_diagram)
        self.__create_menu("Exit", file_menu, self.main_window.main_control.exit)
        self.__add_menu_category("File", file_menu)

        # -------------------------- Edit --------------------------------------
        edit_menu = Gtk.Menu()
        self.__create_menu("Cut", edit_menu, self.main_window.main_control.cut)
        self.__create_menu("Copy", edit_menu, self.main_window.main_control.copy)
        self.__create_menu("Paste", edit_menu, self.main_window.main_control.paste)
        self.__create_menu("Delete", edit_menu, self.main_window.main_control.delete)
        self.__create_menu("Preferences", edit_menu, self.main_window.main_control.preferences)
        self.__add_menu_category("Edit", edit_menu)

        # -------------------------- View --------------------------------------
        view_menu = Gtk.Menu()
        self.__create_menu("Zoom In", view_menu, self.main_window.main_control.zoom_in)
        self.__create_menu("Zoom Out", view_menu, self.main_window.main_control.zoom_out)
        self.__create_menu("Normal Size", view_menu, self.main_window.main_control.zoom_normal)
        self.__create_menu("Show Search Bar", view_menu, self.main_window.main_control.show_search_bar)
        self.__add_menu_category("View", view_menu)

        # -------------------------- Process --------------------------------------
        process_menu = Gtk.Menu()
        self.__create_menu("Run", process_menu, self.main_window.main_control.run)
        self.__create_menu("Save Source", process_menu, self.main_window.main_control.save_source)
        self.__create_menu("View Source", process_menu, self.main_window.main_control.view_source)
        self.__add_menu_category("Process", process_menu)

        # -------------------------- Help --------------------------------------
        #Cria sub menu
        help_menu = Gtk.Menu()
        #Cria o items com o nome fornecido
        self.__create_menu("Tips of The Day", help_menu, self.main_window.main_control.tips)
        self.__create_menu("Example", help_menu, self.main_window.main_control.example)
        self.__create_menu("About", help_menu, self.main_window.main_control.about)
        self.__add_menu_category("Help", help_menu)

    def __create_menu(self, name, menu, action):
        item = Gtk.MenuItem(name)
        menu.append(item)
        item.connect("activate", self.__menu_clicked, None)
        self.actions[item] = action
        return item

    def __add_menu_category(self, name, submenu):
        menu_item = Gtk.MenuItem(name)
        menu_item.show()
        menu_item.set_submenu(submenu)
        self.append(menu_item)

    def __menu_clicked(self, widget, data):
        self.actions[widget]()
