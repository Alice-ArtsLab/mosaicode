#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the BlocksTreeView class.
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
        Gtk.ScrolledWindow.__init__(self)
        self.main_window = main_window
        self.current_filter = None

        self.tree_store = Gtk.TreeStore(GdkPixbuf.Pixbuf, str)
        self.filter = self.tree_store.filter_new()
        self.filter.set_visible_func(self.__filter_func)
        self.blocks_tree_view = Gtk.TreeView.new_with_model(self.filter)
        self.add(self.blocks_tree_view)

        col = Gtk.TreeViewColumn(_("Available Blocks"))
        self.blocks_tree_view.append_column(col)

        cellrenderimage = Gtk.CellRendererPixbuf()
        col.pack_start(cellrenderimage, False)
        col.add_attribute(cellrenderimage, "pixbuf", 0)

        cellrenderertext = Gtk.CellRendererText()
        col.pack_end(cellrenderertext, True)
        col.add_attribute(cellrenderertext, "text", 1)

        self.blocks_tree_view.set_enable_search(False)
        self.blocks_tree_view.connect("row-activated", self.__on_row_activated)
        self.blocks_tree_view.connect(
            "cursor-changed", self.__on_tree_selection_changed)

        self.blocks_tree_view.enable_model_drag_source(
            Gdk.ModifierType.BUTTON1_MASK,
            [('text/plain', Gtk.TargetFlags.SAME_APP, 1)],
            Gdk.DragAction.DEFAULT | Gdk.DragAction.COPY)
        self.blocks_tree_view.connect("drag-data-get", self.__drag_data)
        self.blocks = {}

        # Load blocks
        for x in System.blocks:
            name = System.blocks[x].language
            name += "/" + System.blocks[x].framework
            if name != language:
                continue
            self.blocks[x] = System.blocks[x]
            self.__add_item(System.blocks[x]())

    # ----------------------------------------------------------------------
    def __add_item(self, block):
        """
        This method add a block in blockstreeview.
        Args:
        Returns:
            None
        """
        category = self.__contains_category(block.get_group())
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(
            os.environ['HARPIA_DATA_DIR'] + block.get_icon())
        self.tree_store.append(category, [pixbuf, block.get_label()])

    # ----------------------------------------------------------------------
    def __contains_category(self, category_name):
        iter = self.tree_store.get_iter_first()
        while iter is not None:
            if category_name in self.tree_store[iter][:]:
                return iter
            iter = self.tree_store.iter_next(iter)
        return self.tree_store.append(None, [None, str(category_name)])

    # ----------------------------------------------------------------------
    def __filter_func(self, model, iter, data):
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
        self.blocks_tree_view.expand_all()
        self.current_filter = key
        self.filter.refilter()

    # ----------------------------------------------------------------------
    def __on_row_activated(self, tree_view, path, column):
        tree_view_model = tree_view.get_model()
        block_name = tree_view_model.get_value(
            tree_view_model.get_iter(path), 0)
        block = self.get_selected_block()
        if block is not None:
            self.main_window.main_control.add_block(block)

    # ----------------------------------------------------------------------
    def __drag_data(self, treeview, context, selection, target_id, etime):
        block = self.get_selected_block()
        if block is not None:
            selection.set_text(block.get_label(), -1)

    # ----------------------------------------------------------------------
    def get_selected_block(self):
        treeselection = self.blocks_tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        path = model.get_path(iterac)
        block_name = model.get_value(
            model.get_iter(path), 1)  # 1 is the name position
        for x in self.blocks:                                 # 0 is the icon
            block = self.blocks[x]()
            if block.get_label() == block_name:
                return block
        return None
# ----------------------------------------------------------------------
