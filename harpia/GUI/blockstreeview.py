#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

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
        self.blocks_tree_view.connect("cursor-changed", self.__on_tree_selection_changed)
        self.blocks_tree_view.connect("row-activated", self.__on_row_activated)

        self.blocks_tree_view.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK,
                                                                [('text/plain', Gtk.TargetFlags.SAME_APP, 1)],
                                                                Gdk.DragAction.DEFAULT |
                                                                Gdk.DragAction.COPY)
        self.blocks_tree_view.connect("drag-data-get", self.__drag_data)

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

        if iter != None:
            block_name = tree_view_model.get_value(iter, 0)
            self.main_window.main_control.set_help(block_name)

    # ----------------------------------------------------------------------
    def add_item(self, item, category_name):
        category = self.__contains_category(category_name)
        self.tree_store.append(category, [item])

    # ----------------------------------------------------------------------
    def search(self, key):
        self.blocks_tree_view.expand_all()
        self.current_filter = key
        self.filter.refilter()

    # ----------------------------------------------------------------------
    def __on_row_activated(self, tree_view, path, column):
        print "Selection"


    def __drag_data(self, treeview, context, selection, target_id, etime):
        treeselection = treeview.get_selection()
        model, iterac = treeselection.get_selected()
        self.tree_view_path = model.get_path(iterac)
        selection.set('text/plain', 8, "test")
        return    
# ----------------------------------------------------------------------
