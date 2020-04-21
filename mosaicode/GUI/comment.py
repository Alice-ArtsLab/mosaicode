# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the Block class.
"""
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GooCanvas
from gi.repository import Pango
from mosaicode.system import System
from mosaicode.model.commentmodel import CommentModel

class Comment(GooCanvas.CanvasText, CommentModel):
    """
    This class contains methods related the Block class
    """

    # ----------------------------------------------------------------------

    def __init__(self, diagram, comment):
        """
        This method is the constuctor.
        """
        GooCanvas.CanvasText.__init__(self)
        CommentModel.__init__(self, comment)

        self.diagram = diagram

        self.remember_x = 0
        self.remember_y = 0

        self.is_selected = False
        self.focus = False

        self.connect("button-press-event", self.__on_button_press)
        self.connect("motion-notify-event", self.__on_motion_notify)
        # Mouse over
        self.connect("enter-notify-event", self.__on_enter_notify)
        self.connect("leave-notify-event", self.__on_leave_notify)
        self.move(int(float(self.x)), int(float(self.y)))

        self.__update()

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

        self.diagram.show_comment_property(self)

        Gtk.Widget.grab_focus(self.diagram)
        if event.button == 1:
            self.remember_x = event.x
            self.remember_y = event.y

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
    def update_flow(self):
        self.__update()
        self.__update_state()

    # ----------------------------------------------------------------------
    def __update(self):
        """
        This method draw the label.

        """
        text_label = "<span font_family ='Arial' " + \
            "size = '10000' weight = 'ultralight'>" + \
            self.get_properties()[0]["value"] + "</span>"

        self.set_property("text", text_label)
        self.set_property("fill_color", 'black')
        self.set_property("stroke_color", 'black')
        self.set_property("line_dash", GooCanvas.CanvasLineDash.newv((4.0, 2.0)))
        self.set_property("use_markup", True)

    # ----------------------------------------------------------------------
    def move(self, x, y):
        """
        This method move a block.

            Parameters:
                * **(x,y)** (:class:`float<float>`)
            Returns:
                * **Types** (:class:`float<float>`)
        """
        new_x = x - (x % System.get_preferences().grid)
        new_y = y - (y % System.get_preferences().grid)
        self.translate(new_x, new_y)

    # ----------------------------------------------------------------------
    def adjust_position(self):
        position = self.get_position()
        grid = System.get_preferences().grid
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
        CommentModel.set_properties(self, data)

    # ----------------------------------------------------------------------
    def get_properties(self):
        """
        This method get properties of each block.

            Returns:
                * **Types** ()
        """
        return CommentModel.get_properties(self)

    # ----------------------------------------------------------------------
    def __update_state(self):
        """
        This method update the Line state.
        """
        if self.focus:
            self.set_property("fill_color", 'red')
        else:
            self.set_property("fill_color", 'black')

        if self.is_selected:
            text_label = "<span font_family ='Arial' background='#CCC' " + \
                    "size = '10000' weight = 'ultralight'>" + \
                    self.get_properties()[0]["value"] + "</span>"
            self.set_property("text", text_label)
        else:
            text_label = "<span font_family ='Arial' background='#FFF'" + \
                    "size = '10000' weight = 'ultralight'>" + \
                    self.get_properties()[0]["value"] + "</span>"
            self.set_property("text", text_label)

# ----------------------------------------------------------------------
