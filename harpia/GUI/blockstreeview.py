#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

from harpia import s2idirectory

class BlocksTreeView(Gtk.ScrolledWindow):

    def __init__(self, main_window):
        Gtk.ScrolledWindow.__init__(self)
        self.main_window = main_window
        self.current_filter = None

        self.tree_store = Gtk.TreeStore(str)
        self.filter = self.tree_store.filter_new()
        self.filter.set_visible_func(self.__filter_func)
        self.blocks_tree_view = Gtk.TreeView.new_with_model(self.filter)
        self.add(self.blocks_tree_view)

        view = Gtk.TreeViewColumn("Available BLocks")
        self.blocks_tree_view.append_column(view)
        cellrenderertext = Gtk.CellRendererText()
        view.pack_start(cellrenderertext, True)
        view.add_attribute(cellrenderertext, "text", 0)

        self.blocks_tree_view.set_enable_search(False)
        self.blocks_tree_view.connect("row-activated", self.__on_row_activated)
        self.blocks_tree_view.connect("cursor-changed", self.__on_tree_selection_changed)

        self.blocks_tree_view.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK,
                                                                [('text/plain', Gtk.TargetFlags.SAME_APP, 1)],
                                                                Gdk.DragAction.DEFAULT |
                                                                Gdk.DragAction.COPY)
        self.blocks_tree_view.connect("drag-data-get", self.__drag_data)
        self.blocks = {}

        # Load blocks
        for x in s2idirectory.block:
            block = s2idirectory.block[x]()
            self.__add_item(block.get_description()["Label"], block.get_description()["TreeGroup"])
            self.blocks[id] = s2idirectory.block[x]

    # ----------------------------------------------------------------------
    def __add_item(self, item, category_name):
        category = self.__contains_category(category_name)
        self.tree_store.append(category, [item])

    # ----------------------------------------------------------------------
    def __contains_category(self, category_name):
        iter = self.tree_store.get_iter_first()
        while iter != None:
            if category_name in self.tree_store[iter][:] :
                return iter
            iter = self.tree_store.iter_next(iter)
        return self.tree_store.append(None, [category_name])

    # ----------------------------------------------------------------------
    def __filter_func(self, model, iter, data):
        if self.current_filter is None:
            return True
        if self.current_filter == "None":
            return True
        if self.current_filter == "":
            return True
        if self.tree_store.iter_children(iter) != None :
            return True
        return self.current_filter in model[iter][0]

    # ----------------------------------------------------------------------
    def __on_tree_selection_changed(self, treeview):
        treeViewSelection = self.blocks_tree_view.get_selection()
        (tree_view_model, iter) = treeViewSelection.get_selected()

        # If it is a category, give up
        if tree_view_model.iter_has_child(iter) :
            return

        block = self.get_selected_block()
        if block != None:
            self.main_window.main_control.set_block(self.get_selected_block())

    # ----------------------------------------------------------------------
    def search(self, key):
        self.blocks_tree_view.expand_all()
        self.current_filter = key
        self.filter.refilter()

    # ----------------------------------------------------------------------
    def __on_row_activated(self, tree_view, path, column):
        tree_view_model = tree_view.get_model()
        block_name = tree_view_model.get_value(tree_view_model.get_iter(path), 0)
        block = self.get_selected_block()
        if block != None:
            self.main_window.main_control.add_block(block)

    # ----------------------------------------------------------------------
    def __drag_data(self, treeview, context, selection, target_id, etime):
        block = self.get_selected_block()
        selection.set_text(block.get_description()["Label"], -1)
        return

    # ----------------------------------------------------------------------
    def get_selected_block(self):
        treeselection = self.blocks_tree_view.get_selection()
        model, iterac = treeselection.get_selected()
        path = model.get_path(iterac)
        block_name = model.get_value(model.get_iter(path), 0)
        for x in self.blocks:
            block = self.blocks[x]()
            if block.get_description()["Label"] == block_name:
                return block
        return None
# ----------------------------------------------------------------------
