#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
from gi.repository import Gtk
from harpia.system import System as System

gi.require_version('Gtk', '3.0')


class Menu(Gtk.MenuBar):

    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        Gtk.MenuBar.__init__(self)
        self.main_window = main_window

        mc = self.main_window.main_control
        self.accel_group = Gtk.AccelGroup()
        self.main_window.add_accel_group(self.accel_group)
        # dictionary component: action
        self.list_of_examples = []
        self.actions = {}

        # -------------------------- File -------------------------------------
        file_menu = Gtk.Menu()
        self.recent_files_menu = Gtk.Menu()
        self.__create_menu("New", "<Control>N", file_menu, mc.new)
        self.__create_menu("Open", "<Control>O", file_menu, mc.select_open)
        self.__create_menu("Close", "<Control>W", file_menu, mc.close)
        recents = self.__create_menu("Recents", None, file_menu, None)
        recents.set_submenu(self.recent_files_menu)
        file_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu("Save", "<Control>S", file_menu, mc.save)
        self.__create_menu("Save As...", None, file_menu, mc.save_as)
        self.__create_menu("Rename", None, file_menu, mc.rename_tab)
        file_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu(
            "Export Diagram As PNG", "<Control>E",
            file_menu, mc.export_diagram)
        file_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu("Exit", "<Control>Q", file_menu, mc.exit)
        self.__add_menu_category("File", file_menu)

        # -------------------------- Edit -------------------------------------
        edit_menu = Gtk.Menu()
        self.__create_menu("Undo", "<Control>Z", edit_menu, mc.undo)
        self.__create_menu("Redo", "<Shift><Control>Z", edit_menu, mc.redo)
        edit_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu(
            "Select All", "<Control>A", edit_menu, mc.select_all)
        self.__create_menu("Cut", "<Control>X", edit_menu, mc.cut)
        self.__create_menu("Copy", "<Control>C", edit_menu, mc.copy)
        self.__create_menu("Paste", "<Control>V", edit_menu, mc.paste)
        self.__create_menu("Delete", "Delete", edit_menu, mc.delete)
        edit_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu(
            "Clear Console", "<Control>L", edit_menu, mc.clear_console)
        edit_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu("Preferences", None, edit_menu, mc.preferences)
        self.__add_menu_category("Edit", edit_menu)

        # -------------------------- View -------------------------------------
        view_menu = Gtk.Menu()
        self.__create_menu("Zoom In", None, view_menu, mc.zoom_in)
        self.__create_menu("Zoom Out", None, view_menu, mc.zoom_out)
        self.__create_menu(
            "Normal Size", "<Control>0", view_menu, mc.zoom_normal)
        self.__add_menu_category("View", view_menu)

        # -------------------------- Process --------------------------------
        process_menu = Gtk.Menu()
        self.__create_menu("Run", "<Control>R", process_menu, mc.run)
        self.__create_menu("Save Source", None, process_menu, mc.save_source)
        self.__create_menu("View Source", None, process_menu, mc.view_source)
        self.__add_menu_category("Process", process_menu)

        # -------------------------- Help -----------------------------------
        # Cria sub menu
        help_menu = Gtk.Menu()
        self.example_menu = Gtk.Menu()
        examples = self.__create_menu("Example", None, help_menu, None)
        examples.set_submenu(self.example_menu)
        help_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu("About", None, help_menu, mc.about)
        self.__add_menu_category("Help", help_menu)

    # ----------------------------------------------------------------------
    def __create_menu(self, name, accel, menu, action):
        item = Gtk.MenuItem(name)
        if accel is not None:
            key, mod = Gtk.accelerator_parse(accel)
            item.add_accelerator(
                "activate", self.accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(item)
        if action is not None:
            item.connect("activate", self.__menu_clicked, None)
            self.actions[item] = action
        return item

    # ----------------------------------------------------------------------
    def __add_menu_category(self, name, submenu):
        menu_item = Gtk.MenuItem(name)
        menu_item.show()
        menu_item.set_submenu(submenu)
        self.append(menu_item)

    # ----------------------------------------------------------------------
    def __menu_clicked(self, widget, data):
        self.actions[widget]()

    # ----------------------------------------------------------------------
    def __load_recent(self, widget, data):
        self.main_window.main_control.open(widget.get_label())

    # ----------------------------------------------------------------------
    def add_example(self, example):
        self.list_of_examples.append(example)
        menu_item = Gtk.MenuItem(example.split("/").pop())
        self.example_menu.append(menu_item)
        menu_item.connect(
            "activate", self.__load_example, len(self.list_of_examples) - 1)
        self.example_menu.show_all()

    # ----------------------------------------------------------------------
    def __load_example(self, widget, data):
        self.main_window.main_control.open(self.list_of_examples[int(data)])

    # ----------------------------------------------------------------------
    def update_recent_file(self):
        for widget in self.recent_files_menu.get_children():
            self.recent_files_menu.remove(widget)
        for recent_file in System.properties.get_recent_files_as_array():
            self.__add_recent_file(recent_file)

    # ----------------------------------------------------------------------
    def __add_recent_file(self, recent_file):
        menu_item = Gtk.MenuItem(recent_file)
        self.recent_files_menu.append(menu_item)
        menu_item.connect("activate", self.__load_recent, None)
        self.recent_files_menu.show_all()
