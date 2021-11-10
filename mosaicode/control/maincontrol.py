# -*- coding: utf-8 -*-
"""
This module contains the MainControl class.
"""
import gettext
import os
import zipfile
import shutil
import signal
import subprocess
import datetime
from copy import copy, deepcopy
from threading import Event, Thread

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.control.codegenerator import CodeGenerator
from mosaicode.control.codetemplatecontrol import CodeTemplateControl
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.control.portcontrol import PortControl
from mosaicode.GUI.about import About
from mosaicode.GUI.block import Block
from mosaicode.GUI.codewindow import CodeWindow
from mosaicode.GUI.comment import Comment
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.messagedialog import MessageDialog
from mosaicode.GUI.confirmdialog import ConfirmDialog
from mosaicode.GUI.savedialog import SaveDialog
from mosaicode.GUI.opendialog import OpenDialog
from mosaicode.GUI.preferencewindow import PreferenceWindow
from mosaicode.GUI.selectcodetemplate import SelectCodeTemplate
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.model.port import Port
from mosaicode.persistence.preferencespersistence import PreferencesPersistence
from mosaicode.persistence.portpersistence import PortPersistence
from mosaicode.persistence.blockpersistence import BlockPersistence
from mosaicode.persistence.codetemplatepersistence import CodeTemplatePersistence
from mosaicode.system import System as System

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
        self.threads = {}

    # ----------------------------------------------------------------------
    def init(self):
        self.update_blocks()
        self.main_window.menu.update_recent_files(
            System.get_preferences().recent_files)
        self.main_window.menu.update_examples(System.get_examples())

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
        file_name = OpenDialog(
                                "Open Diagram",
                                self.main_window,
                                filetype="mscd",
                                path=System.get_user_dir()
                                ).run()
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
        if not DiagramControl(diagram).load(file_name):
            System.log("Problem Loading the Diagram")
        diagram.redraw()
        diagram.set_modified(False)

        self.set_recent_files(file_name)

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
            return False

        if diagram.file_name == "Untitled" or save_as:
            while True:
                dialog = SaveDialog(
                    self.main_window,
                    title=_("Save Diagram"),
                    filename=System.get_user_dir() + "/" + diagram.patch_name,
                    filetype="*.mscd")
                name = dialog.run()
                if name is None:
                    System.log("File not saved")
                    return

                if not name.endswith("mscd"):
                    name = (("%s" + ".mscd") % name)

                if os.path.exists(name) is True:
                    msg = _("File exists. Overwrite?")
                    result = ConfirmDialog(msg, self.main_window).run()
                    if result == Gtk.ResponseType.CANCEL:
                        continue

                diagram.file_name = name
                self.main_window.work_area.rename_diagram(diagram)
                break
        result, message = False, ""

        if diagram.file_name is not None:
            if len(diagram.file_name) > 0:
                result, message = DiagramControl(diagram).save()
                self.set_recent_files(diagram.file_name)

        if not result:
            MessageDialog("Error", message, self.main_window).run()


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
            return False

        while True:
            name = SaveDialog(
                self.main_window,
                title=_("Export diagram as png"),
                filename=System.get_user_dir() + "/images/" + diagram.patch_name + ".png",
                filetype="png").run()

            if name is None:
                return
            if name.find(".png") == -1:
                name = name + ".png"
            if name is not None and os.path.exists(name) is True:
                msg = _("File exists. Overwrite?")
                result = ConfirmDialog(msg, self.main_window).run()
                if result == Gtk.ResponseType.OK:
                    break
            else:
                break

        result, message = DiagramControl(diagram).export_png(name)

        if not result:
            MessageDialog("Error", message, self.main_window).run()

    # ----------------------------------------------------------------------
    def exit(self, widget=None, data=None):
        """
        This method close main window.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        PreferencesPersistence.save(
            System.get_preferences(), System.get_user_dir())
        if self.main_window.work_area.close_tabs():
            Gtk.main_quit()
        else:
            return True
    # ----------------------------------------------------------------------
    def set_recent_files(self, file_name):
        if file_name in System.get_preferences().recent_files:
            System.get_preferences().recent_files.remove(file_name)
        System.get_preferences().recent_files.insert(0, file_name)
        if len(System.get_preferences().recent_files) > 10:
            System.get_preferences().recent_files.pop()
        self.main_window.menu.update_recent_files(
            System.get_preferences().recent_files)

        PreferencesPersistence.save(
            System.get_preferences(), System.get_user_dir())

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
    def __get_code_generator(self, diagram):

        if diagram.language is None:
            message = "You shall not generate the code of an empty diagram!"
            MessageDialog("Error", message, self.main_window).run()
            return None

        if diagram.code_template is not None:
            return CodeGenerator(diagram)

        template_list = []
        code_templates = System.get_code_templates()

        for key in code_templates:
            if code_templates[key].language == diagram.language:
                template_list.append(code_templates[key])

        if len(template_list) == 0:
            message = "Generator not available for the language " + diagram.language + "."
            MessageDialog("Error", message, self.main_window).run()
            return None

        if len(template_list) == 1:
            diagram.code_template = deepcopy(template_list[0])
            return CodeGenerator(diagram)

        select = SelectCodeTemplate(self.main_window, template_list)
        diagram.code_template = deepcopy(select.get_value())
        return CodeGenerator(diagram)

    # ----------------------------------------------------------------------
    def save_source(self, codes=None, generator=None):
        """
        This method saves the source codes.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False

        # If it is not called from the run method
        if generator is None:
            generator = self.__get_code_generator(diagram)
            if generator is None:
                return False

        if codes is None:
            files = generator.generate_code()
        else:
            files = codes
        for key in files:
            file_name = System.get_dir_name(diagram) + key
            System.log("Saving Code to " + file_name)
            try:
                codeFile = open(file_name, 'w')
                codeFile.write(files[key])
                codeFile.close()
            except Exception as error:
                System.log("File or directory not found!")
                System.log(error)
        return True

    # ----------------------------------------------------------------------
    def view_source(self):
        """
        This method view the source code.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        generator = self.__get_code_generator(diagram)
        codes = {}

        if generator is not None:
            codes = generator.generate_code()
        else:
            return False
        cw = CodeWindow(self.main_window, codes)
        cw.run()
        cw.close()
        cw.destroy()
        return True
        

    # ----------------------------------------------------------------------
    def run(self, codes=None):
        """
        This method runs the code.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False

        generator = self.__get_code_generator(diagram)
        if generator is None:
            return False

        self.save_source(codes=codes, generator=generator)

        command = diagram.code_template.command
        command = command.replace("$dir_name$", System.get_dir_name(diagram))

        def __run(self):
            process = subprocess.Popen(command,
                                       cwd=System.get_dir_name(diagram),
                                       shell=True,
                                       preexec_fn=os.setsid)
            self.threads[thread] = diagram, process
            self.main_window.toolbar.update_threads(self.threads)
            System.log(process.communicate())
            del self.threads[thread]
            self.main_window.toolbar.update_threads(self.threads)

        System.log("Executing Code:\n" + command)
        thread = Thread(target=__run, args=(self,))
        thread.start()

        return True

    # ----------------------------------------------------------------------
    def stop(self, widget, process):
        if process is None:
            return
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)

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
        self.main_window.property_box.set_block(block)

    # ----------------------------------------------------------------------
    def get_selected_block(self):
        """
        This method get the tree view block.
        """
        return self.main_window.block_notebook.get_selected_block()

    # ----------------------------------------------------------------------
    def clear_console(self):
        """
        This method clear the console.
        """
        self.main_window.status.clear()

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
            self.new()
            diagram = self.main_window.work_area.get_current_diagram()
        new_block = BlockModel(block)
        new_block = deepcopy(new_block)
        new_block = Block(diagram, new_block)
        if not DiagramControl(diagram).add_block(new_block):
            message = "Block language is different from diagram language.\n" +\
                "Diagram is expecting to generate " + diagram.language + \
                " code while block is writen in " + block.language
            MessageDialog("Error", message, self.main_window).run()
            return None
        diagram.redraw()
        return new_block

    # ----------------------------------------------------------------------
    def add_comment(self, comment=None):
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
        DiagramControl(diagram).add_comment(comment)
        return True

    # ----------------------------------------------------------------------
    def select_all(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        diagram.select_all()

    # ----------------------------------------------------------------------
    def cut(self):
        """
        This method cut a block on work area.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        DiagramControl(diagram).cut()

    # ----------------------------------------------------------------------
    def copy(self):
        """
        This method copy a block.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        DiagramControl(diagram).copy()

    # ----------------------------------------------------------------------
    def paste(self):
        """
        This method paste a block.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        DiagramControl(diagram).paste()

    # ----------------------------------------------------------------------
    def delete(self):
        """
        This method delete a block.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        DiagramControl(diagram).delete()

    # ----------------------------------------------------------------------
    def zoom_in(self):
        """
        This method increases the zoom value.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        diagram.change_zoom(System.ZOOM_IN)

    # ----------------------------------------------------------------------
    def zoom_out(self):
        """
        This method decreasses the zoom.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        diagram.change_zoom(System.ZOOM_OUT)

    # ----------------------------------------------------------------------
    def zoom_normal(self):
        """
        Set the zoom value to normal.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        diagram.change_zoom(System.ZOOM_ORIGINAL)

    # ----------------------------------------------------------------------
    def undo(self):
        """
        Undo a modification.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        DiagramControl(diagram).undo()

    # ----------------------------------------------------------------------
    def redo(self):
        """
        Redo a modification.
        """
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        DiagramControl(diagram).redo()

    # ----------------------------------------------------------------------
    def align_top(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        DiagramControl(diagram).align("TOP")

    # ----------------------------------------------------------------------
    def align_bottom(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        DiagramControl(diagram).align("BOTTOM")

    # ----------------------------------------------------------------------
    def align_left(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        DiagramControl(diagram).align("LEFT")

    # ----------------------------------------------------------------------
    def align_right(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        DiagramControl(diagram).align("RIGHT")

    # ----------------------------------------------------------------------
    def collapse_all(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        DiagramControl(diagram).collapse_all(True)

    # ----------------------------------------------------------------------
    def uncollapse_all(self):
        diagram = self.main_window.work_area.get_current_diagram()
        if diagram is None:
            return False
        DiagramControl(diagram).collapse_all(False)

    # ----------------------------------------------------------------------
    def redraw(self, show_grid):
        diagrams = self.main_window.work_area.get_diagrams()
        for diagram in diagrams:
            DiagramControl(diagram).set_show_grid(show_grid)
            diagram.redraw()

    # ----------------------------------------------------------------------
    def show_grid(self, event):
        if event is None:
            return
        self.redraw(event.get_active())

    # ----------------------------------------------------------------------
    def add_extension(self, element):
        if isinstance(element, Port):
            PortControl.add_port(element)
        elif isinstance(element, CodeTemplate):
            CodeTemplateControl.add_code_template(element)
        elif isinstance(element, BlockModel):
            BlockControl.add_new_block(element)
            self.update_blocks()
        System.reload()

    # ----------------------------------------------------------------------
    def delete_extension(self, element, element_type):
        if isinstance(element_type, Port):
            if not PortControl.delete_port(element):
                message = "This port is a python file installed in the System.\n"
                message = message + "Sorry, you can't remove it"
                MessageDialog("Error", message, self.main_window).run()
                return False
            System.reload()
        elif isinstance(element_type, CodeTemplate):
            filename = CodeTemplateControl.delete_code_template(element)
            if not filename:
                message = "This code template does not exist."
                MessageDialog("Error", message, self.main_window).run()
                return False
            if filename is None:
                message = "This code template is a python file installed in the System.\n"
                message = message + "Sorry, you can't remove it"
                MessageDialog("Error", message, self.main_window).run()
                return False
            System.reload()
            return True
        elif isinstance(element_type, BlockModel):
            if not BlockControl.delete_block(element):
                message = "This block is a python file installed in the System.\n"
                message = message + "Sorry, you can't remove it"
                MessageDialog("Error", message, self.main_window).run()
                return False
            self.update_blocks()
        MessageDialog("Info", str(element) + " deleted.", self.main_window).run()
        return True

    # ----------------------------------------------------------------------
    def export_extensions(self):
    
        from mosaicode.system import System as System
        System()

        result = True
        folder = "extension-" + datetime.datetime.now().strftime("%Y-%m-%d")

        # Export ports
        ports = System.get_ports()
        for key in ports:
            path = System.get_user_dir()
            path = os.path.join(path, folder, ports[key].language, 'ports')
            result = result and PortPersistence.save(ports[key], path)
        # Export Blocks
        blocks = System.get_blocks()
        result = True
        for key in blocks:
            path = System.get_user_dir()
            path = os.path.join(path,
                                folder,
                                blocks[key].language,
                                'blocks',
                                blocks[key].extension,
                                blocks[key].group)
            result = result and BlockPersistence.save(blocks[key], path)
        # Export Code Templates
        code_templates = System.get_code_templates()
        result = True
        for key in code_templates:
            path = System.get_user_dir()
            path = os.path.join(path,
                                folder,
                                code_templates[key].language,
                                'codetemplates')
            result = result and CodeTemplatePersistence.save(
                    code_templates[key], path)
        # Export examples
        path = System.get_user_dir()
        path = os.path.join(path, "extensions")
        examples = System.get_examples()
        for example in examples:
            relpath = os.path.relpath(example, path)
            path = System.get_user_dir()
            path = os.path.join(path, folder, relpath)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            shutil.copy2(example, path)

        # Create a zip file to the extension
        path = System.get_user_dir()
        path = os.path.join(path, folder+".zip")
        zip_file = zipfile.ZipFile(path, 'w')

        path = System.get_user_dir()
        path = os.path.join(path, folder)

        for folderName, subfolders, filenames in os.walk(path):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                #create complete filepath of file in directory
                # Add file to zip
                zip_file.write(filePath, os.path.relpath(filePath, path))
        zip_file.close()

        path = System.get_user_dir()
        path = os.path.join(path, folder)
        shutil.rmtree(path)

        # create a publish file
        filename = "resource.txt"
        path = System.get_user_dir()
        path = os.path.join(path, filename)
        f = open(path, "w")
        f.write(folder + ".zip")
        f.close()

        if result:
            MessageDialog(
                    "Success",
                     "File " + folder + ".zip created successfully!",
                     self.main_window).run()
        else:
            MessageDialog(
                    "Error",
                    "Could not export extension",
                    self.main_window).run()
        return result

    # ----------------------------------------------------------------------
    def import_extensions(self):
        import urllib.request
        url = "https://alice.dcomp.ufsj.edu.br/mosaicode/extensions/"
        resource_file = url + "resource.txt"
        # download and read resource list
        for line in urllib.request.urlopen(resource_file):
            file_name = line.decode('utf-8')
            # download zip file
            file_path = os.path.join(System.get_user_dir(), file_name)
            urllib.request.urlretrieve(url + file_name, file_path)
            # extract it
            zip_file = zipfile.ZipFile(file_path, 'r')
            destination = os.path.join(System.get_user_dir(), "extensions")
            zip_file.extractall(destination)            
        MessageDialog(
                "Success",
                 "Extensions imported successfully!",
                 self.main_window).run()
        System.reload()
        
    # ----------------------------------------------------------------------
    def update_all(self):
        for diagram in self.main_window.work_area.get_diagrams():
            diagram.update()

# ----------------------------------------------------------------------
