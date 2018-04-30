# -*- coding: utf-8 -*-
"""
This module contains the MainControl class.
"""
from copy import copy
from copy import deepcopy
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.GUI.dialog import Dialog
from mosaicode.GUI.about import About
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.block import Block
from mosaicode.GUI.comment import Comment
from mosaicode.GUI.codewindow import CodeWindow
from mosaicode.GUI.preferencewindow import PreferenceWindow
from mosaicode.GUI.selectcodetemplate import SelectCodeTemplate
from mosaicode.system import System as System
from mosaicode.persistence.preferencespersistence import PreferencesPersistence
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.control.portcontrol import PortControl
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.control.codetemplatecontrol import CodeTemplateControl
from mosaicode.control.codegenerator import CodeGenerator
from mosaicode.control.publisher import Publisher
from mosaicode.model.codetemplate import CodeTemplate


import gettext
_ = gettext.gettext


class MainControl():
    """
    This class contains methods related the MainControl class.
    """
    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        self.main_window = main_window
        # Clipboard is here because It must be possible to exchange data between diagrams
        self.clipboard = []
        self.publisher = Publisher()

    # ----------------------------------------------------------------------
    def init(self):
        self.main_window.menu.update_recent_files(System.properties.recent_files)
        self.main_window.menu.update_examples(System.list_of_examples)
        self.update_blocks()

    # ----------------------------------------------------------------------
    def update_blocks(self):
        System.reload()
        blocks = System.get_blocks()
        self.main_window.menu.update_blocks(blocks)
        self.main_window.block_notebook.update_blocks(blocks)

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
                        filetype="mscd")
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
        diagram.redraw()
        diagram.set_modified(False)

        if file_name in System.properties.recent_files:
            System.properties.recent_files.remove(file_name)
        System.properties.recent_files.insert(0, file_name)
        if len(System.properties.recent_files) > 10:
            System.properties.recent_files.pop()
        self.main_window.menu.update_recent_files(System.properties.recent_files)

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
                        filetype = "mscd")
                if name and not name.endswith("mscd"):
                    name = (("%s" + ".mscd") % name)
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
        PreferencesPersistence.save(System.properties, System.get_user_dir())
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
        PreferenceWindow(self.main_window).run()

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
    def __get_code_generator(self, diagram):

        if diagram.language is None:
            message = "You shall not generate code of an empty diagram!"
            Dialog().message_dialog("Error", message, self.main_window)
            return None

        template_list = []
        code_templates = System.get_code_templates()

        for key in code_templates:
            if code_templates[key].language == diagram.language:
                template_list.append(code_templates[key])

        if len(template_list) == 0:
            message = "Generator not available for the language " + diagram.language + "."
            Dialog().message_dialog("Error", message, self.main_window)
            return None

        if len(template_list) == 1:
            return CodeGenerator(diagram, template_list[0])
        select = SelectCodeTemplate(self.main_window, template_list)
        code_template = select.get_value()
        return CodeGenerator(diagram, code_template)

    # ----------------------------------------------------------------------
    def run(self, code = None):
        """
        This method runs the code.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        generator = self.__get_code_generator(diagram)
        if generator is not None:
            generator.run(code = code)


    # ----------------------------------------------------------------------
    def publish(self):
        """
        This method run web server.
        """
        if self.publisher.is_running():
            self.publisher.stop()
        else:
            self.publisher.start()


    # ----------------------------------------------------------------------
    def save_source(self, code = None):
        """
        This method saves the source code.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return

        generator = self.__get_code_generator(diagram)
        if generator is None:
            return

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
        generator = self.__get_code_generator(diagram)
        if generator is not None:
            code = generator.generate_code()
            cw = CodeWindow(self.main_window, code)
	    cw.run()
            cw.close()
            cw.destroy()
	    

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
        new_block = Block(diagram, deepcopy(block))
        if not DiagramControl.add_block(diagram, new_block):
            message = "Block language is different from diagram language.\n" +\
                "Diagram is expecting to generate " + diagram.language + \
                " code while block is writen in " + block.language
            Dialog().message_dialog("Error", message, self.main_window)
            return False
        diagram.redraw()
        return True

    # ----------------------------------------------------------------------
    def add_comment(self):
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
        comment = Comment(diagram)
        DiagramControl.add_comment(diagram, comment)
        diagram.redraw()
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
    def show_comment_property(self, comment):
        """
        This method show the comment properties.
        """
        self.main_window.block_properties.set_comment(comment)

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
        diagram.align("TOP")

    # ----------------------------------------------------------------------
    def align_bottom(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        diagram.align("BOTTOM")

    # ----------------------------------------------------------------------
    def align_left(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        diagram.align("LEFT")

    # ----------------------------------------------------------------------
    def align_right(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        diagram.align("RIGHT")

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
    def add_code_template(self, code_template):
        CodeTemplateControl.add_code_template(code_template)
        System.reload()

    # ----------------------------------------------------------------------
    def delete_code_template(self, code_template_name):
        filename = CodeTemplateControl.delete_code_template(code_template_name)
        if filename is None:
            message = "This code template is a python file installed in the System.\n"
            message = message + "Sorry, you can't remove it"
            Dialog().message_dialog("Error", message, self.main_window)
        else:
            Dialog().message_dialog("Info", "File " + filename + " deleted.", self.main_window)
        System.reload()

    # ----------------------------------------------------------------------
    def add_port(self, port):
        PortControl.add_port(port)
        System.reload()

    # ----------------------------------------------------------------------
    def delete_port(self, port_key):
        if not PortControl.delete_port(port_key):
            message = "This port is a python file installed in the System.\n"
            message = message + "Sorry, you can't remove it"
            Dialog().message_dialog("Error", message, self.main_window)
        System.reload()

    # ----------------------------------------------------------------------
    def add_new_block(self, block):
        BlockControl.add_new_block(block)
        self.update_blocks()
        # Update everybody!

    # ----------------------------------------------------------------------
    def delete_block(self, block):
        if not BlockControl.delete_block(block):
            message = "This block is a python file installed in the System.\n"
            message = message + "Sorry, you can't remove it"
            Dialog().message_dialog("Error", message, self.main_window)
        self.update_blocks()

    # ----------------------------------------------------------------------
    def collapse_all(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        DiagramControl.collapse_all(diagram, True)

    # ----------------------------------------------------------------------
    def uncollapse_all(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return
        DiagramControl.collapse_all(diagram, False)

    # ----------------------------------------------------------------------
    def update_all(self):
        for diagram in self.main_window.work_area.get_diagrams():
            diagram.update()

    # ----------------------------------------------------------------------
    @classmethod
    def print_ports(cls):
        # This method is used by the launcher class
        ports = System.get_ports()
        for port in ports:
            print "--------------------- "
            PortControl.print_port(ports[port])
    # ----------------------------------------------------------------------
    @classmethod
    def print_blockmodels(cls):
        # This method is used by the launcher class
        blocks = System.get_blocks()
        for block in blocks:
            print "--------------------- "
            BlockControl.print_block(blocks[block])
    # ----------------------------------------------------------------------
    @classmethod
    def print_templates(cls):
        # This method is used by the launcher class
        code_templates = System.get_code_templates()
        for template in code_templates:
            print "--------------------- "
            CodeTemplateControl.print_template(code_templates[template])

# ----------------------------------------------------------------------
