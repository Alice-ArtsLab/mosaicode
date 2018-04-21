# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the DiagramControl class.
"""
import os
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from mosaicode.system import System as System
from mosaicode.persistence.diagrampersistence import DiagramPersistence


class DiagramControl:
    """
    This class contains methods related the DiagramControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, diagram):
        self.diagram = diagram

    # ----------------------------------------------------------------------
    @classmethod
    def add_block(cls, diagram, block):
        """
        This method add a block in the diagram.

            Parameters:
                * **block**
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        if diagram.language is not None and diagram.language != block.language:
            System.log("Block language is different from diagram language.")
            return False
        if diagram.language is None or diagram.language == 'None':
            diagram.language = block.language

        diagram.do("Add Block")
        diagram.last_id = max(int(diagram.last_id), int(block.id))
        if block.id < 0:
            block.id = diagram.last_id
        diagram.last_id += 1
        diagram.blocks[block.id] = block
        return True

    # ----------------------------------------------------------------------
    @classmethod
    def add_comment(cls, diagram, comment):
        """
        This method add a comment in the diagram.

            Parameters:
                * **block**
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        diagram.do("Add Comment")
        diagram.comments.append(comment)
        return True

    # ----------------------------------------------------------------------
    @classmethod
    def add_connection(cls, diagram, connection):
        """
        This method adds a connection to the diagram.

            Parameters:
                * **connection**
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        diagram.do("Add Connection")
        diagram.connectors.append(connection)
        return True

    # ----------------------------------------------------------------------
    @classmethod
    def collapse_all(cls, diagram, status):
        """
        This method Collapses all the blocks in a diagram

            Parameters:
                * **diagram**
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        for block_id in diagram.blocks:
            block = diagram.blocks[block_id]
            block.is_collapsed = status
        diagram.update_flows()
        return True

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

        return True

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
            self.diagram.file_name = "Cadeia_" + str(time.time()) + ".mscd"
        if self.diagram.file_name.find(".mscd") == -1:
            self.diagram.file_name = self.diagram.file_name + ".mscd"

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
