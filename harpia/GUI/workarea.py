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
        self.diagrams = []

    # ----------------------------------------------------------------------
    def add_diagram(self, diagram):
        frame = Gtk.ScrolledWindow()
        frame.set_shadow_type(Gtk.ShadowType.IN)
        frame.add(diagram)
        name = diagram.get_file_name()
        index = self.append_page(frame, self.__create_tab_label(name, frame))
        self.show_all()
        self.diagrams.append(diagram)
        self.set_current_page(self.get_n_pages() - 1)

    # ----------------------------------------------------------------------
    def close_tab(self, position=None):
        if position == None:
            position = self.get_current_page()
        self.remove_page(position)
        self.diagrams.pop(position)

    # ----------------------------------------------------------------------
    def __create_tab_label(self, text, frame):
        box = Gtk.HBox()
        button = Gtk.Button()
        image = Gtk.Image().new_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
        button.set_image(image)
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.connect('clicked', self.__on_close_button_clicked, frame)
        label = Gtk.Label(text)
        box.add(label)
        box.add(button)
        box.show_all()
        return box

    # ----------------------------------------------------------------------
    def __on_close_button_clicked(self, widget, frame):
        index = -1
        for tab in self.get_children():
            index += 1
            if tab == frame:
                break
        self.close_tab(index)

    # ----------------------------------------------------------------------
    def get_current_diagram(self):
        if self.get_current_page() > -1:
            return self.diagrams[self.get_current_page()]
        else:
            return None

    # ----------------------------------------------------------------------
    def rename_diagram(self, diagram):
        index = -1
        for tab in self.get_children():
            index += 1
            if tab.get_children()[0] == diagram:
                break
        tab = self.get_nth_page(index)
        if tab == None:
            return
        hbox = self.get_tab_label(tab)
        label = hbox.get_children()[0]
        label.set_text(diagram.get_file_name())

    # ----------------------------------------------------------------------
    def resize(self, data):
        for diagram in self.diagrams:
            diagram.resize(data)
# ----------------------------------------------------------------------            
