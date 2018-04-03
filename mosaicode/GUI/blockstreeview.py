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
import gettext
_ = gettext.gettext


class BlocksTreeView(Gtk.ScrolledWindow):
    """
    This class contains the methods related to BlocksTreeView class.
    """

    def __init__(self, main_window, language, blocks):
        """
        This method is the constructor.
        """
        Gtk.ScrolledWindow.__init__(self)
        self.main_window = main_window
        self.current_filter = None

        self.tree_store = Gtk.TreeStore(str, str, str, str, object)
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

        # To separate blocks of this language
        block_list = []
        group_list = []
        for x in blocks:
            instance = blocks[x]
            name = instance.language
            name += "/" + instance.framework
            if name != language:
                continue
            block_list.append(x)
            if blocks[x].group not in group_list:
                group_list.append(blocks[x].group)

        # Sorting groups
        for group in sorted(group_list):
            self.__append_category(group)

        for x in sorted(block_list):
            self.__add_item(blocks[x])


    # ----------------------------------------------------------------------
    def __add_item(self, block):
        """
        This method add a block in blockstreeview.

            Parameters:
                * **block**

        """
        category = self.__contains_category(block.group)
        self.tree_store.append(category,
                        [block.label.title()[0],
                        block.label,
                        "white",
                        block.get_color_as_rgba(),
                        block
                        ])

    # ----------------------------------------------------------------------
    def __append_category(self, category_name):
        return self.tree_store.append(None, [None, str(category_name),
                    "white",
                    "white",
                    None])

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
        return __append_category(category_name)

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
            selection.set_text(block.label, -1)

    # ----------------------------------------------------------------------
    def get_selected_block(self):
        """
        This method get the block selected.

            Returns:
                * **Types** (:class:`<>`) or None
        """
        treeselection = self.blocks_tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        if iterac is None:
            return None
        path = model.get_path(iterac)
        block = model.get_value(model.get_iter(path), 4)
        return block
# ----------------------------------------------------------------------
