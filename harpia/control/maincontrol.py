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
from harpia.GUI.codetemplatemanager import CodeTemplateManager
from harpia.GUI.pluginmanager import PluginManager
from harpia.GUI.portmanager import PortManager
from harpia.GUI.preferencewindow import PreferenceWindow
from harpia.control.diagramcontrol import DiagramControl
from harpia.system import System as System
from harpia.control.preferencescontrol import PreferencesControl
from harpia.control.portcontrol import PortControl
from harpia.control.plugincontrol import PluginControl
from harpia.control.codetemplatecontrol import CodeTemplateControl
import gettext
_ = gettext.gettext


class MainControl():
    """
    This class contains methods related the MainControl class.
    """
    main_window = None
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
        file_name = Dialog().open_dialog("Open Diagram",
                        self.main_window,
                        filetype="hrp")
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
        PreferencesControl.add_recent_file(System.properties, file_name)
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

        if diagram.file_name is "Untitled" or save_as:
            while True:
                name = Dialog().save_dialog(
                        self.main_window,
                        title = _("Save Diagram"),
                        filename = diagram.file_name,
                        filetype = "hrp")
                if name and not name.endswith("hrp"):
                    name = (("%s" + ".hrp") % name)
                if Dialog().confirm_overwrite(name, self.main_window):
                    diagram.set_file_name(name)
                    break
        result, message = False, ""

        if diagram.file_name is not None:
            if len(diagram.file_name) > 0:
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
    def export_diagram(self):
        """
        This method exports the diagram.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return

        while True:
            name = Dialog().save_dialog(
                        self.main_window,
                        title = _("Export diagram as png"),
                        filename = diagram.file_name + ".png",
                        filetype = "png")

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
        PreferencesControl.save(System.properties)
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
    def run(self, code = None):
        """
        This method runs the code.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        DiagramControl(diagram).get_code_template().run(code = code)

    # ----------------------------------------------------------------------
    def save_source(self, code = None):
        """
        This method saves the source code.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return

        generator = DiagramControl(diagram).get_code_template()
        while True:
            name = Dialog().save_dialog(self.main_window,
                        filename = generator.get_dir_name() + \
                            generator.get_filename())
            if Dialog().confirm_overwrite(name, self.main_window):
                diagram.set_file_name(name)
                break

        generator.save_code(name=name, code=code)

    # ----------------------------------------------------------------------
    def view_source(self):
        """
        This method view the source code.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        code = DiagramControl(diagram).get_code_template().generate_code()
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
        self.main_window.block_notebook.search(query)

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
        return self.main_window.block_notebook.get_selected_block()

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
    def code_template_manager(self):
        """
        This add a new Code Template.
        """
        CodeTemplateManager(self.main_window)


    # ----------------------------------------------------------------------
    def plugin_manager(self):
        """
        This add a new plugin.
        """
        PluginManager(self.main_window)

    # ----------------------------------------------------------------------
    def port_manager(self):
        """
        This add a new port.
        """
        PortManager(self.main_window)

    # ----------------------------------------------------------------------
    def add_code_template(self, code_template):
        CodeTemplateControl.add_code_template(code_template)

    # ----------------------------------------------------------------------
    def delete_code_template(self, code_template_name):
        if not CodeTemplateControl.delete_code_template(code_template_name):
            message = "This code template is a python file installed in the System.\n"
            message = message + "Sorry, you can't remove it"
            Dialog().message_dialog("Error", message, self.main_window)

    # ----------------------------------------------------------------------
    def add_port(self, port):
        PortControl.add_port(port)

    # ----------------------------------------------------------------------
    def delete_port(self, port_key):
        if not PortControl.delete_port(port_key):
            message = "This port is a python file installed in the System.\n"
            message = message + "Sorry, you can't remove it"
            Dialog().message_dialog("Error", message, self.main_window)

    # ----------------------------------------------------------------------
    def add_plugin(self, plugin):
        PluginControl.add_plugin(plugin)
        self.main_window.block_notebook.update()

    # ----------------------------------------------------------------------
    def delete_plugin(self, plugin):
        if not PluginControl.delete_plugin(plugin):
            message = "This plugin is a python file installed in the System.\n"
            message = message + "Sorry, you can't remove it"
            Dialog().message_dialog("Error", message, self.main_window)
        self.main_window.block_notebook.update()

    # ----------------------------------------------------------------------
    def update_all(self):
        for diagram in self.main_window.work_area.get_diagrams():
            diagram.update()

    # ----------------------------------------------------------------------
    @classmethod
    def print_ports(cls):
        for port in System.ports:
            print "--------------------- "
            PortControl.print_port(System.ports[port])
    # ----------------------------------------------------------------------
    @classmethod
    def print_plugins(cls):
        for plugin in System.plugins:
            print "--------------------- "
            PluginControl.print_plugin(System.plugins[plugin])
    # ----------------------------------------------------------------------
    @classmethod
    def print_templates(cls):
        for template in System.code_templates:
            print "--------------------- "
            CodeTemplateControl.print_template(System.code_templates[template])

    # ----------------------------------------------------------------------
    @classmethod
    def export_extensions(cls, extension):
        if extension == 'py':
            MainControl.export_python()
        else:
            MainControl.export_xml()

    # ----------------------------------------------------------------------
    @classmethod
    def export_python(cls):
        print "Exporting extensions to Python"
        System()
        for plugin in System.plugins:
            print "Exporting plugin " + plugin
            PluginControl.save_python(System.plugins[plugin])
        for port in System.ports:
            print "Exporting port " + port
            PortControl.save_python(System.ports[port])
        for code_template in System.code_templates:
            print "Exporting code template " + code_template
            CodeTemplateControl.save_python(System.code_templates[code_template])
        print "Done!"
        Dialog().message_dialog("Exporting as python", "Exported successfully!", MainControl.main_window)

    # ----------------------------------------------------------------------
    @classmethod
    def export_xml(cls):
        print "Exporting extensions to XML"
        System()
        for plugin in System.plugins:
            print "Exporting plugin " + plugin
            PluginControl.save(System.plugins[plugin])

        for port in System.ports:
            print "Exporting port " + port
            PortControl.save(System.ports[port])

        for code_template in System.code_templates:
            print "Exporting code template " + code_template
            CodeTemplateControl.save(System.code_templates[code_template])
        print "Done!"
        Dialog().message_dialog("Exporting as xml", "Exported successfully!", MainControl.main_window)

# ----------------------------------------------------------------------
