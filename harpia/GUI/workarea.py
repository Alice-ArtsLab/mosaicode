#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from diagram import Diagram


class WorkArea(Gtk.Notebook):

    def __init__(self, main_window):
        Gtk.Notebook.__init__(self)
        self.main_window = main_window
        self.set_scrollable(True)

    def add_tab(self, name):
        new_diagram = Diagram(self)  # created new diagram
        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.IN)
        frame.add(new_diagram)
        self.append_page(frame, self.__create_tab_label(name, frame))
        self.show_all()

    def close_tab(self):
        position = self.get_current_page()
        self.remove_page(position)

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

    def __on_button_clicked(self, widget, args):
        position = self.page_num(args)
        self.remove_page(position)
