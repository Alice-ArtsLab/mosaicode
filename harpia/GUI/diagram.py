# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org), S2i (www.s2i.das.ufsc.br)
#
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License version 3, as published
#    by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranties of
#    MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#    PURPOSE.  See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    For further information, check the COPYING file distributed with this software.
#
# ----------------------------------------------------------------------

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GooCanvas

import copy

from block import Block
from connector import Connector
from harpia.s2idirectory import *
from harpia.model.diagrammodel import DiagramModel
from harpia.constants import *

class Diagram(GooCanvas.Canvas, DiagramModel):

    #----------------------------------------------------------------------
    def __init__(self, main_window):
        GooCanvas.Canvas.__init__(self)
        DiagramModel.__init__(self)
        self.set_property("expand", True)

        self.last_clicked_point = (None, None)
        self.__main_window = main_window

        self.undo_stack = []
        self.redo_stack = []

        self.__block_id = 0
        self.curr_connector = None
        self.current_widgets = []

        self.grab_focus()
        self.connect("motion-notify-event", self.__on_motion_notify)
        self.connect_after("button_press_event", self.__on_button_press)
        self.connect_after("button_release_event", self.__on_button_release)
        self.connect_after("key-press-event", self.__on_key_press)

        self.connect("drag_data_received", self.__drag_data_received)
        self.drag_dest_set(
            Gtk.DestDefaults.MOTION | Gtk.DestDefaults.HIGHLIGHT | Gtk.DestDefaults.DROP,
            [Gtk.TargetEntry.new('text/plain', Gtk.TargetFlags.SAME_APP, 1)],
            Gdk.DragAction.DEFAULT | Gdk.DragAction.COPY)

        self.white_board = None
        self.select_rect = None
        self.__update_white_board()
        self.scrolled_window = None
        self.show()

    #----------------------------------------------------------------------
    def __del__(self):
        pass

    #----------------------------------------------------------------------
    def set_scrolled_window(self, frame):
        self.scrolled_window = frame

    #----------------------------------------------------------------------
    def __on_motion_notify(self, canvas_item, event=None):
        # Select elements
        if self.select_rect != None:
            xi = 0
            xf = 0
            yi = 0
            yf = 0
            if event.x > self.last_clicked_point[0]:
                xi = self.last_clicked_point[0]
                xf = event.x
            else:
                xi = event.x
                xf = self.last_clicked_point[0]
            if event.y > self.last_clicked_point[1]:
                yi = self.last_clicked_point[1]
                yf = event.y
            else:
                yi = event.y
                yf = self.last_clicked_point[1]

            self.select_rect.set_property("x", xi)
            self.select_rect.set_property("width", xf - xi)
            self.select_rect.set_property("y", yi)
            self.select_rect.set_property("height", yf - yi)

            for block_id in self.blocks:
                block = self.blocks[block_id]
                if block.get_position()[0] > xi \
                    and block.get_position()[0] + block.width < xf \
                    and block.get_position()[1] > yi \
                    and block.get_position()[1] + block.height < yf \
                    and block not in self.current_widgets:
                        self.current_widgets.append(block)
#                elif block in self.current_widgets:
#                    self.current_widgets.remove(block)
                block.update_flow()

            for conn in self.connectors:
                if conn.from_point[0] > xi \
                    and conn.to_point[0] < xf \
                    and conn.from_point[1] > yi \
                    and conn.to_point[1] < yf \
                    and conn not in self.current_widgets:
                        self.current_widgets.append(conn)
#                elif conn in self.current_widgets:
#                    self.current_widgets.remove(conn)
                conn.update_flow()

            return True #Abort other events

        if event.state & Gdk.ModifierType.BUTTON1_MASK:
            for connector in self.connectors:
                connector.update_flow()

        if self.curr_connector == None:
            return False
        point = (event.x,event.y)
        self.curr_connector.update_tracking(point)
        return False

    #-------------------------------------------------------[0---------------
    def __on_key_press(self, widget, event=None):
        if event.state == Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK:
            if event.keyval == Gdk.KEY_Up:
                self.move_selected_blocks(0,-5)
                return True
            if event.keyval == Gdk.KEY_Down:
                self.move_selected_blocks(0,5)
                return True
            if event.keyval == Gdk.KEY_Left:
                self.move_selected_blocks(-5,0)
                return True
            if event.keyval == Gdk.KEY_Right:
                self.move_selected_blocks(5,0)
                return True

        if event.keyval == Gdk.KEY_Delete:
            self.delete()
            return True

        if event.keyval == Gdk.KEY_Up:
            self.move_selected_blocks(0,-1)
            return True
        if event.keyval == Gdk.KEY_Down:
            self.move_selected_blocks(0,1)
            return True
        if event.keyval == Gdk.KEY_Left:
            self.move_selected_blocks(-1,0)
            return True
        if event.keyval == Gdk.KEY_Right:
            self.move_selected_blocks(1,0)
            return True


    #----------------------------------------------------------------------
    def __on_button_release(self, widget, event=None):
        if self.select_rect != None:
            self.select_rect.remove()
            del self.select_rect
            self.select_rect = None

    #----------------------------------------------------------------------
    def __on_button_press(self, widget, event=None):
        Gtk.Widget.grab_focus(self)
        if event.button == 1:
            self.last_clicked_point = (event.x, event.y)
            self.current_widgets = []
            self.__abort_connection()
            self.update_flows()
            self.__start_select()
            return False
        return False

    #----------------------------------------------------------------------
    def __start_select(self):
        if self.select_rect == None:
            self.select_rect = GooCanvas.CanvasRect(
                            parent=self.get_root_item(),
                            x = self.last_clicked_point[0],
                            y = self.last_clicked_point[1],
                            width=0,
                            height=0,
                            stroke_color="black",
                            fill_color=None,
                            line_dash = GooCanvas.CanvasLineDash.newv((4.0, 2.0))
                            )

    # ----------------------------------------------------------------------
    def __drag_data_received(self, widget, context, x, y, selection, targetType, time):
        block = self.__main_window.main_control.get_selected_block()
        if block != None:
            block.x = x
            block.y = y
            self.__main_window.main_control.add_block(block)
        return

    #----------------------------------------------------------------------
    def update_scrolling(self):
        x, y, width, height = self.get_min_max()
        for block_id in self.blocks:
            block = self.blocks[block_id]
            block.move(0 - x, 0 - y)
        self.update_flows()

    #----------------------------------------------------------------------
    def insert_block(self, plugin):
        plugin.set_id(self.__block_id)
        if not self.load_block(plugin):
            return False
        self.update_scrolling()
        return True

    #----------------------------------------------------------------------
    def load_block(self, plugin):
        if self.language != None and self.language != plugin.language:
            return False
        if self.language == None:
            self.language = plugin.language
        self.do("Insert block")
        new_block = Block(self, plugin)
        self.blocks[plugin.get_id()] = new_block
        self.get_root_item().add_child(new_block, -1)
        self.set_modified(True)
        self.__block_id = max(int(self.__block_id), int(plugin.get_id()))
        self.__block_id = int(self.__block_id) + 1
        return True

    #----------------------------------------------------------------------
    def insert_ready_connector(self, from_block, from_block_out, to_block, to_block_in):
        if from_block not in self.blocks:
            harpia.s2idirectory.Log.log("Connection from non existent block")
            return
        if to_block not in self.blocks:
            harpia.s2idirectory.Log.log("Connection to non existent block")
            return
        conn_type = self.blocks[from_block].get_description()["OutTypes"][from_block_out]
        new_connection = Connector(self, from_block, from_block_out, conn_type)
        new_connection.set_end(to_block, to_block_in)
        if self.__valid_connector(new_connection):
            if self.__connector_types_match(new_connection):
                self.connectors.append(new_connection)  # TODO: checar se ja existe este conector
                self.connector_id += 1
                self.update_flows()
                self.get_root_item().add_child(new_connection, -1)
        return new_connection

    #----------------------------------------------------------------------
    def clicked_input(self, block, block_input):
        if self.curr_connector == None:
            return
        self.curr_connector.set_end(block.get_id(), block_input)
        if not self.__valid_connector(self.curr_connector):
            self.__abort_connection()
            return
        if not self.__connector_types_match(self.curr_connector):
            self.__abort_connection()
            return
        self.connectors.append(self.curr_connector)

        self.connector_id += 1
        self.curr_connector = None
        self.update_flows()

    #----------------------------------------------------------------------
    def __connector_types_match(self, conn):
        outType = self.blocks[conn.from_block].get_description()["OutTypes"][conn.from_block_out]
        inType = self.blocks[conn.to_block].get_description()["InTypes"][conn.to_block_in]
        if not outType == inType:
            harpia.s2idirectory.Log.log("Connection Types mismatch")
        return outType == inType

    #----------------------------------------------------------------------
    def __valid_connector(self, newCon):
        for oldCon in self.connectors:
            if oldCon.to_block == newCon.to_block \
                    and oldCon.to_block_in == newCon.to_block_in\
                    and not harpia.s2idirectory.connections[newCon.type]["multiple"]:
                harpia.s2idirectory.Log.log("Connector Already exists")
                return False
        if newCon.to_block == newCon.from_block:
            harpia.s2idirectory.Log.log("Recursive connection is not allowed")
            return False
        return True

    #----------------------------------------------------------------------
    def clicked_output(self, block, output):
        self.__abort_connection()  # abort any possibly running connections
        conn_type = block.get_description()["OutTypes"][output]
        self.curr_connector = Connector(self, block.get_id(), output, conn_type)
        self.get_root_item().add_child(self.curr_connector, -1)
        self.update_flows()

    #----------------------------------------------------------------------
    def __abort_connection(self):
        if self.curr_connector == None:
            return
        connector_number = self.get_root_item().find_child(self.curr_connector)
        self.get_root_item().remove_child(connector_number)
        del self.curr_connector
        self.curr_connector = None

    #----------------------------------------------------------------------
    def __white_board_event(self, widget, event=None):
        if event.type == Gdk.EventType.BUTTON_PRESS:  # se temos um clique nao pego por ngm, abortar a conexao
            if event.button == 1:
                self.white_board.grab_focus()
                self.__abort_connection()
                return False
        return False

    #----------------------------------------------------------------------
    def __update_white_board(self):
        self.white_board = GooCanvas.CanvasRect(
                        parent=self.get_root_item(),
                        x=0,
                        y=0,
                        width=self.__main_window.get_size()[0],
                        height=1000,
                        stroke_color="white",
                        fill_color="white")
        self.white_board.connect("focus-in-event", self.__white_board_event)

    #----------------------------------------------------------------------
    def update_flows(self):
        for block_id in self.blocks:  # self.blocks is a dict!
            self.blocks[block_id].update_flow()
        for conn in self.connectors:
            conn.update_flow()

    #----------------------------------------------------------------------
    def get_connectors_to(self, block):
        result = []
        for conn in self.connectors:
            if conn.to_block == block.get_id():
                result.append(conn)
        return result

    #----------------------------------------------------------------------
    def set_file_name(self, file_name):
        DiagramModel.set_file_name(self, file_name)
        self.__main_window.work_area.rename_diagram(self)

    #----------------------------------------------------------------------
    def __apply_zoom(self):
        self.set_scale(self.get_zoom())
        self.update_scrolling()
        self.set_modified(True)

    #----------------------------------------------------------------------
    def set_zoom(self, zoom):
        DiagramModel.set_zoom(self, zoom)
        self.__apply_zoom()

    #----------------------------------------------------------------------
    def change_zoom(self, value):
        zoom = self.get_zoom()
        if value == ZOOM_ORIGINAL:
            zoom = ZOOM_ORIGINAL
        elif value == ZOOM_IN:
            zoom = zoom + 0.1
        elif value == ZOOM_OUT:
            zoom = zoom - 0.1
        DiagramModel.set_zoom(self, zoom)
        self.__apply_zoom()

    #----------------------------------------------------------------------
    def show_block_property(self, block):
        self.__main_window.main_control.show_block_property(block)

    # ----------------------------------------------------------------------
    def resize(self, data):
        self.set_property("x2", self.__main_window.get_size()[0])
        self.white_board.set_property("width", self.__main_window.get_size()[0])

    # ----------------------------------------------------------------------
    def select_all(self):
        self.current_widgets = []
        for block_id in self.blocks:
            self.current_widgets.append(self.blocks[block_id])
        for conn in self.connectors:
            self.current_widgets.append(conn)
        self.update_flows()

    # ----------------------------------------------------------------------
    def move_selected_blocks(self, x, y):
        self.do("Move selected blocks")
        for block_id in self.blocks:
            if self.blocks[block_id] in self.current_widgets:
                self.blocks[block_id].move(x,y)
        self.update_flows()
        self.set_modified(True)

    # ---------------------------------------------------------------------
    def delete(self):
        for widget in self.current_widgets:
            widget.delete()
        self.current_widgets = []
        self.update_flows()

    # ---------------------------------------------------------------------
    def paste(self):
        replace = {}
        self.current_widgets = []
        # interact into blocks, add blocks and change their id
        clipboard = self.__main_window.main_control.get_clipboard()
        for widget in clipboard:
            if not isinstance(widget, Block):
                continue
            plugin = copy.deepcopy(widget.get_plugin())
            plugin.x += 20
            plugin.y += 20
            if not self.__main_window.main_control.add_block(plugin):
                return
            new_id = plugin.get_id()
            replace[widget.get_id()] = new_id
            self.current_widgets.append(self.blocks[new_id])
        # interact into connections changing block ids
        for widget in clipboard:
            if not isinstance(widget, Connector):
                continue
            # if a connector is copied without blocks
            if widget.from_block not in replace:
                continue
            if widget.to_block not in replace:
                continue
            from_block = replace[widget.from_block]
            from_block_out = widget.from_block_out
            to_block = replace[widget.to_block]
            to_block_in = widget.to_block_in
            new_connection = self.insert_ready_connector(
                        from_block,
                        from_block_out,
                        to_block,
                        to_block_in)
            self.current_widgets.append(new_connection)
        self.update_flows()

    # ---------------------------------------------------------------------
    def copy(self):
        self.__main_window.main_control.reset_clipboard()
        for widget in self.current_widgets:
            self.__main_window.main_control.get_clipboard().append(widget)

    # ---------------------------------------------------------------------
    def cut(self):
        self.__main_window.main_control.reset_clipboard()
        for widget in self.current_widgets:
            self.__main_window.main_control.get_clipboard().append(widget)
            widget.delete()

    #----------------------------------------------------------------------
    def delete_connection(self, connection):
        if connection not in self.connectors:
            return
        self.do("Delete Connection")
        self.connectors.remove(connection)
        connection.remove()
        self.set_modified(True)

    #----------------------------------------------------------------------
    def delete_block(self, block):
        block_id = block.get_id()
        # removing related connectors
        for idx in reversed(range(len(self.connectors))):
            if self.connectors[idx].from_block == block_id \
                or self.connectors[idx].to_block == block_id:
                    self.delete_connection(self.connectors[idx])

        if block_id not in self.blocks:
            return
        self.do("Delete Block")
        self.blocks[block_id].remove()
        del self.blocks[block_id]
        self.update_flows()
        self.set_modified(True)

    # ---------------------------------------------------------------------
    def set_modified(self, state):
        DiagramModel.set_modified(self, state)
        self.__main_window.work_area.rename_diagram(self)

    # ---------------------------------------------------------------------
    def grab_focus(self):
        Gtk.Widget.grab_focus(self)

    # ---------------------------------------------------------------------
    def redraw(self):
        while self.get_root_item().get_n_children() != 0:
            self.get_root_item().remove_child(0)
        self.__update_white_board()
        for block_id in self.blocks:
            self.get_root_item().add_child(self.blocks[block_id], -1)
        for connector in self.connectors:
            self.get_root_item().add_child(connector, -1)

    # ---------------------------------------------------------------------
    def do(self, msg):
        harpia.s2idirectory.Log.log("Do: " + msg)
        self.undo_stack.append(
                (copy.copy(self.blocks), 
                copy.copy(self.connectors),
                msg))
        self.redo_stack = []

    # ---------------------------------------------------------------------
    def undo(self):
        if len(self.undo_stack) < 1:
            return
        blocks, connectors, msg = self.undo_stack.pop()
        harpia.s2idirectory.Log.log("Undo: " + msg)
        self.redo_stack.append(
                (copy.copy(self.blocks), 
                copy.copy(self.connectors),
                msg))
        self.blocks = blocks
        self.connectors = connectors
        self.redraw()

    # ---------------------------------------------------------------------
    def redo(self):
        if len(self.redo_stack) < 1:
            return
        blocks, connectors, msg = self.redo_stack.pop()
        harpia.s2idirectory.Log.log("Redo: " + msg)
        self.undo_stack.append(
                (copy.copy(self.blocks), 
                copy.copy(self.connectors),
                msg))
        self.blocks = blocks
        self.connectors = connectors
        self.redraw()

    # ---------------------------------------------------------------------
    def get_min_max(self):
        min_x = 32000
        min_y = 32000

        max_x = 0
        max_y = 0

        for block_id in self.blocks:
            block = self.blocks[block_id]
            x,y = block.get_position()
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if x + block.width > max_x:
                max_x = x + block.width
            if y + block.height > max_y:
                max_y = y + block.height

        return min_x, min_y, max_x - min_x, max_y - min_y
#----------------------------------------------------------------------
