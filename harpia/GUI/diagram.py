# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org),
# S2i (www.s2i.das.ufsc.br)
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
#    For further information, check the COPYING file distributed with this
#    software.
#
# ----------------------------------------------------------------------
"""
This module contains the Diagram class.
"""
import gi
import copy
from block import Block
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk
from gi.repository import Gdk
from connector import Connector
from gi.repository import GObject
from gi.repository import GooCanvas
from harpia.system import System as System
from harpia.model.diagrammodel import DiagramModel
import gettext
_ = gettext.gettext


class Diagram(GooCanvas.Canvas, DiagramModel):
    """
    This class contains the methods related to Diagram class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        GooCanvas.Canvas.__init__(self)
        DiagramModel.__init__(self)
        self.set_property("expand", True)

        self.last_clicked_point = (None, None)
        self.__main_window = main_window

        self.curr_connector = None
        self.current_widgets = []

        self.grab_focus()
        self.connect("motion-notify-event", self.__on_motion_notify)
        self.connect_after("button_press_event", self.__on_button_press)
        self.connect_after("button_release_event", self.__on_button_release)
        self.connect_after("key-press-event", self.__on_key_press)

        self.connect("drag_data_received", self.__drag_data_received)
        self.drag_dest_set(
            Gtk.DestDefaults.MOTION |
            Gtk.DestDefaults.HIGHLIGHT |
            Gtk.DestDefaults.DROP,
            [Gtk.TargetEntry.new('text/plain', Gtk.TargetFlags.SAME_APP, 1)],
            Gdk.DragAction.DEFAULT | Gdk.DragAction.COPY)

        self.white_board = None
        self.select_rect = None
        self.__update_white_board()
        self.scrolled_window = None
        self.set_property("has-tooltip", True)  # Allow tooltip on elements
        self.show()

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def set_scrolled_window(self, frame):
        """
        This method set scrolled window.

            Parameters:
                * **frame**

        """
        self.scrolled_window = frame

    # ----------------------------------------------------------------------
    def __on_motion_notify(self, canvas_item, event):
        scale = self.get_scale()
        # Select elements
        if self.select_rect is not None:
            self.__update_select(event.x / scale, event.y / scale)
            items = self.get_items_in_area(
                self.select_rect.bounds, True, False, True)
            self.current_widgets = []
            for item in items:
                if not isinstance(item, Connector) and not \
                        isinstance(item, Block):
                    continue
                if item not in self.current_widgets:
                    self.current_widgets.append(item)
            self.update_flows()
            return True  # Abort other events

        if event.state & Gdk.ModifierType.BUTTON1_MASK:
            for connector in self.connectors:
                connector.update_flow()

        if self.curr_connector is None:
            return False
        point = (event.x / scale, event.y / scale)
        self.curr_connector.update_tracking(point)
        return False

    # ----------------------------------------------------------------------
    def __on_key_press(self, widget, event=None):
        if event.state == \
                Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK:
            if event.keyval == Gdk.KEY_Up:
                self.move_selected_blocks(0, -5)
                return True
            if event.keyval == Gdk.KEY_Down:
                self.move_selected_blocks(0, 5)
                return True
            if event.keyval == Gdk.KEY_Left:
                self.move_selected_blocks(-5, 0)
                return True
            if event.keyval == Gdk.KEY_Right:
                self.move_selected_blocks(5, 0)
                return True

        if event.keyval == Gdk.KEY_Delete:
            self.delete()
            return True

        if event.keyval == Gdk.KEY_Up:
            self.move_selected_blocks(0, -1)
            return True
        if event.keyval == Gdk.KEY_Down:
            self.move_selected_blocks(0, 1)
            return True
        if event.keyval == Gdk.KEY_Left:
            self.move_selected_blocks(-1, 0)
            return True
        if event.keyval == Gdk.KEY_Right:
            self.move_selected_blocks(1, 0)
            return True

    # ----------------------------------------------------------------------
    def __on_button_release(self, widget, event=None):
        self.__end_select()

    # ----------------------------------------------------------------------
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

    # ----------------------------------------------------------------------
    def __start_select(self):
        if self.select_rect is None:
            self.select_rect = GooCanvas.CanvasRect(
                parent=self.get_root_item(),
                x=self.last_clicked_point[0],
                y=self.last_clicked_point[1],
                width=0,
                height=0,
                stroke_color="black",
                fill_color=None,
                line_dash=GooCanvas.CanvasLineDash.newv((4.0, 2.0))
            )

    # ----------------------------------------------------------------------
    def __end_select(self):
        if self.select_rect is not None:
            self.select_rect.remove()
            del self.select_rect
            self.select_rect = None

    # ----------------------------------------------------------------------
    def __update_select(self, x, y):
        scale = self.get_scale()
        xi = 0
        xf = 0
        yi = 0
        yf = 0
        if x > self.last_clicked_point[0] / scale:
            xi = self.last_clicked_point[0] / scale
            xf = x
        else:
            xi = x
            xf = self.last_clicked_point[0] / scale
        if y > self.last_clicked_point[1] / scale:
            yi = self.last_clicked_point[1] / scale
            yf = y
        else:
            yi = y
            yf = self.last_clicked_point[1] / scale
        self.select_rect.set_property("x", xi)
        self.select_rect.set_property("width", xf - xi)
        self.select_rect.set_property("y", yi)
        self.select_rect.set_property("height", yf - yi)

    # ----------------------------------------------------------------------
    def __drag_data_received(self, widget, context, x, y, selection,
                             targetType, time):
        block = self.__main_window.main_control.get_selected_block()
        if block is not None:
            block.x = x
            block.y = y
            self.__main_window.main_control.add_block(block)
        return

    # ----------------------------------------------------------------------
    def update_scrolling(self):
        """
        This method update scrolling.

        """
        x, y, width, height = self.get_min_max()
        if x >= 0 and y >= 0:
            self.update_flows()
            return
        for block_id in self.blocks:
            block = self.blocks[block_id]
            block.move(0 - x, 0 - y)
        self.update_flows()

    # ----------------------------------------------------------------------
    def add_block(self, plugin):
        """
        This method add a block in the diagram.

            Parameters:
                * **plugin**
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        new_block = Block(self, plugin)
        if DiagramModel.add_block(self, new_block):
            self.do("Add")
            self.get_root_item().add_child(new_block, -1)
            return True
        else:
            return False

    # ----------------------------------------------------------------------

    def __valid_connector(self, newCon):
        """
        Parameters:

        Returns
             * **Types** (:class:`boolean<boolean>`)
        """
        for oldCon in self.connectors:
            if oldCon.sink == newCon.sink \
                    and oldCon.sink_port == newCon.sink_port\
                    and not System.connectors[newCon.type]["multiple"]:
                System.log(_("Connector Already exists"))
                return False
        if newCon.sink == newCon.source:
            System.log(_("Recursive connection is not allowed"))
            return False
        return True

    # ----------------------------------------------------------------------
    def __abort_connection(self):
        if self.curr_connector is None:
            return
        connector_number = self.get_root_item().find_child(self.curr_connector)
        self.get_root_item().remove_child(connector_number)
        del self.curr_connector
        self.curr_connector = None

    # ----------------------------------------------------------------------
    def start_connection(self, block, output):
        """
        This method start a connection.

            Parameters:
                * **block**
                * **output**

        """
        self.__abort_connection()  # abort any possibly running connections
        conn_type = block.get_out_types()[output]
        self.curr_connector = Connector(self, block, output, conn_type)
        self.get_root_item().add_child(self.curr_connector, -1)
        self.update_flows()

    # ----------------------------------------------------------------------
    def end_connection(self, block, block_input):
        """
        This method end a connection.

            Parameters:
                * **block**
                * **block_input**
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        if self.curr_connector is None:
            return False
        self.curr_connector.set_end(block, block_input)
        if not self.__valid_connector(self.curr_connector):
            self.__abort_connection()
            return False
        if not self.curr_connector.type_match():
            System.log(_("Connection Types mismatch"))
            self.__abort_connection()
            return False
        self.add_connection(self.curr_connector)
        self.curr_connector = None
        self.update_flows()
        return True

    # ----------------------------------------------------------------------
    def __white_board_event(self, widget, event=None):
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == 1:
                self.white_board.grab_focus()
                self.__abort_connection()
        return False

    # ----------------------------------------------------------------------
    def __update_white_board(self):
        self.white_board = GooCanvas.CanvasRect(
            parent=self.get_root_item(),
            x=0,
            y=0,
            width=self.__main_window.get_size()[0],
            height=self.__main_window.get_size()[1],
            stroke_color="white",
            fill_color="white")
        self.white_board.connect("focus-in-event", self.__white_board_event)

    # ----------------------------------------------------------------------
    def update_flows(self):
        """
        This method update flows.
        """
        self.white_board.set_property("stroke_color", "white")
        for block_id in self.blocks:
            self.blocks[block_id].update_flow()
        for conn in self.connectors:
            conn.update_flow()

    # ----------------------------------------------------------------------
    def set_file_name(self, file_name):
        """
        This method set name of diagram file.

            Parameters:
                * **file_name** (:class:`str<str>`)

        """
        DiagramModel.set_file_name(self, file_name)
        self.__main_window.work_area.rename_diagram(self)

    # ----------------------------------------------------------------------
    def __apply_zoom(self):
        self.set_scale(self.get_zoom())
        self.update_scrolling()
        self.set_modified(True)

    # ----------------------------------------------------------------------
    def set_zoom(self, zoom):
        """
        This method set zoom.

            Parameters:
                * **zoom**
        """
        DiagramModel.set_zoom(self, zoom)
        self.__apply_zoom()

    # ----------------------------------------------------------------------
    def change_zoom(self, value):
        """
        This method change zoom.

            Parameters:
               * **value** (:class:`float<float>`)
        """
        zoom = self.get_zoom()
        if value == System.ZOOM_ORIGINAL:
            zoom = System.ZOOM_ORIGINAL
        elif value == System.ZOOM_IN:
            zoom = zoom + 0.1
        elif value == System.ZOOM_OUT:
            zoom = zoom - 0.1
        DiagramModel.set_zoom(self, zoom)
        self.__apply_zoom()

    # ----------------------------------------------------------------------
    def show_block_property(self, block):
        """
        This method show block property.

            Parameters:
                * **block**(:class: `Block<harpia.GUI.block>`)
        """
        self.__main_window.main_control.show_block_property(block)

    # ----------------------------------------------------------------------
    def resize(self, data):
        """
        This method resize diagram.

            Parameters:
               * **data**
        """
        self.set_property("x2", self.__main_window.get_size()[0])
        self.white_board.set_property(
            "width", self.__main_window.get_size()[0])

    # ----------------------------------------------------------------------
    def select_all(self):
        """
        This method select all blocks in diagram.
        """
        self.current_widgets = []
        for block_id in self.blocks:
            self.current_widgets.append(self.blocks[block_id])
        for conn in self.connectors:
            self.current_widgets.append(conn)
        self.update_flows()

    # ----------------------------------------------------------------------
    def move_selected_blocks(self, x, y):
        """
        This method move selected blocks.

            Parameters:
                * **(x,y)** (:class:`float<float>`)

        """
        self.do("Move blocks")
        for block_id in self.blocks:
            if self.blocks[block_id] in self.current_widgets:
                self.blocks[block_id].move(x, y)
        self.update_scrolling()

    # ---------------------------------------------------------------------
    def delete(self):
        """
        This method delete a block.

        """
        if len(self.current_widgets) < 1:
            return
        self.do("Delete")
        for widget in self.current_widgets:
            widget.delete()
        self.current_widgets = []
        self.update_flows()

    # ---------------------------------------------------------------------
    def paste(self):
        """
        This method paste a block.
        """
        replace = {}
        self.current_widgets = []
        # interact into blocks, add blocks and change their id
        clipboard = self.__main_window.main_control.get_clipboard()
        for widget in clipboard:
            if not isinstance(widget, Block):
                continue
            plugin = copy.deepcopy(widget)
            plugin.x += 20
            plugin.y += 20
            plugin.set_id(-1)
            if not self.__main_window.main_control.add_block(plugin):
                return
            replace[widget.get_id()] = plugin
            self.current_widgets.append(plugin)
        # interact into connections changing block ids
        for widget in clipboard:
            if not isinstance(widget, Connector):
                continue
            # if a connector is copied without blocks
            if widget.source.get_id() not in replace or widget.sink.get_id() \
                    not in replace:
                continue
            print _("continuing...")
            source = replace[widget.source.get_id()]
            source_port = widget.source_port
            sink = replace[widget.sink.get_id()]
            sink_port = widget.sink_port
            self.start_connection(source, source_port)
            self.current_widgets.append(self.curr_connector)
            self.end_connection(sink, sink_port)
        self.update_flows()

    # ---------------------------------------------------------------------
    def copy(self):
        """
        This method copy a block.
        """
        self.__main_window.main_control.reset_clipboard()
        for widget in self.current_widgets:
            self.__main_window.main_control.get_clipboard().append(widget)

    # ---------------------------------------------------------------------
    def cut(self):
        """
        This method delete a block.
        """
        if len(self.current_widgets) < 1:
            return
        self.do(_("Cut"))
        self.__main_window.main_control.reset_clipboard()
        for widget in self.current_widgets:
            self.__main_window.main_control.get_clipboard().append(widget)
            widget.delete()

    # ----------------------------------------------------------------------
    def delete_connection(self, connection):
        """
        This method delete a connection.

            Parameters:
                connection
        """
        DiagramModel.delete_connection(self, connection)
        connection.remove()

    # ----------------------------------------------------------------------
    def delete_block(self, block):
        """
        This method delete a block.

            Parameters:
                block
        """
        if not DiagramModel.delete_block(self, block):
            return
        self.blocks[block.get_id()].remove()
        del self.blocks[block.get_id()]
        self.update_flows()

    # ---------------------------------------------------------------------
    def set_modified(self, state):
        """
        This method set a modification.

            Parameters:
                * **state**
        """
        DiagramModel.set_modified(self, state)
        self.__main_window.work_area.rename_diagram(self)

    # ---------------------------------------------------------------------
    def grab_focus(self):
        """
        This method define focus.

        """
        Gtk.Widget.grab_focus(self)

    # ---------------------------------------------------------------------
    def redraw(self):
        """
        This method redraw a block.
        """
        while self.get_root_item().get_n_children() != 0:
            self.get_root_item().remove_child(0)
        self.__update_white_board()
        for block_id in self.blocks:
            self.get_root_item().add_child(self.blocks[block_id], -1)
        for connector in self.connectors:
            self.get_root_item().add_child(connector, -1)

    # ---------------------------------------------------------------------
    def do(self, new_msg):
        """
        This method do something
            Parameters:
                * **new_msg** (:class:`str<str>`)
        """
        self.set_modified(True)
        action = (copy.copy(self.blocks), copy.copy(self.connectors), new_msg)
        self.undo_stack.append(action)
        System.log(_("Do: " + new_msg))

    # ---------------------------------------------------------------------
    def undo(self):
        """
        This method undo a modification.
        """
        if len(self.undo_stack) < 1:
            return
        self.set_modified(True)
        action = self.undo_stack.pop()
        self.blocks = action[0]
        self.connectors = action[1]
        msg = action[2]
        self.redraw()
        self.redo_stack.append(action)
        if len(self.undo_stack) == 0:
            self.set_modified(False)
        System.log(_("Undo: " + msg))

    # ---------------------------------------------------------------------
    def redo(self):
        """
        This method redo a modification.
        """
        if len(self.redo_stack) < 1:
            return
        self.set_modified(True)
        action = self.redo_stack.pop()
        self.blocks = action[0]
        self.connectors = action[1]
        msg = action[2]
        self.redraw()
        self.undo_stack.append(action)
        System.log(_("Redo: " + msg))

    # ---------------------------------------------------------------------
    def get_min_max(self):
        """
        This method get min and max.
            Returns

        """
        min_x = self.__main_window.get_size()[0]
        min_y = self.__main_window.get_size()[1]

        max_x = 0
        max_y = 0

        for block_id in self.blocks:
            block = self.blocks[block_id]
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
