#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the BlocksTreeView class.
"""
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from harpia.system import System as System
import gettext
_ = gettext.gettext


class BlocksTreeView(Gtk.ScrolledWindow):
    """
    This class contains the methods related to BlocksTreeView class.
    """

    def __init__(self, main_window, language):
        """
        This method is the constructor.
        """
        Gtk.ScrolledWindow.__init__(self)
        self.main_window = main_window
        self.current_filter = None

        self.tree_store = Gtk.TreeStore(str, str, str, str)
        self.filter = self.tree_store.filter_new()
        self.filter.set_visible_func(self.__filter_func)
        self.blocks_tree_view = Gtk.TreeView.new_with_model(self.filter)
        self.add(self.blocks_tree_view)

        col = Gtk.TreeViewColumn(_("Available Blocks"))
        self.blocks_tree_view.append_column(col)

        cellrenderertext = Gtk.CellRendererText()
        col.pack_start(cellrenderertext, False)
        cellrenderertext.set_property('background-set' , True)
        cellrenderertext.set_property('foreground-set' , True)
        col.add_attribute(cellrenderertext, "text", 0)
        col.set_attributes(cellrenderertext, text=0, foreground=2, background=3)

        cellrenderertext = Gtk.CellRendererText()
        col.pack_end(cellrenderertext, True)
        col.add_attribute(cellrenderertext, "text", 1)

        self.blocks_tree_view.set_enable_search(False)
        self.blocks_tree_view.connect("row-activated", self.__on_row_activated)
        self.blocks_tree_view.connect("cursor-changed",
                    self.__on_tree_selection_changed)

        self.blocks_tree_view.enable_model_drag_source(
            Gdk.ModifierType.BUTTON1_MASK,
            [('text/plain', Gtk.TargetFlags.SAME_APP, 1)],
            Gdk.DragAction.DEFAULT | Gdk.DragAction.COPY)
        self.blocks_tree_view.connect("drag-data-get", self.__drag_data)
        self.blocks = {}

        # Load blocks
        for x in System.plugins:
            instance = System.plugins[x]()
            name = instance.language
            name += "/" + instance.framework
            if name != language:
                continue
            self.blocks[x] = System.plugins[x]
            self.__add_item(System.plugins[x]())

    # ----------------------------------------------------------------------
    def __add_item(self, block):
        """
        This method add a block in blockstreeview.

            Parameters:
                * **block**

        """
        category = self.__contains_category(block.get_group())
        self.tree_store.append(category,
                        [block.get_label().title()[0],
                        block.get_label(),
                        "white",
                        block.get_color_as_rgba()
                        ])

    # ----------------------------------------------------------------------
    def __contains_category(self, category_name):
        """
        This method verify if category name already exists.
        """
        iter = self.tree_store.get_iter_first()
        while iter is not None:
            if category_name in self.tree_store[iter][:]:
                return iter
            iter = self.tree_store.iter_next(iter)
        return self.tree_store.append(None, [None, str(category_name),
                    "white",
                    "white"])

    # ----------------------------------------------------------------------
    def __filter_func(self, model, iter, data):
        """
        This methods filters the functions.
        """
        if self.current_filter is None:
            return True
        if self.current_filter == "None":
            return True
        if self.current_filter == "":
            return True
        if self.tree_store.iter_children(iter) is not None:
            return True
        return self.current_filter in model[iter][1].upper()

    # ----------------------------------------------------------------------
    def __on_tree_selection_changed(self, treeview):
        """
        This method monitors if tree selection was changed.
        """
        treeViewSelection = self.blocks_tree_view.get_selection()
        (tree_view_model, iter) = treeViewSelection.get_selected()

        # If it is a category, give up
        if tree_view_model.iter_has_child(iter):
            return

        block = self.get_selected_block()
        if block is not None:
            self.main_window.main_control.set_block(self.get_selected_block())

    # ----------------------------------------------------------------------
    def search(self, key):
        """
        This method search the key in blocks_tree_view.

            Parameters:
                * **key** (:class:`str<str>`)
        """
        self.blocks_tree_view.expand_all()
        self.current_filter = key
        self.filter.refilter()

    # ----------------------------------------------------------------------
    def __on_row_activated(self, tree_view, path, column):
        block = self.get_selected_block()
        if block is not None:
            self.main_window.main_control.add_block(block)

    # ----------------------------------------------------------------------
    def __drag_data(self, treeview, context, selection, target_id, etime):
        """
        This method drag the a selection data.
        """
        block = self.get_selected_block()
        if block is not None:
            selection.set_text(block.get_label(), -1)

    # ----------------------------------------------------------------------
    def get_selected_block(self):
        """
        This method get the block selected.

            Returns:
                * **Types** (:class:`<>`) or None
        """
        treeselection = self.blocks_tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        path = model.get_path(iterac)
        block_name = model.get_value(
            model.get_iter(path), 1)  # 1 is the name position
        for x in self.blocks:         # 0 is the icon
            block = self.blocks[x]()
            if block.get_label() == block_name:
                return block
        return None
# ----------------------------------------------------------------------
