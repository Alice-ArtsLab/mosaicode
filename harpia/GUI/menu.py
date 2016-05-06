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
        self.list_of_examples = []
        self.actions = {}

        # -------------------------- File --------------------------------------
        file_menu = Gtk.Menu()
        self.recent_files_menu = Gtk.Menu()
        self.__create_menu("New", file_menu, self.main_window.main_control.new)
        self.__create_menu("Open", file_menu, self.main_window.main_control.select_open)
        self.__create_menu("Close", file_menu, self.main_window.main_control.close)
        recents = self.__create_menu("Recents", file_menu, None)
        recents.set_submenu(self.recent_files_menu)
        file_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu("Save", file_menu, self.main_window.main_control.save)
        self.__create_menu("Save As...", file_menu, self.main_window.main_control.save_as)
        file_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu("Export Diagram As PNG", file_menu, self.main_window.main_control.export_diagram)
        file_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu("Exit", file_menu, self.main_window.main_control.exit)
        self.__add_menu_category("File", file_menu)

        # -------------------------- Edit --------------------------------------
        edit_menu = Gtk.Menu()
        self.__create_menu("Cut", edit_menu, self.main_window.main_control.cut)
        self.__create_menu("Copy", edit_menu, self.main_window.main_control.copy)
        self.__create_menu("Paste", edit_menu, self.main_window.main_control.paste)
        self.__create_menu("Delete", edit_menu, self.main_window.main_control.delete)
        edit_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu("Preferences", edit_menu, self.main_window.main_control.preferences)
        self.__add_menu_category("Edit", edit_menu)

        # -------------------------- View --------------------------------------
        view_menu = Gtk.Menu()
        self.__create_menu("Zoom In", view_menu, self.main_window.main_control.zoom_in)
        self.__create_menu("Zoom Out", view_menu, self.main_window.main_control.zoom_out)
        self.__create_menu("Normal Size", view_menu, self.main_window.main_control.zoom_normal)
        view_menu.append(Gtk.SeparatorMenuItem())
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
        self.example_menu = Gtk.Menu()

        #Cria o items com o nome fornecido
        self.__create_menu("Tips of The Day", help_menu, self.main_window.main_control.tips)
        help_menu.append(Gtk.SeparatorMenuItem())
        examples = self.__create_menu("Example", help_menu, None)
        examples.set_submenu(self.example_menu)
        help_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu("About", help_menu, self.main_window.main_control.about)
        help_menu.append(Gtk.SeparatorMenuItem())
        self.__add_menu_category("Help", help_menu)


    def __create_menu(self, name, menu, action):
        item = Gtk.MenuItem(name)
        menu.append(item)
        if action != None :
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

    def __load_example(self, widget, data):
        self.main_window.main_control.open(self.list_of_examples[int(data)])

    def __load_recent(self, widget, data):
        self.main_window.main_control.open(widget.get_label())

    def add_example(self, example):
        self.list_of_examples.append(example)
        menu_item = Gtk.MenuItem(example.split("/").pop())
        self.example_menu.append(menu_item)
        menu_item.connect("activate", self.__load_example, len(self.list_of_examples) - 1)
        self.example_menu.show_all()
 
    def add_recent_file(self, recent_file):
        menu_item = Gtk.MenuItem(recent_file)
        self.recent_files_menu.append(menu_item)
        menu_item.connect("activate", self.__load_recent, None)
        self.recent_files_menu.show_all()
 
