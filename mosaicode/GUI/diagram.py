# -*- coding: utf-8 -*-
"""
This module contains the Diagram class.
"""
import gi
from copy import deepcopy
from copy import copy
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GooCanvas
from block import Block
from connector import Connector
from comment import Comment
from mosaicode.system import System as System
from mosaicode.model.diagrammodel import DiagramModel
from mosaicode.model.blockmodel import BlockModel
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
        self.set_property("has-tooltip", True)  # Allow tooltip on elements
        self.set_property("background-color", "White")
        self.set_property("clear-background", True)
        Gtk.Widget.grab_focus(self)

        self.last_clicked_point = (None, None)
        self.main_window = main_window

        self.curr_connector = None

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

        self.show_grid = False
        self.select_rect = None
        self.__draw_grid()

        # Used for cycle detection
        self.show()

    # ----------------------------------------------------------------------
    def __on_motion_notify(self, canvas_item, event):
        scale = self.get_scale()
        # Select elements
        if self.select_rect is not None:
            self.__update_select(event.x / scale, event.y / scale)
            items = self.get_items_in_area(
                self.select_rect.bounds, True, False, True)
            for item in items:
                try:
                    item.is_selected = True
                except:
                    pass
            self.update_flows()
            return True  # Abort other events

        if event.state & Gdk.ModifierType.BUTTON1_MASK:
            for connector in self.connectors:
                connector.update_flow()

        if self.curr_connector is None:
            return False
        point = (event.x / scale, event.y / scale)
        self.curr_connector.update_flow(point)
        return False

    # ----------------------------------------------------------------------
    def __on_key_press(self, widget, event=None):
        grid = System.properties.grid
        modifier_mask = Gtk.accelerator_get_default_mod_mask()
        event.state = event.state & modifier_mask
        if event.state == Gdk.ModifierType.CONTROL_MASK:
            if event.keyval == Gdk.KEY_Up:
                self.move_selected(0, -grid*5)
                return True
            if event.keyval == Gdk.KEY_Down:
                self.move_selected(0, grid*5)
                return True
            if event.keyval == Gdk.KEY_Left:
                self.move_selected(-grid*5, 0)
                return True
            if event.keyval == Gdk.KEY_Right:
                self.move_selected(grid*5, 0)
                return True

        if event.keyval == Gdk.KEY_Delete:
            self.delete()
            return True

        if event.keyval == Gdk.KEY_Up:
            self.move_selected(0, -grid)
            return True
        if event.keyval == Gdk.KEY_Down:
            self.move_selected(0, grid)
            return True
        if event.keyval == Gdk.KEY_Left:
            self.move_selected(-grid, 0)
            return True
        if event.keyval == Gdk.KEY_Right:
            self.move_selected(grid, 0)
            return True

    # ----------------------------------------------------------------------
    def __on_button_release(self, widget, event=None):
        self.__end_select()

    # ----------------------------------------------------------------------
    def __on_button_press(self, widget, event=None):
        Gtk.Widget.grab_focus(self)
        if event.button == 1:
            self.last_clicked_point = (event.x, event.y)
            self.deselect_all()
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
                line_dash=GooCanvas.CanvasLineDash.newv((4.0, 4.0))
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
        block = self.main_window.main_control.get_selected_block()
        if block is not None:
            block.x = x
            block.y = y
            self.main_window.main_control.add_block(block)
        return

    # ----------------------------------------------------------------------
    def __valid_connector(self, newCon):
        """
        Parameters:

        Returns
             * **Types** (:class:`boolean<boolean>`)
        """
        for oldCon in self.connectors:
            if oldCon.input == newCon.input \
                    and oldCon.input_port == newCon.input_port\
                    and not newCon.port.multiple:
                System.log(_("Connector Already exists"))
                return False
        if (newCon.input == newCon.output) or self.__cycle_detection(newCon):
            System.log(_("Recursive connection is not allowed"))
            return False
        if newCon.input_port.type != newCon.output_port.type:
            System.log(_("Connection Types mismatch"))
            return False
        return True

    # ----------------------------------------------------------------------
    def __cycle_detection(self, newCon):
        marks = []
        marks.append(newCon.input.id)
        i = 0
        while i < len(marks):
            for connection in self.connectors:
                if connection.output.id != marks[i]:
                    continue
                if connection.input == newCon.output:
                    return True
                if connection.input.id not in marks:
                    marks.append(connection.input.id)
            i += 1
        return False

    # ----------------------------------------------------------------------
    def __abort_connection(self):
        if self.curr_connector is None:
            return
        connector_number = self.get_root_item().find_child(self.curr_connector)
        self.get_root_item().remove_child(connector_number)
        del self.curr_connector
        self.curr_connector = None

    # ----------------------------------------------------------------------
    def start_connection(self, block, port):
        """
        This method start a connection.

            Parameters:
                * **block**
                * **output**

        """
        self.__abort_connection()  # abort any possibly running connections
        self.curr_connector = Connector(self, block, port)
        self.get_root_item().add_child(self.curr_connector, -1)
        self.update_flows()

    # ----------------------------------------------------------------------
    def end_connection(self, block, port):
        """
        This method end a connection.

            Parameters:
                * **block**
                * **port**
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        if self.curr_connector is None:
            return False
        self.curr_connector.input = block
        self.curr_connector.input_port = port
        if not self.__valid_connector(self.curr_connector):
            self.__abort_connection()
            return False

        self.connectors.append(self.curr_connector)
        self.curr_connector = None
        self.update_flows()
        return True

    # ----------------------------------------------------------------------
    def __draw_grid(self):
        if self.show_grid:
            width = self.main_window.get_size()[0]
            height = self.main_window.get_size()[1]

            i = 0
            while i < height:
                GooCanvas.CanvasPath(
                        parent=self.get_root_item(),
                        stroke_color="#F9F9F9",
                        data="M 0 " + str(i) + " L "+ str(width) +" "+ str(i) + "",
                        line_width=0.8
                        )
                i = i + System.properties.grid
            i = 0
            while i < width:
                GooCanvas.CanvasPath(
                        parent=self.get_root_item(),
                        stroke_color="#F9F9F9",
                        data="M " + str(i) + " 0 L "+ str(i) + " "+ str(height) +"",
                        line_width=0.8
                        )
                i = i + System.properties.grid

    # ----------------------------------------------------------------------
    def set_show_grid(self, bool):
        if bool is not None:
            self.show_grid = bool

    # ----------------------------------------------------------------------
    def update_flows(self):
        """
        This method update flows.
        """
        self.update()
        for block_id in self.blocks:
            self.blocks[block_id].update_flow()
        for conn in self.connectors:
            conn.update_flow()
        for comment in self.comments:
            comment.update_flow()

    # ----------------------------------------------------------------------
    def set_file_name(self, file_name):
        """
        This method set name of diagram file.

            Parameters:
                * **file_name** (:class:`str<str>`)

        """
        self.file_name = file_name
        self.main_window.work_area.rename_diagram(self)

    # ----------------------------------------------------------------------
    def __apply_zoom(self):
        self.set_scale(self.zoom)
        self.update_flows()
        self.set_modified(True)

    # ----------------------------------------------------------------------
    def set_zoom(self, zoom):
        """
        This method set zoom.

            Parameters:
                * **zoom**
        """
        self.zoom = zoom
        self.__apply_zoom()

    # ----------------------------------------------------------------------
    def change_zoom(self, value):
        """
        This method change zoom.

            Parameters:
               * **value** (:class:`float<float>`)
        """
        zoom = self.zoom
        if value == System.ZOOM_ORIGINAL:
            zoom = System.ZOOM_ORIGINAL
        elif value == System.ZOOM_IN:
            zoom = zoom + 0.1
        elif value == System.ZOOM_OUT:
            zoom = zoom - 0.1
        self.zoom = zoom
        self.__apply_zoom()

    # ----------------------------------------------------------------------
    def show_commnent_property(self, comment):
        """
        This method show comment property.

            Parameters:
                * **block**(:class: `Block<mosaicode.GUI.block>`)
        """
        self.main_window.main_control.show_comment_property(comment)

    # ----------------------------------------------------------------------
    def show_block_property(self, block):
        """
        This method show block property.

            Parameters:
                * **block**(:class: `Block<mosaicode.GUI.block>`)
        """
        self.main_window.main_control.show_block_property(block)

    # ----------------------------------------------------------------------
    def resize(self, data):
        """
        This method resize diagram.

            Parameters:
               * **data**
        """
        value = self.main_window.get_size()[0]
        self.set_property("x2", value)

    # ----------------------------------------------------------------------
    def deselect_all(self):
        for key in self.blocks:
            self.blocks[key].is_selected = False
        for conn in self.connectors:
            conn.is_selected = False
        for comment in self.comments:
            comment.is_selected = False

    # ----------------------------------------------------------------------
    def select_all(self):
        """
        This method select all blocks in diagram.
        """
        for key in self.blocks:
            self.blocks[key].is_selected = True
        for conn in self.connectors:
            conn.is_selected = True
        for comment in self.comments:
            comment.is_selected = True
        self.update_flows()
        Gtk.Widget.grab_focus(self)

    # ----------------------------------------------------------------------
    def move_selected(self, x, y):
        """
        This method move selected blocks.

            Parameters:
                * **(x,y)** (:class:`float<float>`)

        """
        for key in self.blocks:
            if not self.blocks[key].is_selected:
                continue
            pos_x, pos_y = self.blocks[key].get_position()
            x, y = self.check_limit(x, y, pos_x, pos_y)
            self.blocks[key].move(x, y)

        for comment in self.comments:
            if not comment.is_selected:
                continue
            pos_x, pos_y = comment.get_position()
            x, y = self.check_limit(x, y, pos_x, pos_y)
            comment.move(x, y)
        self.update_flows()

    # ---------------------------------------------------------------------
    def check_limit(self, x, y, block_pos_x, block_pos_y):
        min_x = 0
        min_y = 0

        max_x, max_y = self.main_window.get_size()

        new_x = x + block_pos_x
        new_y = y + block_pos_y

        if new_x < min_x:
            x = min_x - block_pos_x
        elif new_x > max_x:
            x = max_x - block_pos_x

        if new_y < min_y:
            y = min_y - block_pos_y
        elif new_y > max_y:
            y = max_y - block_pos_y

        return x, y

    # ---------------------------------------------------------------------
    def paste(self):
        """
        This method paste a block.
        """
        replace = {}
        self.deselect_all()
        # interact into blocks, add blocks and change their id
        clipboard = self.main_window.main_control.get_clipboard()
        for widget in clipboard:
            if not isinstance(widget, Block):
                continue
            block = BlockModel(widget)
            block.x += 20
            block.y += 20
            block.id = -1
            if not self.main_window.main_control.add_block(block):
                return
            replace[widget.id] = block
            block.is_selected = True
        # interact into connections changing block ids
        for widget in clipboard:
            if not isinstance(widget, Connector):
                continue
            # if a connector is copied without blocks
            if widget.output.id not in replace or widget.input.id \
                    not in replace:
                continue
            output = replace[widget.output.id]
            output_port = widget.output_port
            input = replace[widget.input.id]
            input_port = widget.input_port
            self.start_connection(output, output_port)
            self.curr_connector.is_selected = True
            self.end_connection(input, input_port)
        self.update_flows()

    # ---------------------------------------------------------------------
    def copy(self):
        """
        This method copy a block.
        """
        self.main_window.main_control.reset_clipboard()
        for key in self.blocks:
            if not self.blocks[key].is_selected:
                continue
            self.main_window.main_control.get_clipboard().append(self.blocks[key])
        for conn in self.connectors:
            if not conn.is_selected:
                continue
            self.main_window.main_control.get_clipboard().append(conn)
        for comment in self.comments:
            if not comment.is_selected:
                continue
            self.main_window.main_control.get_clipboard().append(comment)

    # ---------------------------------------------------------------------
    def cut(self):
        """
        This method delete a block.
        """
        self.do(_("Cut"))
        self.self.copy()
        self.delete()

    # ---------------------------------------------------------------------
    def delete(self):
        """
        This method delete a block or connection.
        """
        self.do("Delete")
        for key in self.blocks.copy():
            if not self.blocks[key].is_selected:
                continue
            del self.blocks[key]
        for con in self.connectors:
            if not con.is_selected:
                continue
            if con not in self.connectors:
                continue
            self.connectors.remove(con)
        for comment in self.comments:
            if not comment.is_selected:
                continue
            self.comments.remove(comment)

        self.deselect_all()
        self.redraw()

    # ---------------------------------------------------------------------
    def set_modified(self, state):
        """
        This method set a modification.

            Parameters:
                * **state**
        """
        self.modified = state
        self.main_window.work_area.rename_diagram(self)

    # ---------------------------------------------------------------------
    def redraw(self):
        """
        This method redraw the diagram.
        """
        # First, remove all items from the diagram
        while self.get_root_item().get_n_children() != 0:
            self.get_root_item().remove_child(0)
        self.__draw_grid()

        # Check diagram content
        # Create Block widgets
        for key in self.blocks:
            block = self.blocks[key]
            if not isinstance(block, Block):
                block = Block(self, self.blocks[key])
                self.blocks[key] = block
        # Create Connection Widgets
        i = 0
        to_remove = []
        for connector in self.connectors:
            if not isinstance(connector, Connector):
                outb = self.blocks[connector.output.id]
                conn = Connector(self, outb, connector.output_port)
                conn.input = self.blocks[connector.input.id]
                conn.input_port = connector.input_port
                connector = conn
                self.connectors[i] = conn
            if connector.output.id not in self.blocks or connector.input.id not in self.blocks:
                to_remove.append(connector)
            i = i + 1
        for conn in to_remove:
            self.connectors.remove(conn)
        # Create Comment Widgets
        i = 0
        for comment in self.comments:
            if not isinstance(comment, Comment):
                comm = Comment(self)
                comm.set_text(comment.text)
                comm.move(comment.x, comment.y)
                self.comments[i] = comm
            i = i + 1

        # Redraw Blocks
        for key in self.blocks:
            block = self.blocks[key]
            if not isinstance(block, Block):
                block = Block(self, self.blocks[key])
                self.blocks[key] = block
            self.get_root_item().add_child(block, -1)
            block.adjust_position()
        i = 0

        # Redraw Connections
        for connector in self.connectors:
            if not isinstance(connector, Connector):
                outb = self.blocks[connector.output.id]
                conn = Connector(self, outb, connector.output_port)
                conn.input = self.blocks[connector.input.id]
                conn.input_port = connector.input_port
                connector = conn
                self.connectors[i] = conn
            self.get_root_item().add_child(connector, -1)
            i = i + 1

        # Redraw Comments
        for comment in self.comments:
            self.get_root_item().add_child(comment, -1)

        self.update_flows()

    # ---------------------------------------------------------------------
    def do(self, new_msg):
        """
        This method do something
            Parameters:
                * **new_msg** (:class:`str<str>`)
        """
        self.set_modified(True)
        action = (copy(self.blocks),    #0
                  copy(self.connectors),#1
                  copy(self.comments),  #2
                  new_msg)              #3
        self.undo_stack.append(action)

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
        self.comments = action[2]
        msg = action[3]
        self.redraw()
        self.redo_stack.append(action)
        if len(self.undo_stack) == 0:
            self.set_modified(False)

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
        self.comments = action[2]
        msg = action[3]
        self.redraw()
        self.undo_stack.append(action)

    # ----------------------------------------------------------------------
    def align(self, alignment):
        top = self.main_window.get_size()[1]
        bottom = 0
        left = self.main_window.get_size()[0]
        right = 0

        for key in self.blocks:
            if not self.blocks[key].is_selected:
                continue
            x, y = self.blocks[key].get_position()
            if top > y: top = y
            if bottom < y: bottom = y
            if left > x: left = x
            if right < x: right = x

        for key in self.blocks:
            if not self.blocks[key].is_selected:
                continue
            x, y = self.blocks[key].get_position()
            if alignment == "BOTTOM":
                self.blocks[key].move(0, bottom -y)
            if alignment == "TOP":
                self.blocks[key].move(0, top -y)
            if alignment == "LEFT":
                self.blocks[key].move(left -x, 0)
            if alignment == "RIGHT":
                self.blocks[key].move(right -x, 0)
        self.update_flows()

    # ----------------------------------------------------------------------
    def get_min_max(self):
        """
        This method get min and max.
            Returns

        """
        min_x = self.main_window.get_size()[0]
        min_y = self.main_window.get_size()[1]

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
    def show_block_menu(self, block, event):
        self.main_window.block_menu.show_block_menu(block, event)
# ----------------------------------------------------------------------
