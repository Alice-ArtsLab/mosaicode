# -*- coding: utf-8 -*-
# noqa: E402
"""
This module contains the Connector class.
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk
from gi.repository import GooCanvas
from connectormenu import ConnectorMenu
from mosaicode.GUI.block import *
from mosaicode.model.connectionmodel import ConnectionModel
from mosaicode.system import System as System

class Connector(GooCanvas.CanvasGroup, ConnectionModel):
    """
    This class contains the methods related to Connector class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, diagram, output, output_port):
        """
        This method is the constructor.
        """
        GooCanvas.CanvasGroup.__init__(self)
        ConnectionModel.__init__(self, diagram, output, output_port)

        self.__from_point = (0,0)
        self.__to_point = (0, 0)

        self.__focus = False
        self.is_selected = False
        self.width = 0
        self.height = 0

        self.connect("button-press-event", self.__on_button_press)
        self.connect("enter-notify-event", self.__on_enter_notify)
        self.connect("leave-notify-event", self.__on_leave_notify)
        self.__widgets = {}

        self.update_flow()

    # ----------------------------------------------------------------------
    def __on_button_press(self, canvas_item, target_item, event):
        """
        This method monitors if on button was pressed.
        """
        Gtk.Widget.grab_focus(self.diagram)
        if event.button == 3:
            ConnectorMenu(self, event)

        if self.is_selected:
            self.diagram.deselect_all()
        else:
            self.diagram.deselect_all()
            self.is_selected = True

        self.diagram.update_flows()
        return True

    # ----------------------------------------------------------------------
    def __on_enter_notify(self, canvas_item, target_item, event=None):
        self.__focus = True
        self.__update_state()
        return False

    # ----------------------------------------------------------------------
    def __on_leave_notify(self, canvas_item, target_item, event=None):
        self.__focus = False
        self.__update_state()
        return False

    # ----------------------------------------------------------------------
    def update_flow(self, newEnd=None):
        """
        This method update Tracking.

            Parameters:
                * **newEnd**
        """
        self.__from_point = self.output.get_port_pos(self.output_port)

        if self.input is None:
            if newEnd is None:
                newEnd = self.__from_point
            a = newEnd[0] - self.__from_point[0]
            b = newEnd[1] - self.__from_point[1]
            a = a - 1 if a > 0 else a + 1
            b = b - 1 if b > 0 else b + 1
            self.__to_point = self.__from_point[0] + a - 5, self.__from_point[1] + b
        else:
            self.__to_point = self.input.get_port_pos(self.input_port)

        self.__update_draw()

    # ----------------------------------------------------------------------
    def __update_draw(self):
        """
        This method update draw.
        """
        path = ""
        x0 = self.__from_point[0]
        y0 = self.__from_point[1]
        x1 = self.__to_point[0]
        y1 = self.__to_point[1]

        if System.properties.connection == "Curve":
            c1x = x1
            c1y = y0
            c2x = x0
            c2y = y1
            path += "M " + str(x0) + " " + str(y0) 
            path += " C" 
            if x0 + 25 > x1:
                c1x = x0 + x0 - x1
                c2x = x1 - x0 + x1
            path += " " + str(c1x) + " " + str(c1y)
            path += " " + str(c2x) + " " + str(c2y)
            path += " " + str(x1) + " " + str(y1)

        elif System.properties.connection == "Line":
            path += "M " + str(x0) + " " + str(y0) 
            path += " L " + str(x1) + " " + str(y1)


        else: # System.properties.connection == "Square":
            x0_shift = (self.output_port.type_index * 4)
            x1_shift = 0
            if self.input_port is not None:
                x1_shift = self.input_port.type_index * 4

            # svg M L bezier curve
            # Move to output port starting point / first horizontal line
            path += "M " + str(x0) + " " + str(y0) 
            # Line to start point + 25 on x + output type index --
            path += " L " + str(x0 + 25 + x0_shift) + " " + str(y0)
            # First vertical line
            path += " L " + str(x0 + 25 + x0_shift) + " " + str((y0 + y1) / 2)

            # Middle horizontal line if second block is on the left
            if x1 - 25 - x1_shift < x0 + 25 + x0_shift:
                path += " L " + str((x1 + x0) / 2 - x1_shift) + " " + str((y0 + y1) / 2)
                path += " L " + str(x1 - 25 - x1_shift) + " " + str((y0 + y1) / 2)
            else:
                path += " L " + str(x0 + 25 + x0_shift) + " " + str(y1)

            path += " L " + str(x1 - 25 - x1_shift) + " " + str(y1)
            # End Point
            path += " L " + str(x1) + " " + str(y1)


        if "Line" not in self.__widgets:
            color = self.output_port.color
            widget = GooCanvas.CanvasPath(
                parent=self,
                stroke_color = color,
                data=path
            )
            self.__widgets["Line"] = widget
        else:
            self.__widgets["Line"].set_property("data", path)

        self.__update_state()

    # ----------------------------------------------------------------------
    def __update_state(self):
        """
        This method update the connector state.
        """

        # With focus: line width = 3
        if self.__focus:
            self.__widgets["Line"].set_property("line-width", 2)
        else:
            self.__widgets["Line"].set_property("line-width", 1)

        # selected: line style = dashed and line width = 3
        if self.is_selected:
            self.__widgets["Line"].set_property(
                "line_dash", GooCanvas.CanvasLineDash.newv((4.0, 2.0)))
        else:
            self.__widgets["Line"].set_property(
                "line_dash", GooCanvas.CanvasLineDash.newv((10.0, 0.0)))

