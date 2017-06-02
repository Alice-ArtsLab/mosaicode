# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the DiagramControl class.
"""
import os
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from harpia.utils.XMLUtils import XMLParser
from harpia.system import System as System
from harpia.control.codegenerator import CodeGenerator
from harpia.model.codetemplate import CodeTemplate
from harpia.persistence.diagrampersistence import DiagramPersistence


class DiagramControl():
    """
    This class contains methods related the DiagramControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, diagram):
        self.diagram = diagram

    # ----------------------------------------------------------------------
    def get_code_template(self):
        code_template = CodeTemplate()
        for key in System.code_templates:
            if System.code_templates[key].language == self.diagram.language:
                code_template = System.code_templates[key]
                break
        generator = CodeGenerator(self.diagram, code_template)
        return generator

    # ----------------------------------------------------------------------
    def load(self, file_name=None):
        """
        This method load a file.

        Returns:
            * **Types** (:class:`boolean<boolean>`)
        """
        if file_name is not None:
            self.diagram.file_name = file_name
        else:
            if self.diagram.file_name is None:
                System.log("Cannot Load without filename")
                return False
        if not os.path.exists(self.diagram.file_name):
            System.log("File '" + self.diagram.file_name +
                       "' does not exist!")
            return False

        DiagramPersistence.load(self.diagram)
        self.diagram.redo_stack = []
        self.diagram.undo_stack = []

    # ----------------------------------------------------------------------
    def save(self, file_name=None):
        """
        This method save a file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        if file_name is not None:
            self.diagram.file_name = file_name
        if self.diagram.file_name is None:
            self.diagram.file_name = "Cadeia_" + str(time.time()) + ".hrp"
        if self.diagram.file_name.find(".hrp") == -1:
            self.diagram.file_name = self.diagram.file_name + ".hrp"

        return DiagramPersistence.save(self.diagram)

    # ----------------------------------------------------------------------
    def export_png(self, file_name="diagrama.png"):
        """
        This method export a png.

        Returns:

            * **Types** (:class:`boolean<boolean>`): True to Success.
        """
        if file_name is None:
            file_name = "diagrama.png"

        x, y, width, height = self.diagram.get_min_max()

        if x < 0 or y < 0:
            self.diagram.reload()
            x, y, width, height = self.diagram.get_min_max()

        pixbuf = Gdk.pixbuf_get_from_window(
            self.diagram.get_window(), x, y, width, height)

        if pixbuf is None:
            return False, "No image to export"

        test, tmp_buffer = pixbuf.save_to_bufferv("png",  [], [])

        try:
            save_file = open(file_name, "w")
            save_file.write(tmp_buffer)
            save_file.close()
        except IOError as e:
            System.log(e.strerror)
            return False, e.strerror

        return True, ""
# ------------------------------------------------------------------------------
