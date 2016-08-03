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
    def add_tab(self, name):
        frame = Gtk.ScrolledWindow()
        frame.set_shadow_type(Gtk.ShadowType.IN)
        diagram = Diagram(self.main_window)  # created new diagram
        frame.add(diagram)
        self.append_page(frame, self.__create_tab_label(name, frame))
        self.show_all()
        self.diagrams.append(diagram)
        self.set_current_page(self.get_n_pages() - 1)
 
    # ----------------------------------------------------------------------
    def close_tab(self):
        position = self.get_current_page()
        self.remove_page(position)
        self.diagrams.pop(position)

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
        self.close_tab()
        
    # ----------------------------------------------------------------------
    def open_diagram(self, diagram_name):
        self.add_tab(diagram_name)
        diagram = self.diagrams[self.get_current_page()]
        diagram.set_file_name(diagram_name)
        DiagramControl(diagram).load()
        self.get_current_page()

    # ----------------------------------------------------------------------
    def get_current_diagram(self):
        if self.get_current_page() > -1:
            return self.diagrams[self.get_current_page()]
        else:
            return None

    # ----------------------------------------------------------------------
    def resize(self, data):
        for diagram in self.diagrams:
            diagram.resize(data)
# ----------------------------------------------------------------------            
