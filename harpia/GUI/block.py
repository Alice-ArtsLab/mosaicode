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
from harpia.system import System as System
from harpia.GUI.blockmenu import BlockMenu
from harpia.model.plugin import Plugin

WIDTH_DEFAULT = 112
HEIGHT_DEFAULT = 60
PORT_SENSITIVITY = 12
RADIUS = 25
INPUT_WIDTH = 24
INPUT_HEIGHT = 12

class Block(GooCanvas.CanvasGroup, Plugin):
    """
    This class contains methods related the Block class
    """

    # ----------------------------------------------------------------------

    def __init__(self, diagram, plugin):
        """
        This method is the constuctor.
        """
        GooCanvas.CanvasGroup.__init__(self)
        Plugin.__init__(self, plugin)
        self.diagram = diagram
        self.data_dir = os.environ['HARPIA_DATA_DIR']

        self.remember_x = 0
        self.remember_y = 0

        self.widgets = {}
        self.focus = False
        self.has_flow = False

        self.width = WIDTH_DEFAULT
        self.build()

        self.connect("button-press-event", self.__on_button_press)
        self.connect("motion-notify-event", self.__on_motion_notify)
        self.connect("enter-notify-event", self.__on_enter_notify)
        self.connect("leave-notify-event", self.__on_leave_notify)
        self.move(self.x, self.y)

    # ----------------------------------------------------------------------
    def __on_button_press(self, canvas_item, target_item, event):
        """
        This method monitors the when the button is pressed.

            Parameters:
                canvas_item
            Returns:
                * **Types** (:class:`boolean<boolean>`)
                Indicates the button is pressed.
            """
        # with Shift
        if event.state == Gdk.ModifierType.SHIFT_MASK \
                | Gdk.ModifierType.MOD2_MASK:
            if self in self.diagram.current_widgets:
                self.diagram.current_widgets.remove(self)
            else:
                self.diagram.current_widgets.append(self)

        else:
            if self not in self.diagram.current_widgets:
                self.diagram.current_widgets = []
                self.diagram.current_widgets.append(self)

        self.diagram.show_block_property(self)

        Gtk.Widget.grab_focus(self.diagram)
        if event.button.button == 1:
            self.remember_x = event.x
            self.remember_y = event.y

        elif event.button.button == 3:
            BlockMenu(self, event)
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
        self.diagram.move_selected_blocks(new_x, new_y)
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
                                    y=0,
                                    width=self.width,
                                    height=self.height,
                                    radius_x=10,
                                    radius_y=10,
                                    stroke_color="black",
                                    fill_color_rgba=self.get_color()
                                    )
        self.widgets["Rect"] = rect

    # ----------------------------------------------------------------------
    def __draw_icon(self):
        """
        This method draw a icon.
        """
        text_label = "<span font_family ='Arial' " + \
            "size = '25000' weight = 'bold' > " + \
            self.get_label().title()[0] + "</span>"

        icon = GooCanvas.CanvasText(parent=self,
                                     text=text_label,
                                     fill_color='white',
                                     anchor=GooCanvas.CanvasAnchorType.CENTER,
                                     x=(self.width / 2),
                                     y=(self.height / 2),
                                     use_markup=True,
                                     stroke_color='black'
                                     )

        width = Pango.Rectangle()
        width2 = Pango.Rectangle()
        icon.get_natural_extents(width, width2)
        text_width = width2.width / 1000
        oldX, oldY = ((self.width / 2), (self.height / 2))
        self.width = max(text_width + 22, self.width)
        icon.translate((self.width / 2) - oldX, (self.height / 2) - oldY)
        self.widgets["Label"] = icon

#        pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.data_dir +
#                                                self.get_icon())
#        pixbuf = Gtk.IconTheme.get_default().load_icon(Gtk.stock_list_ids()[10],24,0)
#        image = GooCanvas.CanvasImage(parent=self,
#                                      pixbuf=pixbuf,
#                                      x=(self.width / 2) -
#                                      (pixbuf.props.width / 2),
#                                      y=(self.height / 2) -
#                                      (pixbuf.props.height / 2) + 10
#                                      )

#        self.widgets["Icon"] = image

    # ----------------------------------------------------------------------
    def __draw_label(self):
        """
        This method draw the label.

        """
        text_label = "<span font_family ='Arial' " + \
            "size = '10000' weight = 'ultralight'> " + \
            self.get_label() + "</span>"

        label = GooCanvas.CanvasText(parent=self,
                                     text=text_label,
                                     fill_color='black',
                                     anchor=GooCanvas.CanvasAnchorType.CENTER,
                                     x=(self.width / 2),
                                     y=(10),
                                     use_markup=True,
                                     stroke_color='black'
                                     )

        width = Pango.Rectangle()
        width2 = Pango.Rectangle()
        label.get_natural_extents(width, width2)
        text_width = width2.width / 1000
        oldX, oldY = ((self.width / 2), (self.height - 10))
        self.width = max(text_width + 22, self.width)
        label.translate((self.width / 2) - oldX, (self.height - 10) - oldY)
        self.widgets["Label"] = label

    # ----------------------------------------------------------------------
    def __draw_inputs(self):
        """
        This method draw the inputs.
        """
        ins = []
        x = 0
        for port_type in self.get_in_types():
            text_name = self.__get_port_label(port_type);
            inp = GooCanvas.CanvasText(parent=self,
                                 text=text_name,
                                 fill_color='black',
                                 anchor=GooCanvas.CanvasAnchorType.WEST,
                                 alignment = Pango.Alignment.LEFT,
                                 x=2,
                                 y=(RADIUS +  # upper border
                                     (x * 5) +  # spacing betwen ports
                                      x * INPUT_HEIGHT),  # prev ports
                                 use_markup=True
                                 )
            inp.set_property("tooltip", port_type)
            inp.connect("button-press-event", self.__on_input_press, x)
            inp.connect("button-release-event", self.__on_input_release, x)
            ins.append(inp)
            x += 1
        self.widgets["Inputs"] = ins

    # ----------------------------------------------------------------------
    def __on_input_press(self, canvas_item, target_item, event, args):
        """
        This method return true if a input was connected.

            Parameters:
                * **canvas_item**
                * **target_item**
                * **event**
            Returns:
                * **Types** (:class:`boolean<boolean>`): Indicates the input as connected.
        """
        self.diagram.end_connection(self, args)
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
    def __draw_outputs(self):
        """
        This method draw the outputs.
        """
        outs = []
        x = 0
        for port_type in self.get_out_types():
            text_name = self.__get_port_label(port_type);
            out = GooCanvas.CanvasText(parent=self,
                                 text=text_name,
                                 fill_color='black',
                                 anchor=GooCanvas.CanvasAnchorType.EAST,
                                 alignment = Pango.Alignment.RIGHT,
                                 x=(self.width - 1),
                                 y=(RADIUS +  # upper border
                                     (x * 5) +  # spacing betwen ports
                                      x * INPUT_HEIGHT),  # prev ports
                                 use_markup=True
                                 )

            out.set_property("tooltip", port_type)
            out.connect("button-press-event", self.__on_output_press, x)
            out.connect("button-release-event", self.__on_output_release, x)
            outs.append(out)
            x += 1
        self.widgets["Outputs"] = outs

    # ----------------------------------------------------------------------
    def __on_output_press(self, canvas_item, target_item, event, args):
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
        self.diagram.start_connection(self, args)
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
    def rebuild(self):
        """
        This method rebuild the block.
        """
        self.widgets = {}
        # remove all elements
        while self.get_root_item().get_n_children() != 0:
            self.get_root_item().remove_child(0)
        self.build()

    # ----------------------------------------------------------------------
    def build(self):
        """
        This method build the block.
        """
        maxIO = max(len(self.get_in_types()), len(self.get_out_types()))

        # Generates the block size, based on the number of inputs,outputs
        # Comment block is too small...
        if not maxIO:
            maxIO = 1

        self.height = max(((maxIO - 1) * 5) +  # espacamento entre ports = 5
                          (RADIUS * 2) +
                          # tirando a margem superior e inferior
                          (maxIO * INPUT_HEIGHT),
                          # adicionando a altura de cada port
                          HEIGHT_DEFAULT)

        self.__draw_label()
        self.__draw_rect()
        self.__draw_inputs()
        self.__draw_outputs()
        self.__draw_icon()
        self.update_flow()

    # ----------------------------------------------------------------------
    def get_input_pos(self, input_id):
        """
        This method get input position.

            Parameters:
                * **input_id**
            Returns:
                * **Types** (:class:`float<float>`)
        """
        isSet, x, y, scale, rotation = self.get_simple_transform()
        x = INPUT_WIDTH / 2 + x - PORT_SENSITIVITY
        y = (RADIUS +  # upper border
             (input_id * 5) +  # spacing betwen ports
             input_id * INPUT_HEIGHT +  # previous ports
             INPUT_HEIGHT / 2) + y - PORT_SENSITIVITY + 3
        return (x, y)

    # ----------------------------------------------------------------------
    def get_output_pos(self, output_id):
        """
        This method get output position.

            Parameters:
                * **output_id**
            Returns:
                * **Types** (:class:`float<float>`)

        """
        isSet, x, y, scale, rotation = self.get_simple_transform()
        x = self.width - (INPUT_WIDTH / 2) + x + PORT_SENSITIVITY
        y = (RADIUS +  # upper border
             (output_id * 5) +  # spacing betwen ports
             output_id * INPUT_HEIGHT +  # previous ports
             INPUT_HEIGHT / 2) + y - PORT_SENSITIVITY + 3
        return (x, y)

    # ----------------------------------------------------------------------
    def move(self, x, y):
        """
        This method move a block.

            Parameters:
                * **(x,y)** (:class:`float<float>`)
            Returns:
                * **Types** (:class:`float<float>`)
        """
        new_x = x - x % System.properties.get_grid()
        new_y = y - y % System.properties.get_grid()
        self.translate(new_x, new_y)

    # ----------------------------------------------------------------------
    def adjust_position(self):
        position = self.get_position()
        grid = System.properties.get_grid()
        new_x = position[0] - position[0] % grid
        new_y = position[1] - position[1] % grid
        self.translate(new_x - position[0], new_y - position[1])

    # ----------------------------------------------------------------------
    def delete(self):
        """
        This method delete a block.
        """
        self.diagram.delete_block(self)
        self.diagram.update_flows()

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
        Plugin.set_properties(self, data)

    # ----------------------------------------------------------------------
    def get_properties(self):
        """
        This method get properties of each block.

            Returns:
                * **Types** ()
        """
        return Plugin.get_properties(self)

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
            if conn.sink != self:
                continue
            if conn.sink_port not in distinct_con:
                distinct_con.append(conn.sink_port)
        if len(distinct_con) < len(self.get_in_types()):
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
            self.widgets["Rect"].set_property("stroke_color", 'black')
        else:
            self.widgets["Rect"].set_property("stroke_color", 'red')

        # in focus: Line width = 3
        if self.focus:
            self.widgets["Rect"].set_property("line-width", 3)
        else:
            self.widgets["Rect"].set_property("line-width", 1)

        # selected: Line = dashed
        if self in self.diagram.current_widgets:
            self.widgets["Rect"].set_property(
                "line_dash", GooCanvas.CanvasLineDash.newv((4.0, 2.0)))
        else:
            self.widgets["Rect"].set_property(
                "line_dash", GooCanvas.CanvasLineDash.newv((10.0, 0.0)))

    # ----------------------------------------------------------------------
    def __get_port_label(self, port_type):
        return \
            "<span font_family ='Arial' size = '7000' weight = 'ultralight'>{" + \
            "<span color = '" + \
            System.connectors[port_type].get_color() + "'>" + \
            System.connectors[port_type].get_label() + "</span>}</span>"
# ----------------------------------------------------------------------
