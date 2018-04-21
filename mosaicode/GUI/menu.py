#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the menu bar.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import gettext

_ = gettext.gettext


class Menu(Gtk.MenuBar):
    """
    This class contains methods related the Menu class
    """
    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        """Constructor."""
        Gtk.MenuBar.__init__(self)
        self.main_window = main_window

        mc = self.main_window.main_control
        self.accel_group = Gtk.AccelGroup()
        self.main_window.add_accel_group(self.accel_group)

        self.actions = {}
        # -------------------------- File -------------------------------------
        file_menu = Gtk.Menu()
        self.recent_files_menu = Gtk.Menu()
        self.create_menu(_("New"), "<Control>N", file_menu, mc.new)
        self.create_menu(_("Open"), "<Control>O", file_menu, mc.select_open)
        self.create_menu(_("Close"), "<Control>W", file_menu, mc.close)
        recents = self.create_menu(_("Recents"), None, file_menu, None)
        recents.set_submenu(self.recent_files_menu)
        file_menu.append(Gtk.SeparatorMenuItem())
        self.create_menu(_("Save"), "<Control>S", file_menu, mc.save)
        self.create_menu(_("Save As..."), None, file_menu, mc.save_as)
        self.create_menu(_("Export Diagram As PNG..."), "<Control>E",
                           file_menu, mc.export_diagram)
        file_menu.append(Gtk.SeparatorMenuItem())
        self.create_menu(_("Exit"), "<Control>Q", file_menu, mc.exit)
        self.add_menu_category(_("File"), file_menu)

        # -------------------------- Edit -------------------------------------
        edit_menu = Gtk.Menu()
        self.create_menu(_("Undo"), "<Control>Z", edit_menu, mc.undo)
        self.create_menu(_("Redo"), "<Shift><Control>Z", edit_menu, mc.redo)
        edit_menu.append(Gtk.SeparatorMenuItem())
        self.create_menu(
            _("Select All"), "<Control>A", edit_menu, mc.select_all)
        self.create_menu(_("Cut"), "<Control>X", edit_menu, mc.cut)
        self.create_menu(_("Copy"), "<Control>C", edit_menu, mc.copy)
        self.create_menu(_("Paste"), "<Control>V", edit_menu, mc.paste)
        self.create_menu(_("Delete"), "Delete", edit_menu, mc.delete)
        edit_menu.append(Gtk.SeparatorMenuItem())
        self.create_menu(
            _("Clear Console"), "<Control>L", edit_menu, mc.clear_console)
        edit_menu.append(Gtk.SeparatorMenuItem())
        self.create_menu(_("Collapse All"), None, edit_menu, mc.collapse_all)
        self.create_menu(_("Uncollapse All"), None, edit_menu, mc.uncollapse_all)
        edit_menu.append(Gtk.SeparatorMenuItem())
        self.create_menu(_("Preferences"), None, edit_menu, mc.preferences)
        self.add_menu_category(_("Edit"), edit_menu)

        # -------------------------- Align -------------------------------------
        align_menu = Gtk.Menu()
        self.create_menu(_("Align Top"), "<Control>1", align_menu, mc.align_top)
        self.create_menu(_("Align Bottom"), "<Control>2", align_menu, mc.align_bottom)
        self.create_menu(_("Align Left"), "<Control>3", align_menu, mc.align_left)
        self.create_menu(_("Align Right"), "<Control>4", align_menu, mc.align_right)
        self.add_menu_category(_("Align"), align_menu)

        # -------------------------- View -------------------------------------
        view_menu = Gtk.Menu()
        self.create_menu(_("Zoom In"), None, view_menu, mc.zoom_in)
        self.create_menu(_("Zoom Out"), None, view_menu, mc.zoom_out)
        self.create_menu(
            _("Normal Size"), "<Control>0", view_menu, mc.zoom_normal)

        view_menu.append(Gtk.SeparatorMenuItem())
        self.__create_check_menu(_("Show Grid"), "<Control>g", view_menu, mc.show_grid)
        self.add_menu_category(_("View"), view_menu)

        # -------------------------- Insert -------------------------------------
        # Cria sub menu
        insert_menu = Gtk.Menu()
        self.block_menu = Gtk.Menu()
        blocks = self.create_menu(_("Block"), None, insert_menu, None)
        blocks.set_submenu(self.block_menu)
        insert_menu.append(Gtk.SeparatorMenuItem())
        self.create_menu(_("Coment"), None, insert_menu, mc.add_comment)
        self.add_menu_category(_("Insert"), insert_menu)

        # -------------------------- Process --------------------------------
        process_menu = Gtk.Menu()
        self.create_menu(_("Run"), "<Control>R", process_menu, mc.run)
        self.create_menu(_("Save Source"), None,
                           process_menu, mc.save_source)
        self.create_menu(_("View Source"), None,
                           process_menu, mc.view_source)
        self.add_menu_category(_("Process"), process_menu)

        # -------------------------- Help --------------------------------
        self.help_menu = Gtk.Menu()
        self.example_menu = Gtk.Menu()
        examples = self.create_menu(_("Example"), None, self.help_menu, None)
        examples.set_submenu(self.example_menu)
        self.help_menu.append(Gtk.SeparatorMenuItem())
        self.create_menu(_("About"), None, self.help_menu, mc.about)

    # ----------------------------------------------------------------------
    def add_help(self):
        self.add_menu_category(_("Help"), self.help_menu)

    # ----------------------------------------------------------------------
    def create_menu(self, name, accel, menu, action):
        """
        This method create the menu
            Parameters:
                * **name** (:class:`str<str>`): Name the menu.
                * **accel** (:class:`str<str>`):
                menu(Gtk.Menu): GTK.Menu().
                action(Objeto): Instance.
            Returns:
                Return menu.

        """
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
    def __create_check_menu(self, name, accel, menu, action):
        item = Gtk.CheckMenuItem(name)
        if accel is not None:
            key, mod = Gtk.accelerator_parse(accel)
            item.add_accelerator(
                "activate", self.accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(item)
        if action is not None:
            item.connect("activate", action)
            self.actions[item] = action
        return item

    # ----------------------------------------------------------------------
    def add_menu_category(self, name, submenu):
        """
        This method add a category in menu.

            Parameters:
                * **name** (:class:`str<str>`):
                * **submenu** (:class:`str<str>`):
        """
        menu_item = Gtk.MenuItem(name)
        menu_item.show()
        menu_item.set_submenu(submenu)
        self.append(menu_item)

    # ----------------------------------------------------------------------
    def __menu_clicked(self, widget, data):
        """
        This method monitors if the menu was cliked.

            Parameters:
                widget:
                data:
        """
        self.actions[widget]()

    # ----------------------------------------------------------------------
    def __load_recent(self, widget, data):
        """
        This method monitors the lasts files loaded.

            Parameters:
                widget:
                data:
            Returns:
                None.
        """
        self.main_window.main_control.open(widget.get_label())

    # ----------------------------------------------------------------------
    def __get_child_by_name(self, container, name):
        for child in container.get_children():
            if child.get_name() == name:
                return child
        return None

    # ----------------------------------------------------------------------
    def update_blocks(self, blocks):
        for widget in self.block_menu.get_children():
            self.block_menu.remove(widget)

        block_list = []
        # Copy the list to sort
        for key in blocks:
            instance = blocks[key]
            block_list.append(instance)

        # time to populate
        for block in sorted(block_list):
            # first, the language submenu
            language_menu_item = self.__get_child_by_name(self.block_menu, block.language)
            if language_menu_item is None:
                language_menu_item = Gtk.MenuItem(block.language)
                language_menu_item.set_name(block.language)
                self.block_menu.append(language_menu_item)
                language_menu = Gtk.Menu()
                language_menu_item.set_submenu(language_menu)
            else:
                language_menu = language_menu_item.get_submenu()

            framework_menu_item = self.__get_child_by_name(language_menu, block.framework)
            if framework_menu_item is None:
                framework_menu_item = Gtk.MenuItem(block.framework)
                framework_menu_item.set_name(block.framework)
                language_menu.append(framework_menu_item)
                framework_menu = Gtk.Menu()
                framework_menu_item.set_submenu(framework_menu)
            else:
                framework_menu = framework_menu_item.get_submenu()

            group_menu_item = self.__get_child_by_name(framework_menu, block.group)
            if group_menu_item is None:
                group_menu_item = Gtk.MenuItem(block.group)
                group_menu_item.set_name(block.group)
                framework_menu.append(group_menu_item)
                group_menu = Gtk.Menu()
                group_menu_item.set_submenu(group_menu)
            else:
                group_menu = group_menu_item.get_submenu()

            menu_item = Gtk.MenuItem(block.type)
            group_menu.append(menu_item)
            menu_item.connect("activate", self.__add_block, block)

        self.block_menu.show_all()

    # ----------------------------------------------------------------------
    def __add_block(self, widget, data):
        """
        This method load a example.

            Parameters:
                widget:
                data:

        """
        self.main_window.main_control.add_block(data)

    # ----------------------------------------------------------------------
    def update_examples(self, list_of_examples):

        for widget in self.example_menu.get_children():
            self.example_menu.remove(widget)
        for example in list_of_examples:
            menu_item = Gtk.MenuItem(example.split("/").pop())
            self.example_menu.append(menu_item)
            menu_item.connect("activate", self.__load_example, example)
        self.example_menu.show_all()

    # ----------------------------------------------------------------------
    def __load_example(self, widget, data):
        """
        This method load a example.

            Parameters:
                widget:
                data:

        """
        self.main_window.main_control.open(data)


    # ----------------------------------------------------------------------
    def update_recent_files(self, list_of_recent_files):
        """
        This method update recent files.
        """

        for widget in self.recent_files_menu.get_children():
            self.recent_files_menu.remove(widget)

        for recent_file in list_of_recent_files:
            menu_item = Gtk.MenuItem(recent_file)
            self.recent_files_menu.append(menu_item)
            menu_item.connect("activate", self.__load_recent, None)
        self.recent_files_menu.show_all()
