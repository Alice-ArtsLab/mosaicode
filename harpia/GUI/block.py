# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the information about each block.
The block class is in this file.
"""
import gi
import os
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GooCanvas
from gi.repository import GdkPixbuf
from harpia.system import System as System
from harpia.GUI.blockmenu import BlockMenu
from harpia.model.blockmodel import BlockModel

WIDTH_2_TEXT_OFFSET = 22
WIDTH_DEFAULT = 112
HEIGHT_DEFAULT = 60
PORT_SENSITIVITY = 12
RADIUS = 15
INPUT_WIDTH = 24
INPUT_HEIGHT = 24
OUTPUT_HEIGHT = 24
OUTPUT_WIDTH = 24


class Block(GooCanvas.CanvasGroup, BlockModel):
    """
    This class contains the methods about blocks.
    """

    # ----------------------------------------------------------------------

    def __init__(self, diagram, plugin):
        """
        This method is the constuctor.
        """
        GooCanvas.CanvasGroup.__init__(self)
        BlockModel.__init__(self, plugin)
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
        Args:

        Returns:
            True(boolean): Indicates the button is pressed.
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
        Args:
        Returns:
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
        Args:
        Returns:
        """
        self.focus = True
        self.__update_state()
        return False

    # ----------------------------------------------------------------------
    def __on_leave_notify(self, canvas_item, target_item, event=None):
        """
        This method monitors the motion.
        Args:
        Returns:
        """
        self.focus = False
        self.__update_state()
        return False

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def __draw_rect(self):
        """
        This method draw a rectangle.
        Args:
            None
        Returns:
            None
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
        Args:
            None.
        Returns:
            None.
        """
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.data_dir +
                                                self.get_icon())
        image = GooCanvas.CanvasImage(parent=self,
                                      pixbuf=pixbuf,
                                      x=(self.width / 2) -
                                      (pixbuf.props.width / 2),
                                      y=(self.height / 2) -
                                      (pixbuf.props.height / 2)
                                      )
        self.widgets["Icon"] = image

    # ----------------------------------------------------------------------
    def __draw_inputs(self):
        """
        This method draw the inputs.
        Args:
            None.
        Returns:
            None.
        """
        ins = []
        x = 0
        for in_type in self.get_in_types():
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(
                    self.data_dir +
                    System.connectors[in_type]["icon_in"])
            except:
                pass

            image = GooCanvas.CanvasImage(parent=self,
                                          pixbuf=pixbuf,
                                          x=0,
                                          y=(RADIUS +  # upper border
                                             (x * 5) +  # spacing betwen ports
                                              x * INPUT_HEIGHT)  # prev ports
                                          )
            image.set_property("tooltip", in_type)
            image.connect("button-press-event", self.__on_input_press, x)
            image.connect("button-release-event", self.__on_input_release, x)
            ins.append(image)
            x += 1
        self.widgets["Inputs"] = ins

    # ----------------------------------------------------------------------
    def __on_input_press(self, canvas_item, target_item, event, args):
        """
        This method return true if a input was connected.
        Args:

        Returns:
            True(boolean): Indicates the input as connected.
        """
        self.diagram.end_connection(self, args)
        return True

    # ----------------------------------------------------------------------
    def __on_input_release(self, canvas_item, target_item, event, args):
        """
        This method monitors the input release.
        Args:

        Return:
            True(boolean)
        """
        return True

    # ----------------------------------------------------------------------
    def __draw_outputs(self):
        """
            This method draw the outputs.
            Args:
                None.
            Returns:
                None.
        """
        outs = []
        x = 0
        for out_type in self.get_out_types():
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(
                    self.data_dir +
                    System.connectors[out_type]["icon_out"])
            except:
                pass

            image = GooCanvas.CanvasImage(parent=self,
                                          pixbuf=pixbuf,
                                          x=(self.width - OUTPUT_WIDTH),
                                          y=(RADIUS +  # upper border
                                             (x * 5) +  # spacing betwen ports
                                              x * OUTPUT_HEIGHT)  # prev ports
                                          )
            image.set_property("tooltip", out_type)
            image.connect("button-press-event", self.__on_output_press, x)
            image.connect("button-release-event", self.__on_output_release, x)
            outs.append(image)
            x += 1
        self.widgets["Outputs"] = outs

    # ----------------------------------------------------------------------
    def __on_output_press(self, canvas_item, target_item, event, args):
        """
        This method monitors the output state, monitors if output was pressed.
        Args:
        Returns:
            None.
        """
        self.diagram.start_connection(self, args)
        return True

    # ----------------------------------------------------------------------
    def __on_output_release(self, canvas_item, target_item, event, args):
          """
        This method monitors the output state, monitors if output was release. 
        Args:
        Returns:
            boolean.
        """
        return True

    # ----------------------------------------------------------------------
    def __draw_label(self):
        """
        This method draw the label.
        Args:
        Returns:
            None
        """
        text_label = "<span font_family ='Arial' " + \
            "size = '10000' weight = 'ultralight'> " + \
            self.get_label() + "</span>"

        label = GooCanvas.CanvasText(parent=self,
                                     text=text_label,
                                     fill_color='black',
                                     anchor=GooCanvas.CanvasAnchorType.CENTER,
                                     x=(self.width / 2),
                                     y=(self.height - 10),
                                     use_markup=True
                                     )

        text_width = label.get_property('width')
        oldX, oldY = ((self.width / 2), (self.height - 10))
        self.width = max(text_width + WIDTH_2_TEXT_OFFSET, self.width)
        label.translate((self.width / 2) - oldX, (self.height - 10) - oldY)
        self.widgets["Label"] = label

    # ----------------------------------------------------------------------
    def rebuild(self):
        """
        This method rebuild the block.
        Args:
        Returns:
            None.
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
        Args:
        Returns:
            None
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
        Args:
        Returns:
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
        Args:
        Returns:
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
        Args:
        Returns:
        """
        self.translate(x, y)

    # ----------------------------------------------------------------------
    def delete(self):
        """
        This method delete a block.
        Args:
        Returns:
        """
        self.diagram.delete_block(self)
        self.diagram.update_flows()

    # ----------------------------------------------------------------------
    def get_position(self):
        """
        This method get position the block.
        Args:
        Returns:
        """
        isSet, x, y, scale, rotation = self.get_simple_transform()
        return x, y

    # ----------------------------------------------------------------------
    def set_properties(self, data):
        """
        This method set properties of each block.
        Args:
        Returns:
        """
        self.diagram.do("Set block property")
        BlockModel.set_properties(self, data)

    # ----------------------------------------------------------------------
    def get_properties(self):
        """
        This method get properties of each block.
        Args:
        Returns:
            Properties.
        """
        return BlockModel.get_properties(self)

    # ----------------------------------------------------------------------
    def update_flow(self):
        """
        This method update flow.
        Args:
        Returns:
            None
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
        Args:
            Self
        Returns:
            None
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
