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

from harpia import s2idirectory

import copy

WIDTH_2_TEXT_OFFSET = 22
WIDTH_DEFAULT = 112
HEIGHT_DEFAULT = 60
PORT_SENSITIVITY = 12
RADIUS = 15
INPUT_WIDTH = 24
INPUT_HEIGHT = 24
OUTPUT_HEIGHT = 24
OUTPUT_WIDTH = 24


class Block(GooCanvas.CanvasGroup):

#----------------------------------------------------------------------
    def __init__( self, diagram, plugin, block_id=1):
        GooCanvas.CanvasGroup.__init__(self)
        self.plugin = plugin
        self.plugin.id = block_id
        self.block_id = block_id
        self.diagram = diagram
        self.data_dir = os.environ['HARPIA_DATA_DIR']
        
        self.remember_x = 0
        self.remember_y = 0

        self.block_description = self.plugin.get_description()

        self.widgets = {}
        self.focus = False
        self.has_flow = False
        self.is_source = False

        if self.block_description.has_key("IsSource"): #all data sources
            self.is_source = self.block_description["IsSource"]

        self.width = WIDTH_DEFAULT

        maxIO = max(len(self.block_description["InTypes"]), len(self.block_description["OutTypes"]))

        ## Generates the block size, based on the number of inputs,outputs
        # Comment block is too small...
        if not maxIO:
            maxIO = 1

        self.height = max( ((maxIO-1)* 5 ) #espacamento entre ports = 5
                          +(RADIUS*2 ) #tirando a margem superior e inferior
                          +(maxIO * INPUT_HEIGHT),#adicionando a altura de cada port
                          HEIGHT_DEFAULT)

        self.build()
        self.set_parent(diagram.get_root_item())

        self.input_port_centers = []
        for inputPort in range(len(self.block_description["InTypes"])):
            self.input_port_centers.append((INPUT_WIDTH/2,
                     (RADIUS # upper border
                     + (inputPort*5) # spacing betwen ports
                     + inputPort*INPUT_HEIGHT #previous ports
                     + INPUT_HEIGHT/2)))#going to the port's center

        self.output_port_centers = []
        for outputPort in range(len(self.block_description["OutTypes"])):
            self.output_port_centers.append((self.width-(INPUT_WIDTH/2),
                     (RADIUS # upper border
                     + (outputPort*5) # spacing betwen ports
                     + outputPort*INPUT_HEIGHT #previous ports
                     + INPUT_HEIGHT/2)))#going to the port's center

        self.connect("button-press-event", self.__on_button_press)
        self.connect("motion-notify-event", self.__on_motion_notify)
        self.connect("enter-notify-event", self.__on_enter_notify)
        self.connect("leave-notify-event", self.__on_leave_notify)

#----------------------------------------------------------------------
    def __on_button_press(self, canvas_item, target_item, event):
        # with Shift
        if event.state == Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.MOD2_MASK:
            if self in self.diagram.current_widgets:
                self.diagram.current_widgets.remove(self)
            else:
                self.diagram.current_widgets.append(self)

        else:
            if self in self.diagram.current_widgets:
                self.diagram.current_widgets = []
            else:
                self.diagram.current_widgets = []
                self.diagram.current_widgets.append(self)

        self.diagram.show_block_property(self.plugin)

        Gtk.Widget.grab_focus(self.diagram)
        if event.button.button == 1:
            self.remember_x = event.x
            self.remember_y = event.y

        elif event.button.button == 3:
            BlockMenu(self, event)
            return True

        self.diagram.update_flows()

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
        for widget in self.diagram.current_widgets:
            if widget.__class__ == Block:
                widget.move(new_x, new_y)
        self.diagram.update_scrolling()
        return False

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
    def __del__(self):
        pass

#----------------------------------------------------------------------
    def __draw_rect(self):
        color = self.block_description["Color"].split(":")
        color = [int(color[0]), int(color[1]), int(color[2]), int(color[3])]
        color = int(color[0])*0x1000000 + \
                int(color[1])*0x10000 + \
                int(color[2])*0x100 + \
                int(color[3])*0x01
        rect = GooCanvas.CanvasRect(parent=self,
                    x=0,
                    y=0,
                    width=self.width,
                    height=self.height,
                    stroke_color="black",
                    fill_color_rgba=color
                    )
        self.widgets["Rect"] = rect

#----------------------------------------------------------------------
    def __draw_icon(self):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.data_dir + 
                self.block_description["Icon"])
        image = GooCanvas.CanvasImage(parent=self,
                pixbuf=pixbuf,
                x=(self.width/2) - (pixbuf.props.width / 2),
                y=(self.height/2)  - (pixbuf.props.height / 2)
                )
        self.widgets["Icon"] = image

#----------------------------------------------------------------------
    def __draw_inputs(self):
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
            image.connect("button-press-event", self.__on_input_press, x)
            image.connect("button-release-event", self.__on_input_release, x)
            ins.append(image)
        self.widgets["Inputs"] = ins

#----------------------------------------------------------------------
    def __on_input_press(self, canvas_item, target_item, event, args):
        self.diagram.clicked_input(self.block_id, args)
        return True

#----------------------------------------------------------------------
    def __on_input_release(self, canvas_item, target_item, event, args):
        return True

#----------------------------------------------------------------------
    def __draw_outputs(self):
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
    def __draw_label(self):
        text_label = "<span font_family ='Arial' size = '10000' weight = 'ultralight'> " + self.block_description["Label"] + "</span>"

        label = GooCanvas.CanvasText(parent=self,
                            text=text_label,
                            fill_color='black',
                            anchor=GooCanvas.CanvasAnchorType.CENTER,
                            x=(self.width/2),
                            y=(self.height-10),
                            use_markup=True
                            )

        text_width = label.get_property('width')
        oldX,oldY = ((self.width/2),(self.height-10))
        self.width = max(text_width + WIDTH_2_TEXT_OFFSET, self.width)
        label.translate((self.width / 2) - oldX, (self.height - 10) - oldY)
        self.widgets["Label"] = label

#----------------------------------------------------------------------
    def build(self):
        self.__draw_label()#must be called in this order! otherwise the box rect won't have the propper width
        self.__draw_rect()
        self.__draw_inputs()
        self.__draw_outputs()
        self.__draw_icon()
        self.update_flow()

#----------------------------------------------------------------------
    def update_flow(self):
        if self.is_source :#
            self.has_flow = True
        else:
            sourceConnectors = self.diagram.get_connectors_to(self.block_id)
            if len(sourceConnectors) != len(self.block_description["InTypes"]):
                self.has_flow = False
            else:
                self.has_flow = True
        self.__update_state()
        return self.has_flow

#----------------------------------------------------------------------
    def get_input_pos(self, input_id):
        isSet, x, y, scale, rotation = self.get_simple_transform()
        x = self.input_port_centers[input_id][0] + x - PORT_SENSITIVITY
        y = self.input_port_centers[input_id][1] + y - PORT_SENSITIVITY + 3
        return (x, y)

#----------------------------------------------------------------------
    def get_output_pos(self, output_id):
        x = self.output_port_centers[output_id][0] + self.get_simple_transform().x + PORT_SENSITIVITY
        y = self.output_port_centers[output_id][1] + self.get_simple_transform().y - PORT_SENSITIVITY + 3
        return (x,y)

#----------------------------------------------------------------------
    def get_state(self):
        return self.has_flow

#----------------------------------------------------------------------
    def move(self, x, y):
        self.diagram.set_modified(True)
        self.translate(x, y)

#----------------------------------------------------------------------
    def delete(self):
        self.diagram.delete_block(self.block_id)
        self.diagram.update_flows()

#----------------------------------------------------------------------
    def get_id(self):
        return self.block_id

#----------------------------------------------------------------------
    def get_type(self):
        return self.plugin.get_description()["Type"]

#----------------------------------------------------------------------
    def get_position(self):
        isSet, x, y, scale, rotation = self.get_simple_transform()
        return x,y

#----------------------------------------------------------------------
    def get_xml(self):
        return XMLParser(self.plugin.get_xml(), fromString=True)

#----------------------------------------------------------------------
    def set_xml(self, xml):
        properties = {}
        block_properties = xml.getTag("properties").getTag("block").getChildTags("property")
        for prop in block_properties:
            properties[prop.name] = prop.value
        self.plugin.set_properties(properties)

#----------------------------------------------------------------------
    def __update_state(self):
        # Not connected: Color = red
        if self.has_flow:
            self.widgets["Rect"].set_property("stroke_color",'black')
        else:
            self.widgets["Rect"].set_property("stroke_color",'red')

        # in focus: Line width = 3
        if self.focus:
            self.widgets["Rect"].set_property("line-width",3)
        else:
            self.widgets["Rect"].set_property("line-width",1)

        # selected: Line = dashed
        if self in self.diagram.current_widgets:
            self.widgets["Rect"].set_property("line_dash",GooCanvas.CanvasLineDash.newv((4.0, 2.0)))
        else:
            self.widgets["Rect"].set_property("line_dash",GooCanvas.CanvasLineDash.newv((10.0, 0.0)))

#----------------------------------------------------------------------
