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

#from connectormenu import ConnectorMenu
from harpia.utils.graphicfunctions import *

class Connector(GooCanvas.CanvasGroup):

#----------------------------------------------------------------------
    def __init__( self, diagram, from_block=-1, from_block_out=-1):
        GooCanvas.CanvasGroup.__init__(self)

        self.diagram = diagram
        self.from_block = from_block
        self.from_block_out = from_block_out
        self.from_point = self.diagram.blocks[self.from_block].get_output_pos(self.from_block_out) 

        self.to_point = (0,0)
        self.to_block = -1
        self.to_block_in = -1
        self.focus = False
        self.has_flow = False

#        self.group = self.diagram.root().add(self,x=0,y=0)
#        self.group.connect("event", self.__group_event)
#        self.group.set_flags(gtk.CAN_FOCUS)
        self.widgets = {}

        self.update_tracking()

#----------------------------------------------------------------------
    def __del__(self):
        pass

#----------------------------------------------------------------------
    def __group_event(self, widget, event=None):
        if event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                self.group.grab_focus()
                self.update_focus()
                return False
            elif event.button == 3:
                self.__right_click_run_menu(event)
        return False

#----------------------------------------------------------------------
    def __right_click_run_menu(self, a_oEvent):
#        GcdConnectorMenu(self, a_oEvent)
        pass

#----------------------------------------------------------------------
    def set_end(self, to_block=-1, to_block_in=-1):
        self.to_block = to_block
        self.to_block_in = to_block_in
        self.to_point = self.diagram.blocks[self.to_block].get_input_pos(self.to_block_in)
        self.update_tracking(self.to_point)

#----------------------------------------------------------------------
    def update_connectors(self):
        self.from_point = self.diagram.blocks[self.from_block].get_output_pos(self.from_block_out)
        self.to_point = self.diagram.blocks[self.to_block].get_input_pos(self.to_block_in)
        self.__update_draw()

#----------------------------------------------------------------------
    def update_tracking(self, newEnd=None):
        if newEnd == None:
            newEnd = self.from_point
        vec = Psub(newEnd,self.from_point)
        vec = CordModDec(vec)
        self.to_point = Psum(self.from_point,vec)
        self.__update_draw()

#----------------------------------------------------------------------
    def __update_draw(self):
        p = GooCanvas.CanvasPoints.new(4)
        p.set_point(0, self.from_point[0],self.from_point[1])
        p.set_point(1, (self.to_point[0] + self.from_point[0]) / 2, self.from_point[1])
        p.set_point(2, (self.to_point[0] + self.from_point[0]) / 2, self.to_point[1])
        p.set_point(3, self.to_point[0], self.to_point[1])

        if not self.widgets.has_key("Line"):
            widget = GooCanvas.CanvasPolyline(
                     parent=self,
                     points=p,
                     width=1.0,
                     start_arrow = True,
                     close_path = False
                     )
            self.widgets["Line"] = widget
        else:
            self.widgets["Line"].set_property("points",p)

#----------------------------------------------------------------------
    def update_focus(self):
        if self.diagram.get_property('focused-item') == self.group:
            self.focus = True
            self.widgets["Line"].set(fill_color='red',width_units=5.0)
        else:
            self.focus = False
            self.widgets["Line"].set(fill_color='black',width_units=3.0)

#----------------------------------------------------------------------
    def update_flow(self):
        self.has_flow = self.diagram.blocks[self.from_block].has_flow
        if self.has_flow:
            self.widgets["Line"].set_property("width",3.0)
        else:
            self.widgets["Line"].set_property("width",1.0)
        return self.has_flow
