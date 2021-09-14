# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the DiagramControl class.
"""
import os
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from copy import deepcopy
from copy import copy
from mosaicode.system import System as System
from mosaicode.persistence.diagrampersistence import DiagramPersistence
from mosaicode.GUI.comment import Comment
from mosaicode.model.commentmodel import CommentModel
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.connectionmodel import ConnectionModel


class DiagramControl:
    """
    This class contains methods related the DiagramControl class.
    """

    # ----------------------------------------------------------------------
    def __init__(self, diagram):
        self.diagram = diagram

    # ----------------------------------------------------------------------
    def add_block(self, block):
        """
        This method add a block in the diagram.

            Parameters:
                * **block**
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        if self.diagram.language is not None and self.diagram.language != block.language:
            System.log("Block language is different from diagram language.")
            return False
        if self.diagram.language is None or self.diagram.language == 'None':
            self.diagram.language = block.language

        self.do("Add Block")
        self.diagram.last_id = max(int(self.diagram.last_id), int(block.id))
        if block.id < 0:
            block.id = self.diagram.last_id
        self.diagram.last_id += 1
        self.diagram.blocks[block.id] = block
        return True

    # ---------------------------------------------------------------------
    def paste(self):
        """
        This method paste a block.
        """
        replace = {}
        self.diagram.deselect_all()
        # interact into blocks, add blocks and change their id
        clipboard = self.diagram.main_window.main_control.get_clipboard()

        for widget in clipboard:
            if not isinstance(widget, BlockModel):
                continue
            block = BlockModel(widget)
            block.x += 20
            block.y += 20
            block.id = -1
            block = self.diagram.main_window.main_control.add_block(block)
            if block is None:
                return
            replace[widget.id] = block
            block.is_selected = True

        # interact into connections changing block ids
        for widget in clipboard:
            if not isinstance(widget, ConnectionModel):
                continue
            # if a connector is copied without blocks
            if widget.output.id not in replace or widget.input.id \
                    not in replace:
                continue
            output_block = replace[widget.output.id]
            output_port = widget.output_port
            input_block = replace[widget.input.id]
            input_port = widget.input_port
            self.diagram.start_connection(output_block, output_port)
            self.diagram.curr_connector.is_selected = True
            self.diagram.end_connection(input_block, input_port)

        for widget in clipboard:
            if not isinstance(widget, CommentModel):
                continue
            comment = CommentModel(widget)
            comment.x += 20
            comment.y += 20
            comment.is_selected = True
            comment = self.diagram.main_window.main_control.add_comment(comment)


        self.diagram.update_flows()

    # ---------------------------------------------------------------------
    def copy(self):
        """
        This method copy a block.
        """
        mc = self.diagram.main_window.main_control
        mc.reset_clipboard()
        for key in self.diagram.blocks:
            if not self.diagram.blocks[key].is_selected:
                continue
            mc.get_clipboard().append(self.diagram.blocks[key])
        for conn in self.diagram.connectors:
            if not conn.is_selected:
                continue
            mc.get_clipboard().append(conn)
        for comment in self.diagram.comments:
            if not comment.is_selected:
                continue
            mc.get_clipboard().append(comment)

    # ---------------------------------------------------------------------
    def cut(self):
        """
        This method delete a block.
        """
        self.do("Cut")
        self.copy()
        self.delete()

    # ---------------------------------------------------------------------
    def delete(self):
        """
        This method delete a block or connection.
        """
        self.do("Delete")
        for key in self.diagram.blocks.copy():
            if not self.diagram.blocks[key].is_selected:
                continue
            del self.diagram.blocks[key]
        for con in self.diagram.connectors:
            if not con.is_selected:
                continue
            if con not in self.diagram.connectors:
                continue
            self.diagram.connectors.remove(con)
        for comment in self.diagram.comments:
            if not comment.is_selected:
                continue
            self.diagram.comments.remove(comment)

        self.diagram.deselect_all()
        self.diagram.redraw()

    # ----------------------------------------------------------------------
    def add_comment(self, comment=None):
        """
        This method add a comment in the diagram.

            Parameters:
                * **block**
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        self.do("Add Comment")
        new_comment = Comment(self.diagram, comment)
        self.diagram.comments.append(new_comment)
        if comment is None:
            new_comment.is_selected = True
            self.diagram.show_comment_property(new_comment)
        self.diagram.redraw()
        return comment

    # ----------------------------------------------------------------------
    def add_connection(self, connection):
        """
        This method adds a connection to the diagram.

            Parameters:
                * **connection**
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        self.do("Add Connection")
        self.diagram.connectors.append(connection)
        return True

    # ----------------------------------------------------------------------
    def collapse_all(self, status):
        """
        This method Collapses all the blocks in a diagram

            Parameters:
                * **diagram**
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        for block_id in self.diagram.blocks:
            block = self.diagram.blocks[block_id]
            block.is_collapsed = status
        self.diagram.update_flows()
        return True

    # ----------------------------------------------------------------------
    def align(self, alignment):
        top = self.diagram.main_window.get_size()[1]
        bottom = 0
        left = self.diagram.main_window.get_size()[0]
        right = 0

        for key in self.diagram.blocks:
            if not self.diagram.blocks[key].is_selected:
                continue
            x, y = self.diagram.blocks[key].get_position()
            if top > y: top = y
            if bottom < y: bottom = y
            if left > x: left = x
            if right < x: right = x

        for key in self.diagram.blocks:
            if not self.diagram.blocks[key].is_selected:
                continue
            x, y = self.diagram.blocks[key].get_position()
            if alignment == "BOTTOM":
                self.diagram.blocks[key].move(0, bottom -y)
            if alignment == "TOP":
                self.diagram.blocks[key].move(0, top -y)
            if alignment == "LEFT":
                self.diagram.blocks[key].move(left -x, 0)
            if alignment == "RIGHT":
                self.diagram.blocks[key].move(right -x, 0)
        self.diagram.update_flows()

    # ----------------------------------------------------------------------
    def set_show_grid(self, status):
        if status is not None:
            self.diagram.show_grid = status

    # ---------------------------------------------------------------------
    def do(self, new_msg):
        """
        This method do something
            Parameters:
                * **new_msg** (:class:`str<str>`)
        """
        self.diagram.set_modified(True)
        action = (copy(self.diagram.blocks),    #0
                  copy(self.diagram.connectors),#1
                  copy(self.diagram.comments),  #2
                  new_msg)              #3
        self.diagram.undo_stack.append(action)

    # ---------------------------------------------------------------------
    def undo(self):
        """
        This method undo a modification.
        """
        if len(self.diagram.undo_stack) < 1:
            return
        self.diagram.set_modified(True)
        action = self.diagram.undo_stack.pop()
        self.diagram.blocks = action[0]
        self.diagram.connectors = action[1]
        self.diagram.comments = action[2]
        msg = action[3]
        self.diagram.redraw()
        self.diagram.redo_stack.append(action)
        if len(self.diagram.undo_stack) == 0:
            self.diagram.set_modified(False)

    # ---------------------------------------------------------------------
    def redo(self):
        """
        This method redo a modification.
        """
        if len(self.diagram.redo_stack) < 1:
            return
        self.diagram.set_modified(True)
        action = self.diagram.redo_stack.pop()
        self.diagram.blocks = action[0]
        self.diagram.connectors = action[1]
        self.diagram.comments = action[2]
        msg = action[3]
        self.diagram.redraw()
        self.diagram.undo_stack.append(action)

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
    def get_min_max(self):
        """
        This method get min and max.
            Returns

        """
        min_x = self.diagram.main_window.get_size()[0]
        min_y = self.diagram.main_window.get_size()[1]

        max_x = 0
        max_y = 0

        for block_id in self.diagram.blocks:
            block = self.diagram.blocks[block_id]
            x, y = block.get_position()
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if x + block.width > max_x:
                max_x = x + block.width
            if y + block.height > max_y:
                max_y = y + block.height
        return min_x, min_y, max_x - min_x, max_y - min_y

    # ----------------------------------------------------------------------
    def export_png(self, file_name="diagrama.png"):
        """
        This method export a png.

        Returns:

            * **Types** (:class:`boolean<boolean>`): True to Success.
        """
        if file_name is None:
            file_name = "diagrama.png"

        x, y, width, height = self.get_min_max()

        if x < 0 or y < 0:
            self.diagram.reload()
            x, y, width, height = self.get_min_max()

        if self.diagram.get_window() is None:
            return False, "Diagram has no window"
        pixbuf = Gdk.pixbuf_get_from_window(
                        self.diagram.get_window(),
                        x,
                        y,
                        width,
                        height)

        if pixbuf is None:
            return False, "No image to export"

        test, tmp_buffer = pixbuf.save_to_bufferv("png",  [], [])

        try:
            save_file = open(file_name, "wb")
            save_file.write(tmp_buffer)
            save_file.close()
        except IOError as e:
            System.log(e.strerror)
            return False, e.strerror

        return True, "Sucess"
# ------------------------------------------------------------------------------
