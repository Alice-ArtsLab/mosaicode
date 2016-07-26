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
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GooCanvas
from gi.repository import GdkPixbuf

import math
import os

from blockmenu import BlockMenu
import harpia.s2idirectory
from harpia.s2idirectory import *
from harpia.utils.XMLUtils import XMLParser
from harpia.utils.graphicfunctions import *

from harpia import s2idirectory

import copy

WIDTH_2_TEXT_OFFSET = 22
WIDTH_DEFAULT = 112
HEIGHT_DEFAULT = 56
PORT_SENSITIVITY = 12
RADIUS = 15
INPUT_WIDTH = 24
INPUT_HEIGHT = 24
OUTPUT_HEIGHT = 24
OUTPUT_WIDTH = 24


class Block(GooCanvas.CanvasGroup):

#----------------------------------------------------------------------
    def __init__( self, diagram, block_type, block_id=1):
        GooCanvas.CanvasGroup.__init__(self)
        self.block_type = block_type
        self.block_id = block_id
        self.diagram = diagram
        self.data_dir = os.environ['HARPIA_DATA_DIR']
        
        self.remember_x = 0
        self.remember_y = 0

        if s2idirectory.block.has_key(block_type):
            self.block_description = s2idirectory.block[block_type]
        else:
            self.block_description = s2idirectory.block[0]
            print "Bad block type.. assuming 00"

        self.widgets = {}
        self.focus = False
        self.has_flow = False
        self.time_shifts = False
        self.is_source = False

        if self.block_description.has_key("IsSource"): #all data sources
            self.is_source = self.block_description["IsSource"]

        if self.block_description.has_key("TimeShifts"): #delay block
            self.time_shifts = self.block_description["TimeShifts"]

        self.m_oPropertiesXML = XMLParser(self.data_dir +
                    str(self.block_description["Path"]["Xml"]))
        self.m_oPropertiesXML.getTag("properties").getTag("block").setAttr("id",str(self.block_id))

        self.m_oBorderColor = [ 0, 0, 0, 255 ]
        self.m_oBackColor = [0,0,0,150]
        self.input_port_centers = []
        self.output_port_centers = []
        self.width = WIDTH_DEFAULT

        t_nMaxIO = max(len(self.block_description["InTypes"]), len(self.block_description["OutTypes"]))

        ## Generates the block size, based on the number of inputs,outputs
        # Comment block is too small...
        if not t_nMaxIO:
            t_nMaxIO = 1

        self.height = max( ((t_nMaxIO-1)* 5 ) #espacamento entre ports = 5
                          +(RADIUS*2 ) #tirando a margem superior e inferior
                          +(t_nMaxIO * INPUT_HEIGHT),#adicionando a altura de cada port
                          HEIGHT_DEFAULT)

        self.build()
        self.set_parent(diagram.get_root_item())

        self.__compute_output_ports()
        self.__compute_input_ports()
        self.connect("button-press-event", self.__on_button_press)
        self.connect("motion-notify-event", self.__on_motion_notify)
        self.connect("enter-notify-event", self.__on_enter_notify)
        self.connect("leave-notify-event", self.__on_leave_notify)

#----------------------------------------------------------------------
    def __compute_output_ports(self):
        for outputPort in range(len(self.block_description["OutTypes"])):
            self.output_port_centers.append((self.width-(INPUT_WIDTH/2),
                     (RADIUS # upper border
                     + (outputPort*5) # spacing betwen ports
                     + outputPort*INPUT_HEIGHT #previous ports
                     + INPUT_HEIGHT/2)))#going to the port's center

#----------------------------------------------------------------------
    def __compute_input_ports(self):
        for inputPort in range(len(self.block_description["InTypes"])):
            self.input_port_centers.append((INPUT_WIDTH/2,
                     (RADIUS # upper border
                     + (inputPort*5) # spacing betwen ports
                     + inputPort*INPUT_HEIGHT #previous ports
                     + INPUT_HEIGHT/2)))#going to the port's center

#----------------------------------------------------------------------
    def __on_button_press(self, canvas_item, target_item, event):
        self.diagram.current_widget = self
        Gtk.Widget.grab_focus(self.diagram)
        if event.button.button == 1:
            self.remember_x = event.x
            self.remember_y = event.y
            self.update_focus()
            print "Button press"
            return False

        elif event.button.button == 3:
            BlockMenu(self, event)
            return True

        if event.type == Gdk.EventType._2BUTTON_PRESS:
            BlockMenu(self, event)
            return True

#----------------------------------------------------------------------
    def __on_motion_notify(self, canvas_item, target_item, event=None):
        if not event.state & Gdk.ModifierType.BUTTON1_MASK:
            return False
        if self.diagram.curr_connector != None:
            return False
        # Get the new position and move by the difference
        new_x = event.x - self.remember_x
        new_y = event.y - self.remember_y
        self.translate(new_x, new_y)
        self.diagram.update_scrolling()
        return False

#----------------------------------------------------------------------
    def __on_enter_notify(self, canvas_item, target_item, event=None):
        self.__mouse_over_state(True)
        return False

#----------------------------------------------------------------------
    def __on_leave_notify(self, canvas_item, target_item, event=None):
        if not self.focus:
            self.__mouse_over_state(False)
        return False

#----------------------------------------------------------------------
    def __del__(self):
        print "GC: deleting Block:",self.block_id

#----------------------------------------------------------------------
    def delete(self):
        self.diagram.delete_block(self.block_id)

#----------------------------------------------------------------------
    def _BbRect(self):
        color = self.block_description["Color"].split(":")
        back_color = [int(color[0]), int(color[1]), int(color[2]), int(color[3])]
        w1 = GooCanvas.CanvasRect(parent=self,
                    x=0,
                    y=0,
                    width=self.width,
                    height=self.width,
                    stroke_color="black",
                    fill_color_rgba=ColorFromList(back_color)
                    )
        self.widgets["Rect"] = w1

#----------------------------------------------------------------------
    def _BIcon(self):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.data_dir + 
                self.block_description["Icon"])
        image = GooCanvas.CanvasImage(parent=self,
                pixbuf=pixbuf,
                x=(self.width/2),
                y=(self.height/2))
        self.widgets["Icon"] = image

#----------------------------------------------------------------------
    def _BInputs(self):
        ins = []
        for x in range(len(self.block_description["InTypes"])):
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.data_dir + 
                            harpia.s2idirectory.typeIconsIn[
                            self.block_description["InTypes"][x]])
            except:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.data_dir + 
                            harpia.s2idirectory.icons["IconInput"])

            image = GooCanvas.CanvasImage(parent=self,
                        pixbuf=pixbuf,
                        x=0,
                        y=(RADIUS # upper border
                      + (x*5) # spacing betwen ports
                      + x*INPUT_HEIGHT) #previous ports
                       )
            image.connect("button-press-event", self.on_input_press, x)
            image.connect("button-release-event", self.__on_input_release, x)
            ins.append(image)
        self.widgets["Inputs"] = ins

#----------------------------------------------------------------------
    def on_input_press(self, canvas_item, target_item, event, args):
        self.diagram.clicked_input(self.block_id, args)
        print "On input press"
        return True

#----------------------------------------------------------------------
    def __on_input_release(self, canvas_item, target_item, event, args):
        return True

#----------------------------------------------------------------------
    def _BOutputs(self):
        outs = []
        for x in range(len(self.block_description["OutTypes"])):
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.data_dir + 
                            harpia.s2idirectory.typeIconsOut[
                            self.block_description["OutTypes"][x]])
            except:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.data_dir + 
                            harpia.s2idirectory.icons["IconOutput"])

            image = GooCanvas.CanvasImage(parent=self,
                        pixbuf=pixbuf,
                        x=(self.width-OUTPUT_WIDTH),
                        y=(RADIUS # upper border
                      + (x*5) # spacing betwen ports
                      + x*OUTPUT_HEIGHT) #previous ports
                        )
            image.connect("button-press-event", self.__on_output_press, x)
            image.connect("button-release-event", self.__on_output_release, x)
            outs.append(image)
        self.widgets["Outputs"] = outs

#----------------------------------------------------------------------
    def __on_output_press(self, canvas_item, target_item, event, args):
        self.diagram.clicked_output(self.block_id, args)
        return True

#----------------------------------------------------------------------
    def __on_output_release(self, canvas_item, target_item, event, args):
        return True

#----------------------------------------------------------------------
    def _BLabels(self):
        label = GooCanvas.CanvasText(parent=self,
                            text=self.block_description["Label"],
                            fill_color='black',
                            anchor=GooCanvas.CanvasAnchorType.CENTER,
                            x=(self.width/2),
                            y=(self.height-10))

        text_width = label.get_property('width')
        oldX,oldY = ((self.width/2),(self.height-10))
        self.width = max(text_width + WIDTH_2_TEXT_OFFSET,self.width)
        label.translate((self.width/2)-oldX, (self.height-10)-oldY)
        self.widgets["Label"] = label

#----------------------------------------------------------------------
    def build(self):
        self._BLabels()#must be called in this order! otherwise the box rect won't have the propper width
        self._BbRect()
        self._BInputs()
        self._BOutputs()
        self._BIcon()
        self.update_flow()
        self.__update_flow_display()

#----------------------------------------------------------------------
    def update_flow(self,check_time_shifter=False):
        if self.is_source or (self.time_shifts and (not check_time_shifter)):#
            self.has_flow = True
        else:
            sourceConnectors = self.diagram.get_connectors_to(self.block_id)
            if len(sourceConnectors) != len(self.block_description["InTypes"]):
                self.has_flow = False
            else:
#                for connIdx in reversed(range(len(sourceConnectors))):
#                    if sourceConnectors[connIdx].has_flow:
#                        sourceConnectors.pop(connIdx)
                if len(sourceConnectors) != 0:
                    self.has_flow = False
                else:
                    self.has_flow = True
        return self.has_flow

#----------------------------------------------------------------------
    def __update_flow_display(self):
        if self.has_flow:
            self.widgets["Rect"].set_property("stroke_color",'black')
        else:
            self.widgets["Rect"].set_property("stroke_color",'red')

#----------------------------------------------------------------------
    def get_input_pos(self, input_id):
        x = self.input_port_centers[input_id][0] + self.get_simple_transform().x - PORT_SENSITIVITY
        y = self.input_port_centers[input_id][1] + self.get_simple_transform().y - PORT_SENSITIVITY
        return (x, y)

#----------------------------------------------------------------------
    def get_output_pos(self, output_id):
        x = self.output_port_centers[output_id][0] + self.get_simple_transform().x + PORT_SENSITIVITY
        y = self.output_port_centers[output_id][1] + self.get_simple_transform().y - PORT_SENSITIVITY
        return (x,y)

#----------------------------------------------------------------------
    def update_focus(self):
        print "self.diagram.focused_item"
        if self.diagram.focused_item == self:
            self.__mouse_over_state(True)
            self.focus = True
            print "Focus"
        else:
            self.__mouse_over_state(False)
            self.focus = False
            print " NOt Focus"
#----------------------------------------------------------------------
    def __mouse_over_state(self, state):
        if state:
            self.widgets["Rect"].set_property("line-width",3)
        else:
            self.widgets["Rect"].set_property("line-width",1)
        pass

#----------------------------------------------------------------------
    def get_state(self):
        return self.has_flow

#----------------------------------------------------------------------
    def move(self, x, y):
        self.group.move(x,y)

#----------------------------------------------------------------------
    def redraw(self):
        self.group.move(0,0)

#----------------------------------------------------------------------
    def get_id(self):
        return self.block_id

#----------------------------------------------------------------------
    def get_type(self):
        return self.block_type

#----------------------------------------------------------------------
    def get_position(self):
        return self.get_simple_transform().x,self.get_simple_transform().y

#----------------------------------------------------------------------
    def GetPropertiesXML(self):
        return self.m_oPropertiesXML

#----------------------------------------------------------------------
    def SetPropertiesXML(self, outerProps):
        self.m_oPropertiesXML = outerProps

#----------------------------------------------------------------------
    def SetPropertiesXML_nID( self, a_oPropertiesXML ):
        myBlockId = self.m_oPropertiesXML.getTag("properties").getTag("block").getAttr("id")
        #storing this block's Block.Id
        self.m_oPropertiesXML = copy.deepcopy(a_oPropertiesXML)
        self.m_oPropertiesXML.getTag("properties").getTag("block").setAttr("id",myBlockId)

