#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

from diagram import Diagram
from harpia.control.diagramcontrol import DiagramControl


class WorkArea(Gtk.Notebook):

    def __init__(self, main_window):
        Gtk.Notebook.__init__(self)
        self.main_window = main_window
        self.set_scrollable(True)
        self.diagrams = {}
        self.connect("drag_data_received", self.drag_data_received)
        self.drag_dest_set(
            Gtk.DestDefaults.MOTION | Gtk.DestDefaults.HIGHLIGHT | Gtk.DestDefaults.DROP,
            [Gtk.TargetEntry.new('text/plain', Gtk.TargetFlags.SAME_APP, 1)],
            Gdk.DragAction.DEFAULT | Gdk.DragAction.COPY)

    # ----------------------------------------------------------------------
    def add_tab(self, name):
        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.IN)
        diagram = Diagram(self)  # created new diagram
        frame.add(diagram)
        self.append_page(frame, self.__create_tab_label(name, frame))
        self.show_all()
        self.diagrams[self.get_current_page()] = diagram
 
    # ----------------------------------------------------------------------
    def close_tab(self):
        position = self.get_current_page()
        self.remove_page(position)

    # ----------------------------------------------------------------------
    def __create_tab_label(self,text, frame):
        box = Gtk.HBox()
        button = Gtk.Button()
        image = Gtk.Image().new_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
        button.set_image(image)
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.connect('clicked', self.__on_button_clicked, frame)
        label = Gtk.Label(text)
        box.add(label)
        box.add(button)
        box.show_all()
        return box

    # ----------------------------------------------------------------------
    def __on_button_clicked(self, widget, args):
        position = self.page_num(args)
        self.remove_page(position)
        
    # ----------------------------------------------------------------------
    def open_diagram(self, diagram_name):
        self.add_tab(diagram_name)
        if self.diagrams.has_key(self.get_current_page()):
            diagram = self.diagrams[self.get_current_page()]
            diagram.set_file_name(diagram_name)
            DiagramControl(diagram).load()
            self.get_current_page()

    # ----------------------------------------------------------------------
    def drag_data_received(self, widget, context, x, y, selection, targetType, time):
        self.on_BlocksTreeView_row_activated_pos(self.widgets['BlocksTreeView'], self.tree_view_path, 0, x, y)
        return

# ----------------------------------------------------------------------            
