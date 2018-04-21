# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the Block class.
"""
import gi
import os
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GooCanvas
from gi.repository import GdkPixbuf
from gi.repository import Pango
from mosaicode.system import System
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.port import Port

class Block(GooCanvas.CanvasGroup, BlockModel):
    """
    This class contains methods related the Block class
    """

    # ----------------------------------------------------------------------

    def __init__(self, diagram, block):
        """
        This method is the constuctor.
        """
        GooCanvas.CanvasGroup.__init__(self)
        BlockModel.__init__(self, block)

        self.diagram = diagram
        self.remember_x = 0
        self.remember_y = 0

        self.__widgets = {}
        self.focus = False
        self.has_flow = False
        self.is_selected = False

        self.width = 112

        self.connect("button-press-event", self.__on_button_press)
        self.connect("motion-notify-event", self.__on_motion_notify)
        self.connect("enter-notify-event", self.__on_enter_notify)
        self.connect("leave-notify-event", self.__on_leave_notify)
        self.move(int(float(self.x)), int(float(self.y)))

        self.height = self.__calculate_height()

        self.__draw_rect()
        self.__draw_label()
        self.__draw_ports()
        self.__draw_icon()
        self.update_flow()

    # ----------------------------------------------------------------------
    def __on_button_press(self, canvas_item, target_item, event):
        """
        This method monitors when the button is pressed.

            Parameters:
                canvas_item
            Returns:
                * **Types** (:class:`boolean<boolean>`)
                Indicates the button is pressed.
            """
        # with Shift
        if event.state == Gdk.ModifierType.SHIFT_MASK \
                | Gdk.ModifierType.MOD2_MASK:
            if self.is_selected:
                self.is_selected = False
            else:
                self.is_selected = True

        else:
            if not self.is_selected:
                self.diagram.deselect_all()
                self.is_selected = True

        self.diagram.show_block_property(self)

        Gtk.Widget.grab_focus(self.diagram)
        if event.button == 1:
            self.remember_x = event.x
            self.remember_y = event.y

        elif event.button == 3:
            self.diagram.show_block_menu(self, event)
            return True

        self.diagram.update_flows()
        return True

    # ----------------------------------------------------------------------
    def __on_motion_notify(self, canvas_item, target_item, event=None):
        """
        This method monitors the motion.

            Parameters:
                canvas_item
                target_item

            Returns:
                * **Types** (:class:`boolean<boolean>`)

        """
        if not event.state & Gdk.ModifierType.BUTTON1_MASK:
            return False
        if self.diagram.curr_connector is not None:
            return False
        # Get the new position and move by the difference
        new_x = event.x - self.remember_x
        new_y = event.y - self.remember_y
        self.diagram.move_selected(new_x, new_y)
        return False

    # ----------------------------------------------------------------------
    def __on_enter_notify(self, canvas_item, target_item, event=None):
        """
        This method monitors the motion.

            Parameters:
                canvas_item
            Returns:
                * **TYpes** (:class:`boolean<boolean>`)
        """
        self.focus = True
        self.__update_state()
        return False

    # ----------------------------------------------------------------------
    def __on_leave_notify(self, canvas_item, target_item, event=None):
        """
        This method monitors the motion.

            Parameters:
                canvas_item
                target_item

            Returns:
                * **Types** (:class:`boolean<boolean>`)

        """
        self.focus = False
        self.__update_state()
        return False

    # ----------------------------------------------------------------------
    def __draw_rect(self):
        """
        This method draw a rectangle.
        """
        rect = GooCanvas.CanvasRect(parent=self,
                                    x=0,
                                    y=10,
                                    width=self.width,
                                    height=self.height - 15,
                                    radius_x=10,
                                    radius_y=10,
                                    stroke_color="black",
                                    fill_color_rgba=self.get_color(),
                                    tooltip=self.label
                                    )
        self.__widgets["Rect"] = rect

    # ----------------------------------------------------------------------
    def __draw_icon(self):
        """
        This method draw a icon.
        """
        text_label = "<span font_family ='Arial' " + \
            "size = '25000' weight = 'bold' > " + \
            self.label.title()[0] + "</span>"

        icon = GooCanvas.CanvasText(parent=self,
                                    text=text_label,
                                    fill_color='white',
                                    anchor=GooCanvas.CanvasAnchorType.CENTER,
                                    x=(self.width / 2),
                                    y=(self.height / 2),
                                    use_markup=True,
                                    stroke_color='black',
                                    tooltip=self.label
                                    )

        self.__widgets["Icon"] = icon

    # ----------------------------------------------------------------------
    def __draw_label(self):
        """
        This method draw the label.

        """
        text_label = "<span font_family ='Arial' " + \
            "size = '10000' weight = 'normal'> " + \
            self.label + "</span>"

        label = GooCanvas.CanvasText(parent=self,
                                     text=text_label,
                                     fill_color='black',
                                     anchor=GooCanvas.CanvasAnchorType.CENTER,
                                     x=(self.width / 2),
                                     y=0,
                                     use_markup=True,
                                     stroke_color='black'
                                     )
        self.__widgets["Label"] = label

    # ----------------------------------------------------------------------
    def __create_ports_label(self, port):
        text_name = "<span font_family ='Arial' size = '7000' weight = 'ultralight'>" + \
            "<span color = '" + port.color + "'>"
        if self.is_collapsed:
            text_name += " - "
        else:
            text_name += "{" + port.hint + "}"
        text_name += "</span></span>"
        return text_name

    # ----------------------------------------------------------------------
    def __draw_ports(self):
        """        for port in self.ports:

        This method draws the ports.
        """
        for port in self.ports:
            text_name = self.__create_ports_label(port)
            x,y = self.__get_port_pos(port)
            if port.is_input():
                alignment = Pango.Alignment.LEFT
                anchor=GooCanvas.CanvasAnchorType.WEST
                press_event = self.__on_input_press
                release_event = self.__on_input_release
            else:
                alignment = Pango.Alignment.RIGHT
                anchor = GooCanvas.CanvasAnchorType.EAST
                press_event = self.__on_output_press
                release_event = self.__on_output_release

            text = GooCanvas.CanvasText(parent=self,
                                 text=text_name,
                                 fill_color='black',
                                 anchor=anchor,
                                 alignment=alignment,
                                 x=x,
                                 y=y,
                                 use_markup=True,
                                 tooltip=port.label
                                 )
            text.connect("button-press-event", press_event , port)
            text.connect("button-release-event", release_event, port)
            self.__widgets["port" + str(port)] = text

    # ----------------------------------------------------------------------
    def __on_input_press(self, canvas_item, target_item, event, port):
        """
        This method return true if a input was connected.

            Parameters:
                * **canvas_item**
                * **target_item**
                * **event**
            Returns:
                * **Types** (:class:`boolean<boolean>`): Indicates the input as connected.
        """
        self.diagram.end_connection(self, port)
        return True

    # ----------------------------------------------------------------------
    def __on_input_release(self, canvas_item, target_item, event, args):
        """
        This method monitors the input release.

            Parameters:
                * **canvas_item**
                * **target_item**
                * **event **
            Return:
                * **Types** (:class:`boolean<boolean>`)
        """
        return True

    # ----------------------------------------------------------------------
    def __on_output_press(self, canvas_item, target_item, event, port):
        """
        This method monitors the output state, monitors if output was pressed.

            Parameters:
                canvas_item
                target_item
                event
                args
            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        self.diagram.start_connection(self, port)
        return True

    # ----------------------------------------------------------------------
    def __on_output_release(self, canvas_item, target_item, event, args):
        """
        This method monitors the output state, monitors if output was release.

            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        return True

    # ----------------------------------------------------------------------
    def __get_port_pos(self, port):

        if self.is_collapsed:
            y = 16 + (port.type_index * 6)
        else:
            y = 26 + (port.type_index * 11)

        if port.is_input():
            x = 0
        else:
            x = self.width

        if not self.is_collapsed:
            return (x, y)

        if port.is_input():
            return (x + 36, y - 8)
        else:
            return (x - 25, y - 8)

    # ----------------------------------------------------------------------
    def get_port_pos(self, port):
        """
        This method get input position.

            Parameters:
                * **input_id**
            Returns:
                * **Types** (:class:`float<float>`)
        """
        x, y = self.get_position()
        x2, y2 = self.__get_port_pos(port)
        return x + x2, y + y2 + 1

    # ----------------------------------------------------------------------
    def __calculate_height(self):
        if self.is_collapsed:
            return max(((self.maxIO - 1) * 5) + (self.maxIO * 4), 40)
        else:
            return max(((self.maxIO) * 5) + 15 + (self.maxIO * 7), 50)

    # ----------------------------------------------------------------------
    def move(self, x, y):
        """
        This method move a block.

            Parameters:
                * **(x,y)** (:class:`float<float>`)
            Returns:
                * **Types** (:class:`float<float>`)
        """
        new_x = x - (x % System.properties.grid)
        new_y = y - (y % System.properties.grid)
        self.translate(new_x, new_y)

    # ----------------------------------------------------------------------
    def adjust_position(self):
        position = self.get_position()
        grid = System.properties.grid
        new_x = position[0] - position[0] % grid
        new_y = position[1] - position[1] % grid
        self.translate(new_x - position[0], new_y - position[1])

    # ----------------------------------------------------------------------
    def get_position(self):
        """
        This method get position the block.

             Returns:
                * **Types** (:class:`float<float>`)
        """
        isSet, x, y, scale, rotation = self.get_simple_transform()
        return x, y

    # ----------------------------------------------------------------------
    def set_properties(self, data):
        """
        This method set properties of each block.

            Parameters:
                * **data**
        """
        self.diagram.do("Set block property")
        BlockModel.set_properties(self, data)

    # ----------------------------------------------------------------------
    def get_properties(self):
        """
        This method get properties of each block.

            Returns:
                * **Types** ()
        """
        return BlockModel.get_properties(self)

    # ----------------------------------------------------------------------
    def update_flow(self):
        """
        This method update flow.

            Returns:
                * **Types** (:class:`boolean<boolean>`)
        """
        self.has_flow = True
        distinct_con = []
        for conn in self.diagram.connectors:
            if conn.input != self:
                continue
            if conn.input_port not in distinct_con:
                distinct_con.append(conn.input_port)
        in_count = 0
        for port in self.ports:
            if port.is_input():
                in_count += 1
        if len(distinct_con) < in_count:
            self.has_flow = False
        self.__update_state()
        return self.has_flow

    # ----------------------------------------------------------------------
    def __update_state(self):
        """
        This method update the Line state.
        """
        # Not connected: Color = red
        if self.has_flow:
            self.__widgets["Rect"].set_property("stroke_color", 'black')
        else:
            self.__widgets["Rect"].set_property("stroke_color", 'red')

        # in focus: Line width = 3
        if self.focus:
            self.__widgets["Rect"].set_property("line-width", 3)
        else:
            self.__widgets["Rect"].set_property("line-width", 1)

        # selected: Line = dashed
        if self.is_selected:
            self.__widgets["Rect"].set_property(
                "line_dash", GooCanvas.CanvasLineDash.newv((4.0, 2.0)))
        else:
            self.__widgets["Rect"].set_property(
                "line_dash", GooCanvas.CanvasLineDash.newv((10.0, 0.0)))

        self.height = self.__calculate_height()
        if self.is_collapsed:
            self.__widgets["Label"].set_property("visibility", GooCanvas.CanvasItemVisibility.INVISIBLE)
            self.__widgets["Rect"].set_property("width", self.width - 60)
            self.__widgets["Rect"].set_property("x", 35)
            self.__widgets["Rect"].set_property("y", 0)
            self.__widgets["Rect"].set_property("height", self.height - 10)
            self.__widgets["Icon"].set_property("y", (self.height - 10)/2)
            self.__widgets["Icon"].set_property("x", (self.width / 2) + 2)
            i = 0
            for port in self.ports:
                x,y = self.__get_port_pos(port)
                self.__widgets["port" + str(port)].set_property("x", x)
                self.__widgets["port" + str(port)].set_property("y", y)
                self.__widgets["port" + str(port)].set_property("text", self.__create_ports_label(port))
                i += 1
        else:
            self.__widgets["Label"].set_property("visibility", GooCanvas.CanvasItemVisibility.VISIBLE)
            self.__widgets["Rect"].set_property("width", self.width)
            self.__widgets["Rect"].set_property("x", 0)
            self.__widgets["Rect"].set_property("y", 10)
            self.__widgets["Rect"].set_property("height", self.height)
            self.__widgets["Icon"].set_property("y", (self.height + 20)/2)
            self.__widgets["Icon"].set_property("x", (self.width / 2))
            for port in self.ports:
                x,y = self.__get_port_pos(port)
                self.__widgets["port" + str(port)].set_property("x", x)
                self.__widgets["port" + str(port)].set_property("y", y)
                self.__widgets["port" + str(port)].set_property("text", self.__create_ports_label(port))

# ----------------------------------------------------------------------
