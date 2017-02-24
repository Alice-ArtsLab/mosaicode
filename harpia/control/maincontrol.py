#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the MainControl class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from harpia.GUI.dialog import Dialog
from harpia.GUI.about import About
from harpia.GUI.diagram import Diagram
from harpia.GUI.codewindow import CodeWindow
from harpia.GUI.pluginmanager import PluginManager
from harpia.GUI.portmanager import PortManager
from harpia.GUI.preferencewindow import PreferenceWindow
from harpia.control.diagramcontrol import DiagramControl
from harpia.system import System as System
from harpia.control.preferencescontrol import PreferencesControl


class MainControl():
    """
    This class contains methods related the MainControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        self.main_window = main_window
        # It must be possible to exchange data between diagrams
        self.clipboard = []

    # ----------------------------------------------------------------------
    def new(self):
        """
        This method create a new the diagram file.
        """
        self.main_window.work_area.add_diagram(Diagram(self.main_window))

    # ----------------------------------------------------------------------
    def select_open(self):
        """
        This method open a selected file.
        """
        file_name = Dialog().open_dialog("Open Diagram", self.main_window)
        if file_name is None or file_name == "":
            return
        self.open(file_name)

    # ----------------------------------------------------------------------
    def open(self, file_name):
        """
        This method open a file.
        """
        diagram = Diagram(self.main_window)
        self.main_window.work_area.add_diagram(diagram)
        DiagramControl(diagram).load(file_name)
        diagram.set_modified(False)
        System.properties.add_recent_file(file_name)
        self.main_window.menu.update_recent_file()

    # ----------------------------------------------------------------------
    def close(self):
        """
        This method closes a tab on the work area.
        """
        self.main_window.work_area.close_tab()

    # ----------------------------------------------------------------------
    def save(self, save_as=False):
        """
        This method save the file.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return

        if diagram.get_file_name() is "Untitled" or save_as:
            while True:
                name = Dialog().save_dialog("Save", self.main_window)
                if name and not name.endswith("hrp"):
                    name = (("%s" + ".hrp") % name)
                if Dialog().confirm_overwrite(name, self.main_window):
                    diagram.set_file_name(name)
                    break
        result, message = False, ""

        if diagram.get_file_name() is not None:
            if len(diagram.get_file_name()) > 0:
                result, message = DiagramControl(diagram).save()

        if not result:
            Dialog().message_dialog("Error", message, self.main_window)

    # ----------------------------------------------------------------------
    def save_as(self):
        """
        This method save as.
        """
        self.save(save_as=True)

    # ----------------------------------------------------------------------
    def rename_tab(self):
        """
        This method rename a tab.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        Dialog().rename_dialog(self.main_window, diagram)

    # ----------------------------------------------------------------------
    def export_diagram(self):
        """
        This method exports the diagram.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return

        while True:
            name = Dialog().save_png_dialog("Export Diagram...",
                                            self.main_window)
            if name is None:
                return
            if name.find(".png") == -1:
                name = name + ".png"
            if Dialog().confirm_overwrite(name, self.main_window):
                break

        result, message = DiagramControl(diagram).export_png(name)

        if not result:
            Dialog().message_dialog("Error", message, self.main_window)

    # ----------------------------------------------------------------------
    def exit(self, widget=None, data=None):
        """
        This method close main window.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        PreferencesControl(System.properties).save()
        if self.main_window.work_area.close_tabs():
            Gtk.main_quit()
        else:
            return True

    # ----------------------------------------------------------------------
    def select_all(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        diagram.select_all()
        diagram.grab_focus()

    # ----------------------------------------------------------------------
    def cut(self):
        """
        This method cut a block on work area.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        diagram.cut()

    # ----------------------------------------------------------------------
    def copy(self):
        """
        This method copy a block.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        diagram.copy()

    # ----------------------------------------------------------------------
    def paste(self):
        """
        This method paste a block.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        diagram.paste()

    # ----------------------------------------------------------------------
    def get_clipboard(self):
        """
        This method return the clipboard.
        """
        return self.clipboard

    # ----------------------------------------------------------------------
    def reset_clipboard(self):
        """
        This method clear the clipboard.
        """
        self.clipboard = []

    # ----------------------------------------------------------------------
    def preferences(self):
        """
        """
        PreferenceWindow(self.main_window)

    # ----------------------------------------------------------------------
    def delete(self):
        """
        This method delete a block.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        diagram.delete()

    # ----------------------------------------------------------------------
    def run(self):
        """
        This method run the code.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        DiagramControl(diagram).get_generator().execute()

    # ----------------------------------------------------------------------
    def save_source(self):
        """
        This metho save the source code.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        DiagramControl(diagram).get_generator().save_code()

    # ----------------------------------------------------------------------
    def view_source(self):
        """
        This method view the source code.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        code = DiagramControl(diagram).get_generator().generate_code()
        CodeWindow(self.main_window, code)

    # ----------------------------------------------------------------------
    def about(self):
        """
        This method open the about window.
        """
        About(self.main_window).show_all()

    # ----------------------------------------------------------------------
    def search(self, query):
        """
        This method search the query in the blocks_tree_view.
        """
        for blocks_tree_view in self.main_window.block_notebook.get_tabs():
            blocks_tree_view.search(query)

    # ----------------------------------------------------------------------
    def set_block(self, block):
        """
        This method set the block properties.
        """
        self.main_window.block_properties.set_block(block)

    # ----------------------------------------------------------------------
    def append_status_log(self, text):
        """
        This method append a text on status log.
        """
        self.main_window.status.append_text(text)

    # ----------------------------------------------------------------------
    def add_block(self, block):
        """
        This method add a block.

        Parameters:

                * **Types** (:class:`block<>`)
        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        if not diagram.add_block(block):
            message = "Block language is different from diagram language.\n" +\
                "Diagram is expecting to generate " + diagram.language + \
                " code while block is writen in " + block.language
            Dialog().message_dialog("Error", message, self.main_window)
            return False
        return True

    # ----------------------------------------------------------------------
    def get_selected_block(self):
        """
        This method get the tree view block.
        """
        blocks_tree_view = self.main_window.block_notebook.get_current_tab()
        if blocks_tree_view is None:
            return False
        return blocks_tree_view.get_selected_block()

    # ----------------------------------------------------------------------
    def zoom_in(self):
        """
        This method increases the zoom value.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        diagram.change_zoom(System.ZOOM_IN)

    # ----------------------------------------------------------------------
    def zoom_out(self):
        """
        This method decreasses the zoom.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        diagram.change_zoom(System.ZOOM_OUT)

    # ----------------------------------------------------------------------
    def zoom_normal(self):
        """
        Set the zoom value to normal.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        diagram.change_zoom(System.ZOOM_ORIGINAL)

    # ----------------------------------------------------------------------
    def show_block_property(self, block):
        """
        This method show the block properties.
        """
        self.main_window.block_properties.set_block(block)

    # ----------------------------------------------------------------------
    def clear_console(self):
        """
        This method clear the console.
        """
        self.main_window.status.clear()

    # ----------------------------------------------------------------------
    def undo(self):
        """
        Undo a modification.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        diagram.undo()

    # ----------------------------------------------------------------------
    def redo(self):
        """
        Redo a modification.
        """
        if self.main_window.work_area.get_current_diagram() is None:
            return
        self.main_window.work_area.get_current_diagram().redo()

    # ----------------------------------------------------------------------
    def reload(self):
        """
        Reload the diagram.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        diagram.update_scrolling()

    # ----------------------------------------------------------------------
    def new_plugin(self):
        """
        This add a new plugin.
        """
        PluginManager(self.main_window)

    # ----------------------------------------------------------------------
    def new_port(self):
        """
        This add a new port.
        """
        PortManager(self.main_window)

    # ----------------------------------------------------------------------
    def align_top(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False

        diagram.align_top()
    # ----------------------------------------------------------------------
    def align_bottom(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False

        diagram.align_bottom()

    # ----------------------------------------------------------------------
    def align_left(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False

        diagram.align_left()

    # ----------------------------------------------------------------------
    def align_right(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False

        diagram.align_right()

    # ----------------------------------------------------------------------
    def redraw(self, show_grid):
        diagrams = self.main_window.work_area.get_diagrams()

        for diagram in diagrams:
            diagram.set_show_grid(show_grid)
            diagram.redraw()

    # ----------------------------------------------------------------------
    def show_grid(self, event):
        self.redraw(event.get_active())

    # ----------------------------------------------------------------------
    def add_port(self, port):
        System.connectors.update(port)

    # ----------------------------------------------------------------------
    def delete_port(self, port_key):
        System.connectors.pop(port_key, None)
# ----------------------------------------------------------------------
