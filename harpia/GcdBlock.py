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

import pango
import gtk
import math
import gnomecanvas
import os

from GcdBlockMenu import GcdBlockMenu
import s2idirectory
import s2iblockpropertiesgui
from utils.XMLUtils import XMLParser

import copy

WIDTH_2_TEXT_OFFSET = 22
WIDTH_DEFAULT = 112
HEIGHT_DEFAULT = 56

PORT_SENSITIVITY = 12

class GcdBlock( gnomecanvas.CanvasGroup):

    def __init__( self, diagram, a_nBlockType, a_nBlockCountId=1):#a_nInputs, a_nOutputs, a_nBlockType ):

        self.m_nBlockType = a_nBlockType
        self.ParentDiagram = diagram
        self.m_sDataDir = os.environ['HARPIA_DATA_DIR']
        if s2idirectory.block.has_key(a_nBlockType):
            self.m_oDictBlock = s2idirectory.block[a_nBlockType] #a_oDictBlock
        else:
            self.m_oDictBlock = s2idirectory.block[0] #a_oDictBlock
            print "Bad block type.. assuming 00"

        self.m_nBlockCountId = a_nBlockCountId
        self.widgets = {}
        self.m_bFocus = False
        self.m_bHasFlow = False
        self.m_bTimeShifts = False
        self.m_bIsSource = False

        if self.m_oDictBlock.has_key("IsSource"): #all data sources
            self.m_bIsSource = self.m_oDictBlock["IsSource"]

        if self.m_oDictBlock.has_key("TimeShifts"): #delay block
            self.m_bTimeShifts = self.m_oDictBlock["TimeShifts"]

        self.m_oPropertiesXML = XMLParser(self.m_sDataDir+str(self.m_oDictBlock["Path"]["Xml"]))
        self.m_oPropertiesXML.getTag("properties").getTag("block").setAttr("id",str(self.m_nBlockCountId))


        self.m_oBorderColor = [ 0, 0, 0, 255 ]
        self.m_oBackColor = [0,0,0,150]
        self.m_nRadius = 15
        self.m_nInputHeight = 24
        self.m_nInputWidth = 24
        self.m_nOutputHeight = 24
        self.m_nOutputWidth = 24
        self.inputPortCenters = []
        self.outputPortCenters = []
        self.width = WIDTH_DEFAULT
        self.TextWidth = self.width - WIDTH_2_TEXT_OFFSET

        t_nMaxIO = max(len(self.m_oDictBlock["InTypes"]), len(self.m_oDictBlock["OutTypes"]))

        ## Generates the block size, based on the number of inputs,outputs
        # Comment block is too small...
        if not t_nMaxIO:
            t_nMaxIO = 1

        self.height = max( ((t_nMaxIO-1)* 5 ) #espacamento entre ports = 5
                                                +(self.m_nRadius*2 ) #tirando a margem superior e inferior
                                                +(t_nMaxIO * self.m_nInputHeight),#adicionando a altura de cada port
                                                 HEIGHT_DEFAULT)

        self.Label = self.m_oDictBlock["Label"]
        self.iconFile = self.m_sDataDir+self.m_oDictBlock["Icon"]

        self.__gobject_init__()
        self.wGroup = self.ParentDiagram.root().add(self,x=0,y=0)
        self.wGroup.connect("event", self.group_event)
        self.wGroup.set_flags(gtk.CAN_FOCUS)
        self.Build()

    def IsInput(self,event):#checks whether distance from any input center to the event position is less than PORT_SENSITIVITY
        clickedPoint = (event.x - self.wGroup.get_property('x'),event.y - self.wGroup.get_property('y'))
        inputPortCenters = []

        if len(self.inputPortCenters) == 0: #compute portCenters if they don't exist
            self.ComputeInputPorts()

        for pointIndex in range(len(self.inputPortCenters)):
            if Dist(self.inputPortCenters[pointIndex],clickedPoint) < PORT_SENSITIVITY:
                return pointIndex
        return -1

    def IsOutput(self,event):#checks whether distance from any input center to the event position is less than PORT_SENSITIVITY
        clickedPoint = (event.x - self.wGroup.get_property('x'),event.y - self.wGroup.get_property('y'))

        if len(self.outputPortCenters) == 0: #compute portCenters if they don't exist
            self.ComputeOutputPorts()

        for pointIndex in range(len(self.outputPortCenters)):
            if Dist(self.outputPortCenters[pointIndex],clickedPoint) < PORT_SENSITIVITY:
                return pointIndex
        return -1

    def ComputeOutputPorts(self):
        for outputPort in range(len(self.m_oDictBlock["OutTypes"])):
            self.outputPortCenters.append((self.width-(self.m_nInputWidth/2),  (self.m_nRadius # upper border
                     + (outputPort*5) # spacing betwen ports
                     + outputPort*self.m_nInputHeight #previous ports
                     + self.m_nInputHeight/2)))#going to the port's center

    def ComputeInputPorts(self):
        for inputPort in range(len(self.m_oDictBlock["InTypes"])):
            self.inputPortCenters.append((self.m_nInputWidth/2,  (self.m_nRadius # upper border
                     + (inputPort*5) # spacing betwen ports
                     + inputPort*self.m_nInputHeight #previous ports
                     + self.m_nInputHeight/2)))#going to the port's center

    def group_event(self, widget, event=None):
        if event.type == gtk.gdk.BUTTON_PRESS:
                if event.button == 1:
                    # Remember starting position.
                    # if event resolution got here, the diagram event resolution routine didn't matched with any ports.. so..
                    self.remember_x = event.x
                    self.remember_y = event.y

                    #Cascading event resolution:
                    t_nInput = self.IsInput(event)
                    if t_nInput <> -1:
                        self.ParentDiagram.ClickedInput(self.m_nBlockCountId,t_nInput)
                        return True
                    else:
                        t_nOutput = self.IsOutput(event)
                        if t_nOutput <> -1:
                            self.ParentDiagram.ClickedOutput(self.m_nBlockCountId,t_nOutput)
                            return True
                        else:
                            self.wGroup.grab_focus()
                            self.UpdateFocus()
                            #self.SetFocusedState(True)
                            #print("onBlock(" + str(event.x - self.wGroup.get_property('x')) + "," + str(event.y - self.wGroup.get_property('y')) + ")")
                            #print("Since this event does nothing, we should warn GcDiagram that any current opperations were aborted! or just return False!")
                            #self.ParentDiagram.AbortConnection()
                            return False
                    return False
                elif event.button == 3:
                    print "right button at block"
                    self.RightClick(event)
                    return True #explicitly returns true so that diagram won't catch this event
        elif event.type == gtk.gdk.MOTION_NOTIFY:
                if event.state & gtk.gdk.BUTTON1_MASK:
                    if self.ParentDiagram.m_oCurrConnector == None:
                        if(widget == self.wGroup):#make sure we're not moving somebody else!
                            # Get the new position and move by the difference
                            new_x = event.x
                            new_y = event.y
                            widget.move(new_x - self.remember_x, new_y - self.remember_y)

                            self.ParentDiagram.UpdateScrolling()

                            self.remember_x = new_x
                            self.remember_y = new_y
                            return False

        elif event.type == gtk.gdk._2BUTTON_PRESS:
            #Open up the block's options
            print("Open " + self.m_oDictBlock["Label"] + " props")
            GcdBlockMenu(self, event)
            return True

        elif event.type == gtk.gdk.ENTER_NOTIFY:
                # Make the outline wide.
                self.MouseOverState(True)
                return False #pode propagar p/ cima

        elif event.type == gtk.gdk.LEAVE_NOTIFY:
                # Make the outline thin.
                if not self.m_bFocus:
                    self.MouseOverState(False)
                return False #pode passar p/ cima

    def __del__(self):
        print "GC: deleting GcdBlock:",self.m_nBlockCountId

    def _BbRect(self):
        p = []

        m_oArc0 = MakeArc(radius=self.m_nRadius, edges=5, q=0)
        m_oArc1 = MakeArc(radius=self.m_nRadius, edges=5, q=1)
        m_oArc2 = MakeArc(radius=self.m_nRadius, edges=5, q=2)
        m_oArc3 = MakeArc(radius=self.m_nRadius, edges=5, q=3)

        pf = []
        #cw

        #linha superior.. p/ referencia
        pf.append((self.m_nRadius,0))
        pf.append((self.width-self.m_nRadius,0))
        pf.extend(AlterArc(m_oArc3,self.width-self.m_nRadius,self.m_nRadius))##canto superior direito
        pf.extend(AlterArc(m_oArc0,self.width-self.m_nRadius,self.height-self.m_nRadius))##canto inferior direito
        pf.extend(AlterArc(m_oArc1,self.m_nRadius,self.height-self.m_nRadius))##canto inferior esquerdo
        pf.extend(AlterArc(m_oArc2,self.m_nRadius,self.m_nRadius))##canto superior esquerdo

        p = []

        #takes a list of points(tuples)(pf) to produce a list of points in form [x1,y1,x2,y2,x3,y3....,xn,yn] (p)
        for n in pf:
            for e in n:
                p.append(e)
        #print self.m_oDictBlock["Color"].split(":")
        self.SetBackColor()
        w1 = self.wGroup.add(gnomecanvas.CanvasPolygon, points=p,# y1=y1, x2=x2, y2=y2,
                    fill_color_rgba=ColorFromList(self.m_oBackColor), outline_color='black',
                    width_units=1.0)
        #w1.set(dash=[1.0, 1, [0.1,0.1]])#set_dash( 1.0,(5.0,0.1) )
        self.widgets["Rect"] = w1

    def _BIcon(self):
        pb = gtk.gdk.pixbuf_new_from_file(self.m_sDataDir+self.m_oDictBlock["Icon"])
        icon = self.wGroup.add(gnomecanvas.CanvasPixbuf, pixbuf=pb,	x=(self.width/2),	y=(self.height/2), anchor=gtk.ANCHOR_CENTER)

        self.widgets["pb"] = icon

    def _BInputs(self):
        inPWids = []
        for x in range(len(self.m_oDictBlock["InTypes"])):
            try:
                pb = gtk.gdk.pixbuf_new_from_file(self.m_sDataDir+s2idirectory.typeIconsIn[self.m_oDictBlock["InTypes"][x]])
            except:
                pb = gtk.gdk.pixbuf_new_from_file(self.m_sDataDir+s2idirectory.icons["IconInput"])

            t_Wid = self.wGroup.add(gnomecanvas.CanvasPixbuf, pixbuf=pb,x=0,y=(self.m_nRadius # upper border
                              + (x*5) # spacing betwen ports
                              + x*self.m_nInputHeight), #previous ports
                              anchor=gtk.ANCHOR_NORTH_WEST)
            inPWids.append(t_Wid)
        self.widgets["Inputs"] = inPWids

    def _BOutputs(self):
        outPWids = []
        for x in range(len(self.m_oDictBlock["OutTypes"])):
            try:
                pb = gtk.gdk.pixbuf_new_from_file(self.m_sDataDir+s2idirectory.typeIconsOut[self.m_oDictBlock["OutTypes"][x]])
            except:
                pb = gtk.gdk.pixbuf_new_from_file(self.m_sDataDir+s2idirectory.icons["IconOutput"])
            t_Wid = self.wGroup.add(gnomecanvas.CanvasPixbuf, pixbuf=pb,x=(self.width-self.m_nOutputWidth),y=(self.m_nRadius # upper border
                      + (x*5) # spacing betwen ports
                      + x*self.m_nOutputHeight), #previous ports
                      anchor=gtk.ANCHOR_NORTH_WEST)
            outPWids.append(t_Wid)
        self.widgets["Outputs"] = outPWids

    def _BLabels(self):
        label = self.wGroup.add(gnomecanvas.CanvasText, text=self.m_oDictBlock["Label"],
                            fill_color='black', anchor=gtk.ANCHOR_CENTER,
                            weight=pango.WEIGHT_BOLD, size_points=9, x=(self.width/2), y=(self.height-10))
        self.TextWidth = label.get_property('text-width')
        oldX,oldY = ((self.width/2),(self.height-10))
        self.width = max(self.TextWidth+WIDTH_2_TEXT_OFFSET,self.width)
        label.move((self.width/2)-oldX, (self.height-10)-oldY)
        self.widgets["Label"] = label

    def Build(self):
        self._BLabels()#must be called in this order! otherwise the box rect won't have the propper width
        self._BbRect()
        self._BInputs()
        self._BOutputs()
        self._BIcon()
        self.UpdateFlow()
        self.UpdateFlowDisplay()


    def UpdateFlow(self,a_bCheckTimeShifter=False):
        if self.m_bIsSource or (self.m_bTimeShifts and (not a_bCheckTimeShifter)):#
            #if all in connectors have flow
            #print "Block ",self.Label," id(",self.m_nBlockCountId,") has flow"
            self.m_bHasFlow = True
        else:
            sourceConnectors = self.ParentDiagram.GetConnectorsTo(self.m_nBlockCountId)
            if len(sourceConnectors) <> len(self.m_oDictBlock["InTypes"]):
                #print "Block ",self.Label," id(",self.m_nBlockCountId,") doesnt has flow"
                self.m_bHasFlow = False
            else:
                for connIdx in reversed(range(len(sourceConnectors))):
                    if sourceConnectors[connIdx].m_bHasFlow:
                        sourceConnectors.pop(connIdx)
                if len(sourceConnectors) <> 0:
                    #print "Block ",self.Label," id(",self.m_nBlockCountId,") doesnt has flow"
                    self.m_bHasFlow = False
                else:
                    #print "Block ",self.Label," id(",self.m_nBlockCountId,") has flow"
                    self.m_bHasFlow = True

        return self.m_bHasFlow

    def ClickedInput(self, a_nInput):
        print "Input(" + str(a_nInput) + ")"

    def ClickedOutput(self, a_nOutput):
        print "Output(" + str(a_nOutput) + ")"

    def GetInputPos(self, a_nInputID):
        if len(self.inputPortCenters) == 0: #compute portCenters if they don't exist
            self.ComputeInputPorts()
        i_x,i_y = 0+self.wGroup.get_property('x'),self.inputPortCenters[a_nInputID][1]+self.wGroup.get_property('y')#x=0, y=yc
        wPoint = self.i2w(i_x,i_y)
        return (wPoint[0],wPoint[1])

    def GetOutputPos(self, a_nOutputID):
        if len(self.outputPortCenters) == 0: #compute portCenters if they don't exist
            self.ComputeOutputPorts()
        o_x,o_y = self.width+self.wGroup.get_property('x'),self.outputPortCenters[a_nOutputID][1]+self.wGroup.get_property('y')#x=0, y=yc
        wPoint = self.i2w(o_x,o_y)
        return (wPoint[0],wPoint[1])

    def GetBlockPos(self):
        return (self.wGroup.get_property('x'),self.wGroup.get_property('y'))

    def UpdateFocus(self):
        if self.ParentDiagram.get_property('focused-item') == self.wGroup:
            self.MouseOverState(True)
            self.m_bFocus = True
        else:
            self.MouseOverState(False)
            self.m_bFocus = False

    def UpdateFlowDisplay(self):
        t_oFocusCorrectedColor = [self.m_oBackColor[0],self.m_oBackColor[1],
                        self.m_oBackColor[2],self.m_oBackColor[3]]

        if self.m_bHasFlow:
            t_oFocusCorrectedColor[3] = self.m_oBackColor[3] #with focus: original colors
            self.widgets["Rect"].set(outline_color='black',fill_color_rgba=ColorFromList(t_oFocusCorrectedColor))
        else:
            t_oFocusCorrectedColor[3] = 50 #without focus the block background will be much more transparent
            self.widgets["Rect"].set(outline_color='red',fill_color_rgba=ColorFromList(t_oFocusCorrectedColor))

    def MouseOverState(self, a_bState):
        if a_bState:
            self.widgets["Rect"].set(width_units=3)
        else:
            self.widgets["Rect"].set(width_units=1)

    def RightClick(self, a_oEvent):
       GcdBlockMenu(self, a_oEvent)

    def GetState(self):
        return self.m_bHasFlow

    def SetPropertiesXML_nID( self, a_oPropertiesXML ):
        #myBlockId = self.m_oPropertiesXML.properties.block.id #storing this block's Block.Id
        myBlockId = self.m_oPropertiesXML.getTag("properties").getTag("block").getAttr("id") #storing this block's Block.Id

        self.m_oPropertiesXML = copy.deepcopy(a_oPropertiesXML)

        #self.m_oPropertiesXML.properties.block.id = myBlockId #restoring block.Id
        self.m_oPropertiesXML.getTag("properties").getTag("block").setAttr("id",myBlockId)

    def GetBorderColor(self,*args):
        return self.m_oBorderColor

    def GetBackColor(self,*args):
        return self.m_oBackColor

    def SetBackColor( self, a_nColors=None ):#RGBA
        if a_nColors == None:
            a_nColors = self.m_oDictBlock["Color"].split(":")
        t_nRed = int(a_nColors[0])
        t_nGreen = int(a_nColors[1])
        t_nBlue = int(a_nColors[2])
        t_nAlpha = int(a_nColors[3])
        self.m_oBackColor = [t_nRed, t_nGreen, t_nBlue, t_nAlpha]

        if self.widgets.has_key("Rect"): #rect already drawn
            self.widgets["Rect"].set(fill_color_rgba=ColorFromList(self.m_oBackColor))

    def Move(self, x, y):
        self.wGroup.move(x,y)

    def Redraw(self):
        self.wGroup.move(0,0)

    def SetBorderColor(self, a_nColor=None):
        print "SetBorderColor is deprecated, fix this"
        self.m_oBackColor = a_nColor

    def ToggleState(self,*args):
        print "ToggleState is deprecated, fix this"


    def GetPropertiesXML(self):
        return self.m_oPropertiesXML

    def SetPropertiesXML(self, outerProps):
        self.m_oPropertiesXML = outerProps

    def GetId(self):
        return self.m_nBlockCountId

    def GetType(self):
        return self.m_nBlockType

    def GetPos(self):
        return self.wGroup.get_property('x'),self.wGroup.get_property('y')

def Dist(p1,p2):
    return math.sqrt( math.pow(p2[0]-p1[0],2) + math.pow(p2[1]-p1[1],2))

def MakeArc(radius, edges, q=1):
    t_oPoints = []

    sin = math.sin
    cos = math.cos
    pi2 = (math.pi/2)
    for i in xrange(edges + 1):
        n = (pi2 * i) / edges + pi2*q
        t_oPoints.append((cos(n) * radius, sin(n) * radius))

    return t_oPoints

def AlterArc(arc, offsetx=0, offsety=0):
    return [(x+offsetx, y+offsety) for x, y in arc]

def ColorFromList(rgba):
    color = int(rgba[0])*0x1000000+int(rgba[1])*0x10000+int(rgba[2])*0x100+(int(rgba[3])*0x01)
    return color
