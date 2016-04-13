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

import gobject
import gtk
import math
import gnomecanvas
import sys

from GcdConnectorMenu import GcdConnectorMenu
from utils.graphicfunctions import *

class GcdConnector(gnomecanvas.CanvasGroup):

#----------------------------------------------------------------------
    def __init__( self, diagram, from_block=-1, from_block_out=-1):
        self.diagram = diagram
        self.from_block = from_block
        self.from_block_out = from_block_out
        self.from_point = self.diagram.blocks[self.from_block].get_output_pos(self.from_block_out) 
        self.to_point = (0,0)
        self.to_block = -1#a_nTo
        self.to_block_in = -1#a_nToIn
        self.focus = False
        self.has_flow = False

        self.__gobject_init__()

        self.group = self.diagram.root().add(self,x=0,y=0)
        self.group.connect("event", self.__group_event)
        self.group.set_flags(gtk.CAN_FOCUS)
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
        GcdConnectorMenu(self, a_oEvent)

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
        p = []
        p.append(self.from_point[0])
        p.append(self.from_point[1])

# Futuramente permitir linhas curvas
#        p.append((self.to_point[0] + self.from_point[0]) / 2)
#        p.append(self.from_point[1])

#        p.append((self.to_point[0] + self.from_point[0]) / 2)
#        p.append(self.to_point[1])

        p.append(self.to_point[0])
        p.append(self.to_point[1])
        if not self.widgets.has_key("Line"):
            widget = self.group.add(
                     gnomecanvas.CanvasLine,
                     points=p,
                     fill_color='black',
                     width_units=1.0,
                     first_arrowhead=False,
                     last_arrowhead=True,
                     arrow_shape_a=4.0,
                     arrow_shape_b=8.0,
                     arrow_shape_c=4.0,
                     smooth=True)
            self.widgets["Line"] = widget
        else:
            self.widgets["Line"].set(points=p)

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
            self.widgets["Line"].set(width_units=3.0)
        else:
            self.widgets["Line"].set(width_units=1.0)
        return self.has_flow
