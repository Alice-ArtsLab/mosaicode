#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from harpia.constants import *
from harpia.GUI.dialog import Dialog
from harpia.GUI.about import About
from harpia.GUI.diagram import Diagram
from harpia.GUI.codewindow import CodeWindow
from harpia.GUI.preferencewindow import PreferenceWindow
from harpia.control.diagramcontrol import DiagramControl
from harpia.control.codegenerator import CodeGenerator

from harpia.s2idirectory import *

import os

class MainControl():

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        self.main_window = main_window
        # It must be possible to exchange data between diagrams
        self.clipboard = [] 

    # ----------------------------------------------------------------------
    def new(self):
        self.main_window.work_area.add_diagram(Diagram(self.main_window))

    # ----------------------------------------------------------------------
    def select_open(self):
        file_name = Dialog().open_dialog("Open Diagram", self.main_window)
        if file_name == None or file_name == "":
            return
        self.open(file_name)

    # ----------------------------------------------------------------------
    def open(self, file_name):
        diagram = Diagram(self.main_window)
        self.main_window.work_area.add_diagram(diagram)
        DiagramControl(diagram).load(file_name)
        diagram.set_modified(False)
        harpia.s2idirectory.properties.add_recent_file(file_name)
        self.main_window.menu.update_recent_file()

    # ----------------------------------------------------------------------
    def close(self):
        self.main_window.work_area.close_tab()

    # ----------------------------------------------------------------------
    def save(self, save_as = False):

        diagram = self.main_window.work_area.get_current_diagram()
        if diagram == None:
            return

        if diagram.get_file_name() is "Untitled" or save_as:
            while True:
                name = Dialog().save_dialog("Save", self.main_window)
                if name and not name.endswith("hrp"):
                    name=(("%s"+".hrp")%name)
                if Dialog().confirm_overwrite(name, self.main_window):
                    diagram.set_file_name(name)
                    break
        result, message = False,""

        if diagram.get_file_name() is not None:
            if len(diagram.get_file_name()) > 0:
                result, message = DiagramControl(diagram).save()

        if not result:
            Dialog().message_dialog("Error", message, self.main_window)

    # ----------------------------------------------------------------------
    def save_as(self):
        self.save(save_as = True)

    # ----------------------------------------------------------------------
    def export_diagram(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram == None:
            return

        while True:
            name = Dialog().save_png_dialog("Export Diagram...", self.main_window)
            if name == None:
                return
            if name.find(".png") == -1:
                name = name + ".png"
            if Dialog().confirm_overwrite(name, self.main_window):
                break

        result, message = DiagramControl(diagram).export_png(name)

        if not result:
            Dialog().message_dialog("Error", message, self.main_window)

    # ----------------------------------------------------------------------
    def exit(self, widget = None, data = None):
        if self.main_window.work_area.close_tabs():
            Gtk.main_quit()
        else:
            return True

    # ----------------------------------------------------------------------
    def select_all(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram == None:
            return
        diagram.select_all()
        diagram.grab_focus()

    # ----------------------------------------------------------------------
    def cut(self):
        if self.main_window.work_area.get_current_diagram() == None:
            return
        self.main_window.work_area.get_current_diagram().cut()

    # ----------------------------------------------------------------------
    def copy(self):
        if self.main_window.work_area.get_current_diagram() == None:
            return
        self.main_window.work_area.get_current_diagram().copy()

    # ----------------------------------------------------------------------
    def paste(self):
        if self.main_window.work_area.get_current_diagram() == None:
            return
        self.main_window.work_area.get_current_diagram().paste()

    # ----------------------------------------------------------------------
    def get_clipboard(self):
        return self.clipboard

    # ----------------------------------------------------------------------
    def reset_clipboard(self):
        self.clipboard = []

    # ----------------------------------------------------------------------
    def preferences(self):
        PreferenceWindow(self.main_window, harpia.s2idirectory.properties)


    # ----------------------------------------------------------------------
    def delete(self):
        if self.main_window.work_area.get_current_diagram() == None:
            return
        self.main_window.work_area.get_current_diagram().delete()

    # ----------------------------------------------------------------------
    def run(self):
        if self.main_window.work_area.get_current_diagram() == None:
            return
        diagram = self.main_window.work_area.get_current_diagram()
        CodeGenerator(diagram).execute_code()

    # ----------------------------------------------------------------------
    def save_source(self):
        if self.main_window.work_area.get_current_diagram() == None:
            return
        diagram = self.main_window.work_area.get_current_diagram()
        CodeGenerator(diagram).save_code()

    # ----------------------------------------------------------------------
    def view_source(self):
        if self.main_window.work_area.get_current_diagram() == None:
            return
        diagram = self.main_window.work_area.get_current_diagram()
        code = CodeGenerator(diagram).generate_code()
        CodeWindow(self.main_window, code)

    # ----------------------------------------------------------------------
    def about(self):
        About(self.main_window).show_all()

    # ----------------------------------------------------------------------
    def search(self, query):
        self.main_window.blocks_tree_view.search(query)

    # ----------------------------------------------------------------------
    def set_block(self, block):
        self.main_window.block_properties.set_block(block)
        pass

    # ----------------------------------------------------------------------
    def append_status_log(self, text):
        self.main_window.status.append_text(text)

    # ----------------------------------------------------------------------
    def add_block(self, block):
        if self.main_window.work_area.get_current_diagram() == None:
            return
        self.main_window.work_area.get_current_diagram().insert_block(block)

    # ----------------------------------------------------------------------
    def get_selected_block(self):
        return self.main_window.blocks_tree_view.get_selected_block()

    # ----------------------------------------------------------------------
    def zoom_in(self):
        if self.main_window.work_area.get_current_diagram() == None:
            return
        self.main_window.work_area.get_current_diagram().change_zoom(ZOOM_IN)

    # ----------------------------------------------------------------------
    def zoom_out(self):
        if self.main_window.work_area.get_current_diagram() == None:
            return
        self.main_window.work_area.get_current_diagram().change_zoom(ZOOM_OUT)

    # ----------------------------------------------------------------------
    def zoom_normal(self):
        if self.main_window.work_area.get_current_diagram() == None:
            return
        self.main_window.work_area.get_current_diagram().change_zoom(ZOOM_ORIGINAL)

    # ----------------------------------------------------------------------
    def show_block_property(self, block):
        self.main_window.block_properties.set_block(block)

    # ----------------------------------------------------------------------
    def clear_console(self):
        self.main_window.status.clear()

    # ----------------------------------------------------------------------
    def undo(self):
        if self.main_window.work_area.get_current_diagram() == None:
            return
        self.main_window.work_area.get_current_diagram().undo()

    # ----------------------------------------------------------------------
    def redo(self):
        if self.main_window.work_area.get_current_diagram() == None:
            return
        self.main_window.work_area.get_current_diagram().redo()

    # ----------------------------------------------------------------------
    def reload(self):
        if self.main_window.work_area.get_current_diagram() == None:
            return
        self.main_window.work_area.get_current_diagram().update_scrolling()

# ----------------------------------------------------------------------
