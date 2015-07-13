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
import pango
import gtk
import math
import gnomecanvas
import sys

#sys.path.append('../bin')
#import s2idirectory

class GcdConnector( gnomecanvas.CanvasGroup):
	def __init__( self, diagram, a_nConnectorCountId=1, a_nFrom=-1, a_nFromOut=-1):#a_nInputs, a_nOutputs, a_nBlockType ):
		
		self.ParentDiagram = diagram
		
		self.m_nCountId = a_nConnectorCountId
		
		self.fromBlock = a_nFrom
		self.fromBlockOut = a_nFromOut
		
		self.fromPoint = self.ParentDiagram.m_oBlocks[self.fromBlock].GetOutputPos(self.fromBlockOut) #pegando o ponto verdadeiro de onde sai o conector

		self.ConnBoundary = 16.0

		self.toPoint = (0,0)
		
		self.toBlock = -1#a_nTo
		self.toBlockIn = -1#a_nToIn
		
		self.m_bFocus = False
		self.m_bHasFlow = False
		
		self.__gobject_init__()
		
		self.wGroup = self.ParentDiagram.root().add(self,x=0,y=0)
		self.wGroup.connect("event", self.group_event)
		
		self.wGroup.set_flags(gtk.CAN_FOCUS)
		
		self.widgets = {}
		
		self.Build()

	def __del__(self):
		print "GC: deleting GcdConnector:",self.m_nCountId

	def SetEnd(self, a_nTo=-1, a_nToIn=-1):
		self.toBlock = a_nTo
		self.toBlockIn = a_nToIn
		self.toPoint = self.ParentDiagram.m_oBlocks[self.toBlock].GetInputPos(self.toBlockIn) #pegando o ponto verdadeiro de onde sai o conector
		#print "Connected block"+str(self.fromBlock)+"_Out"+str(self.fromBlockOut)+" to block"+str(self.toBlock)+"_In"+str(self.toBlockIn)+" !!!"
		self.UpdateTracking(self.toPoint)

	def group_event(self, widget, event=None):
		if event.type == gtk.gdk.BUTTON_PRESS:
			if event.button == 1:
				self.wGroup.grab_focus()
				self.UpdateFocus()
				return False
			elif event.button == 3:
				self.RightClick(event)
		return False
	
	def LineDone(self):#, newEnd=None):
		self.wGroup.connect("event", self.group_event)
		#print "Line from ",self.fromPoint," to ", self.toPoint 
	
	def UpdateTracking(self, newEnd=None):
		if newEnd == None:
			newEnd = self.fromPoint
			
		vec = Psub(newEnd,self.fromPoint)
		vec = CordModDec(vec)
		newEnd = Psum(self.fromPoint,vec)
		
		self.toPoint = newEnd
		
		p = []
		p.append(self.fromPoint[0])
		p.append(self.fromPoint[1])
		p.append(self.toPoint[0])
		p.append(self.toPoint[1])
		
		if not self.widgets.has_key("Line"):
			w1 = self.wGroup.add(gnomecanvas.CanvasLine, points=p,fill_color='black',width_units=3.0,first_arrowhead=False,last_arrowhead=True,arrow_shape_a=4.0,arrow_shape_b=8.0,arrow_shape_c=4.0)
			wOut = self.wGroup.add(gnomecanvas.CanvasLine, points=p,fill_color_rgba=ColorFromList([0,0,0,0]),width_units=self.ConnBoundary,first_arrowhead=False,last_arrowhead=True,arrow_shape_a=4.0,arrow_shape_b=8.0,arrow_shape_c=4.0)

			self.widgets["Line"] = w1
			self.widgets["LineOut"] = wOut
		else:
			self.widgets["Line"].set(points=p)
			self.widgets["LineOut"].set(points=p)
	
		#self.UpdateFlow()
	
	def UpdateConnectors(self):
		
		self.fromPoint = self.ParentDiagram.m_oBlocks[self.fromBlock].GetOutputPos(self.fromBlockOut) #pegando o ponto verdadeiro de onde sai o conector
		self.toPoint = self.ParentDiagram.m_oBlocks[self.toBlock].GetInputPos(self.toBlockIn) #pegando o ponto verdadeiro de onde sai o conector
		p = []
		p.append(self.fromPoint[0])
		p.append(self.fromPoint[1])
		p.append(self.toPoint[0])
		p.append(self.toPoint[1])
		
		if not self.widgets.has_key("Line"):
			w1 = self.wGroup.add(gnomecanvas.CanvasLine, points=p,fill_color='black',width_units=3.0,first_arrowhead=False,last_arrowhead=True,arrow_shape_a=4.0,arrow_shape_b=8.0,arrow_shape_c=4.0)
			wOut = self.wGroup.add(gnomecanvas.CanvasLine, points=p,fill_color_rgba=ColorFromList([0,0,0,0]),width_units=self.ConnBoundary,first_arrowhead=False,last_arrowhead=True,arrow_shape_a=4.0,arrow_shape_b=8.0,arrow_shape_c=4.0)

			self.widgets["Line"] = w1
			self.widgets["LineOut"] = wOut
		else:
			self.widgets["Line"].set(points=p)
			self.widgets["LineOut"].set(points=p)
	
	def UpdateFocus(self):
		if self.ParentDiagram.get_property('focused-item') == self.wGroup:
			self.m_bFocus = True
			self.widgets["Line"].set(fill_color_rgba=ColorFromList([255,0,0,255]),width_units=5.0)
		else:
			self.m_bFocus = False
			self.widgets["Line"].set(fill_color='black',width_units=3.0)
	
	def Build(self):
		self.UpdateTracking()
		
	def UpdateFlow(self):
		self.m_bHasFlow = self.ParentDiagram.m_oBlocks[self.fromBlock].m_bHasFlow
		return self.m_bHasFlow

	def UpdateFlowDisplay(self):
		if self.m_bHasFlow:
			self.widgets["Line"].set(width_units=3.0)
		else:
			self.widgets["Line"].set(width_units=1.0)#(line_style=gtk.gdk.LINE_ON_OFF_DASH)

	def RightClick(self, a_oEvent):
		t_oMenu = gtk.Menu()
	
		t_oMenuItem = gtk.MenuItem("Properties")
		#t_oMenuItem.connect("activate", self.ShowPropertiesGUI )
		t_oMenu.append(t_oMenuItem)
		
		# Menu separator
		t_oMenuItem = gtk.SeparatorMenuItem()
		t_oMenu.append(t_oMenuItem)
		
		# Excluir (delete) item
		t_oMenuItem = gtk.MenuItem("Delete")
		t_oMenuItem.connect("activate", self.DeleteClicked )
		t_oMenu.append(t_oMenuItem)

		# Another separator
		t_oMenuItem = gtk.SeparatorMenuItem()
		t_oMenu.append(t_oMenuItem)
		# Shows the menu
		t_oMenu.show_all()
		t_oMenu.popup(None, None, None, a_oEvent.button, a_oEvent.time)

	def DeleteClicked(self, *args ): #this strongly depends on the garbage collector
		for connIdx in range(len(self.ParentDiagram.m_oConnectors)):
			if self.ParentDiagram.m_oConnectors[connIdx] == self:
				self.ParentDiagram.m_oConnectors.pop(connIdx)
				self.wGroup.destroy()
				break #faster, necessary (not iteraring on reverse!)

def Psub(p1,p0):
	return p1[0]-p0[0],p1[1]-p0[1]

def Psum(p1,p0):
	return p1[0]+p0[0],p1[1]+p0[1]

def CordModDec(Vector):
	ans = []
	for e in Vector:
		ans.append(e)
	
	for e in range(len(ans)):
		if ans[e] > 0:
			ans[e] -= 1
		else:
			ans[e] += 1
	
	return (ans[0],ans[1])
		
def ColorFromList(rgba):
	color = int(rgba[0])*0x1000000+int(rgba[1])*0x10000+int(rgba[2])*0x100+(int(rgba[3])*0x01)
	return color