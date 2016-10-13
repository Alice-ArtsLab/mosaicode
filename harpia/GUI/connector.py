# -*- coding: utf-8 -*-
# noqa: E402

import gi
import sys
import math
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GooCanvas
from connectormenu import ConnectorMenu
from harpia.model.connectionmodel import ConnectionModel


class Connector(GooCanvas.CanvasGroup, ConnectionModel):

    # ----------------------------------------------------------------------

    def __init__(self, diagram, source, source_port, conn_type):
        GooCanvas.CanvasGroup.__init__(self)
        ConnectionModel.__init__(self, diagram, source, source_port, conn_type)

        self.__from_point = self.source.get_output_pos(self.source_port)
        self.__to_point = (0, 0)

        self.__focus = False
        self.width = 0
        self.height = 0

        self.connect("button-press-event", self.__on_button_press)
        self.connect("enter-notify-event", self.__on_enter_notify)
        self.connect("leave-notify-event", self.__on_leave_notify)
        self.__widgets = {}

        self.update_tracking()

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def delete(self):
        self.get_diagram().delete_connection(self)
        self.get_diagram().update_flows()

    # ----------------------------------------------------------------------
    def __on_button_press(self, canvas_item, target_item, event):
        Gtk.Widget.grab_focus(self.get_diagram())
        if event.button.button == 3:
            ConnectorMenu(self, event)

        if self in self.get_diagram().current_widgets:
            self.get_diagram().current_widgets = []
        else:
            self.get_diagram().current_widgets.append(self)

        self.get_diagram().update_flows()
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
    def set_end(self, sink, sink_port):
        ConnectionModel.set_end(self, sink, sink_port)
        self.__to_point = sink.get_input_pos(self.sink_port)
        self.update_tracking(self.__to_point)

    # ----------------------------------------------------------------------
    def update_tracking(self, newEnd=None):
        if newEnd is None:
            newEnd = self.__from_point
        a = newEnd[0] - self.__from_point[0]
        b = newEnd[1] - self.__from_point[1]
        if a > 0:
            a -= 1
        else:
            a += 1

        if b > 0:
            b -= 1
        else:
            b += 1

        self.__to_point = self.__from_point[
            0] + a - 5, self.__from_point[1] + b
        self.__update_draw()

    # ----------------------------------------------------------------------
    def update_flow(self):
        self.__from_point = self.source.get_output_pos(self.source_port)
        self.__to_point = self.sink.get_input_pos(self.sink_port)
        self.__update_draw()

    # ----------------------------------------------------------------------
    def __update_draw(self):
        # svg M L bezier curve
        path = ""
        x0 = self.__from_point[0]
        y0 = self.__from_point[1]
        x1 = self.__to_point[0]
        y1 = self.__to_point[1]

        path += "M " + str(x0) + " " + str(y0)

        path += " L " + str(x0 + 25) + " " + str(y0)
        path += " L " + str(x0 + 25) + " " + str((y0 + y1) / 2)
        if x1 < x0 + 50:
            path += " L " + str((x1 + x0) / 2) + " " + str((y0 + y1) / 2)
            path += " L " + str(x1 - 25) + " " + str((y0 + y1) / 2)
        else:
            path += " L " + str(x0 + 25) + " " + str(y1)
        path += " L " + str(x1 - 25) + " " + str(y1)
        path += " L " + str(x1) + " " + str(y1)

        path += " L " + str(x1 - 4) + " " + str(y1 - 4)
        path += " L " + str(x1 - 4) + " " + str(y1 + 4)
        path += " L " + str(x1) + " " + str(y1)

        if not self.__widgets.has_key("Line"):
            widget = GooCanvas.CanvasPath(
                    parent = self,
                    data = path
                    )
            self.__widgets["Line"] = widget
        else:
            self.__widgets["Line"].set_property("data", path)

        self.__update_state()

    # ----------------------------------------------------------------------
    def __update_state(self):
        # With focus: line width = 3
        if self.__focus:
            self.__widgets["Line"].set_property("line-width", 3)
        else:
            self.__widgets["Line"].set_property("line-width", 2)

        # selected: line style = dashed and line width = 3
        if self in self.get_diagram().current_widgets:
            self.__widgets["Line"].set_property(
                "line_dash", GooCanvas.CanvasLineDash.newv((4.0, 2.0)))
        else:
            self.__widgets["Line"].set_property(
                "line_dash", GooCanvas.CanvasLineDash.newv((10.0, 0.0)))

        # not connected: Color = red
        if self.sink_port == -1:
            self.__widgets["Line"].set_property("stroke-color", "red")
        else:
            self.__widgets["Line"].set_property("stroke-color", "black")
