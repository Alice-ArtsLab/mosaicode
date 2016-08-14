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
#----------------------------------------------------------------------

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GooCanvas


import math
import sys

from connectormenu import ConnectorMenu

class Connector(GooCanvas.CanvasGroup):

#----------------------------------------------------------------------
    def __init__( self, diagram, from_block=-1, from_block_out=-1):
        GooCanvas.CanvasGroup.__init__(self)

        self.diagram = diagram
        self.from_block = from_block
        self.to_block = -1

        self.from_block_out = from_block_out
        self.to_block_in = -1

        self.from_point = self.diagram.blocks[self.from_block].get_output_pos(self.from_block_out) 
        self.to_point = (0,0)

        self.focus = False

        self.connect("button-press-event", self.__on_button_press)
        self.connect("enter-notify-event", self.__on_enter_notify)
        self.connect("leave-notify-event", self.__on_leave_notify)
        self.widgets = {}

        self.update_tracking()

#----------------------------------------------------------------------
    def __del__(self):
        pass

#----------------------------------------------------------------------
    def delete(self):
        self.diagram.delete_connection(self)
        self.diagram.update_flows()
        print "Fui deletado"

#----------------------------------------------------------------------
    def __on_button_press(self, canvas_item, target_item, event):
        Gtk.Widget.grab_focus(self.diagram)
        if event.button.button == 3:
            ConnectorMenu(self, event)

        if self in self.diagram.current_widgets:
            self.diagram.current_widgets = []
        else:
            self.diagram.current_widgets.append(self)

        self.diagram.update_flows()
        return True

#----------------------------------------------------------------------
    def __on_enter_notify(self, canvas_item, target_item, event=None):
        self.focus = True
        self.diagram.update_flows()
        return False

#----------------------------------------------------------------------
    def __on_leave_notify(self, canvas_item, target_item, event=None):
        self.focus = False
        self.diagram.update_flows()
        return False

#----------------------------------------------------------------------
    def set_end(self, to_block=-1, to_block_in=-1):
        self.to_block = to_block
        self.to_block_in = to_block_in
        self.to_point = self.diagram.blocks[self.to_block].get_input_pos(self.to_block_in)
        self.update_tracking(self.to_point)

#----------------------------------------------------------------------
    def __update_connectors(self):
        self.from_point = self.diagram.blocks[self.from_block].get_output_pos(self.from_block_out)
        self.to_point = self.diagram.blocks[self.to_block].get_input_pos(self.to_block_in)
        self.__update_draw()

#----------------------------------------------------------------------
    def update_tracking(self, newEnd=None):
        if newEnd == None:
            newEnd = self.from_point
        a = newEnd[0] - self.from_point[0]
        b = newEnd[1] - self.from_point[1]
        if a > 0:
            a -= 1
        else:
            a += 1

        if b > 0:
            b -= 1
        else:
            b += 1

        self.to_point = self.from_point[0] + a, self.from_point[1] + b
        self.__update_draw()

#----------------------------------------------------------------------
    def __update_draw(self):
        # svg M L bezier curve
        path = ""
        x0 = self.from_point[0]
        y0 = self.from_point[1]
        x1 = self.to_point[0]
        y1 = self.to_point[1]

        path += "M " + str(x0) + " " + str(y0)
        path += " C " +  str((x1 + x0) / 2) + " " + str(y0)
        path += " " + str((x1 + x0) / 2) + " " + str(y1)
        path += " " + str(x1) + " " + str(y1)

        path += "L " + str(x1 - 3) + " " + str(y1 - 3)
        path += "L " + str(x1 - 3) + " " + str(y1 + 3)
        path += "L " + str(x1) + " " + str(y1)

        if not self.widgets.has_key("Line"):
            widget = GooCanvas.CanvasPath(
                    parent = self,
                    data = path
            )
            self.widgets["Line"] = widget

        else:
            self.widgets["Line"].set_property("data",path)

        self.__update_state()

#----------------------------------------------------------------------
    def update_flow(self):
        self.__update_connectors()

#----------------------------------------------------------------------
    def __update_state(self):
        if self.focus:
            self.widgets["Line"].set_property("line-width",3)
        else:
            self.widgets["Line"].set_property("line-width",2)

        if self in self.diagram.current_widgets:
            self.widgets["Line"].set_property("line_dash",GooCanvas.CanvasLineDash.newv((1.0, 1.0)))
        else:
            self.widgets["Line"].set_property("line_dash",GooCanvas.CanvasLineDash.newv((10.0, 0.0)))

        if  self.to_block_in == -1:
            self.widgets["Line"].set_property("stroke-color","red")
        else:
            self.widgets["Line"].set_property("stroke-color","black")

