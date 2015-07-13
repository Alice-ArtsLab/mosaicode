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

import gnomecanvas
import GcdBlock
import GcdBlock_Show
import GcdConnector
import gtk
import sys
import time

from exceptions import AttributeError

from amara import binderytools as bt
import s2idirectory

class GcDiagram( gnomecanvas.Canvas ):

	def __init__( self ):
		self.__gobject_init__()
		gnomecanvas.Canvas.__init__(self,aa=True)

		self.minWidth = 800
		self.minHeight = 600

		self.width = 800
		self.height = 600
		
		self.lastClickecPt = ( None, None)
		
		#self.set_size_request(self.width, self.height)
		self.set_scroll_region(0,0, self.width, self.height) #must be called everytime a block is moved or inserted with the new scroll region
		
		self.m_fPixels_per_unit = 1.0
		
		self.show()
		self.m_oBlocks = {}
		
		self.m_oConnectors = []
		
		self.m_oCurrConnector = None
		
		self.m_nSessionId = 0
		
		self.m_nBlockCountId = 1 #o primeiro bloco eh o n1 (incrementa a cada novo bloco
		self.m_nConnectorCountId = 1 #o primeiro conector eh o n1 (incrementa a cada novo conector
		
		self.set_flags(gtk.CAN_FOCUS)
		self.grab_focus()
		self.root().connect("event", self.canvas_root_event)#tem q ser o root() se nao ele pega os eventos antes de todu mundo! =]
		self.connect("event", self.canvas_event)#tem q ser o root() se nao ele pega os eventos antes de todu mundo! =]		
		
		self.m_sFilename = None
		
		self.m_sErrorLog = ""
		
		self.wbWidget = None
		self.UpdateWhiteBoard()
		
	def __del__(self):
		pass
	
	def canvas_event(self, widget, event=None):#nao serve pq QUALQUER EVENTO do canvas passa por aqui
		if self.m_oCurrConnector <> None:
			if event.type == gtk.gdk.MOTION_NOTIFY:#se temos um conector aberto, atualizar sua posicao
				t_Point = self.window_to_world(event.x,event.y)# as coordenadas recebidas no widget canvas estao no coord "window", passando as p/ world
				self.m_oCurrConnector.UpdateTracking(t_Point)
				return False
		return False
	
	def canvas_root_event(self, widget, event=None):
		
		if event.type == gtk.gdk.KEY_PRESS:
			if event.keyval == gtk.keysyms.Delete:
				currentWidget = self.get_property('focused-item')
				
				t_bSearching = True
				for blockIdx in self.m_oBlocks:
					if self.m_oBlocks[blockIdx].wGroup == currentWidget:
						self.DeleteBlock(blockIdx)
						t_bSearching = False
						break
					
				if t_bSearching:
					for connIdx in reversed(range(len(self.m_oConnectors))):
						if self.m_oConnectors[connIdx].wGroup == currentWidget:
							connAtLimbo = self.m_oConnectors.pop(connIdx)
							connAtLimbo.wGroup.destroy()
							del connAtLimbo #this line won't do much.. but helps understanding..
							break
				self.UpdateFlows()
		
		#updating focus whenever button 1 is pressed
		if event.type == gtk.gdk.BUTTON_PRESS:#se temos um clique nao pego por ngm, abortar a conexao
			if event.button == 1:
				self.lastClickecPt = (event.x, event.y)
				for blockIdx in self.m_oBlocks:
					self.m_oBlocks[blockIdx].UpdateFocus()#tricky cos we have a dict not a list (iterating through keys not elements)
				for conn in self.m_oConnectors:
					conn.UpdateFocus()
			else: # event.button == 3:
				return False
				#print "right button nowhere"
				#self.RightClick(event)
		
		
		if event.type == gtk.gdk.BUTTON_PRESS:#se temos um clique nao pego por ngm, abortar a conexao
			if event.button == 1:
				self.grab_focus()
				#print "aborting conn on root"
				self.AbortConnection()
				self.UpdateFlows()
				return False
		elif event.type == gtk.gdk.MOTION_NOTIFY:
			if event.state & gtk.gdk.BUTTON1_MASK:
				for connector in self.m_oConnectors:
					connector.UpdateConnectors()
				#self.UpdateFlows()
				return False
		return False
		
	
	def WhiteBoard_event(self, widget, event=None):
		if event.type == gtk.gdk.BUTTON_PRESS:#se temos um clique nao pego por ngm, abortar a conexao
			if event.button == 1:
				self.wbWidget.grab_focus()
				#print "aborting conn on whiteBoard"
				self.AbortConnection()
				return False
		return False
	
	def GotoScrolling(self,x,y):
		t_oHa = self.get_hadjustment()
		t_oVa = self.get_vadjustment()
		t_oHa.set_value(x)
		t_oVa.set_value(y)
	
	def UpdateScrolling(self):
		#minX,minY = 0,0
		#maxX,maxY = 400,400 #self.minWidth,self.minHeight
		
		t_aSr = self.get_scroll_region()
		
		#print t_aSr[0],",",t_aSr[1],",",t_aSr[2],",",t_aSr[3]
		
		minX = t_aSr[0]
		minY = t_aSr[1]
		
		maxX = t_aSr[0]+t_aSr[2]
		maxY = t_aSr[1]+t_aSr[3]
		
		
		for blockIdx in self.m_oBlocks:
			bpos = self.m_oBlocks[blockIdx].GetBlockPos()
			minX = min(minX,bpos[0])
			minY = min(minY,bpos[1])
		
			maxX = max(maxX,bpos[0]+self.m_oBlocks[blockIdx].width)
			maxY = max(maxY,bpos[1]+self.m_oBlocks[blockIdx].height)
		
		self.set_scroll_region(minX,minY,maxX-minX,maxY-minY)
		
		self.RedrawBlocks()
	
	
	def RedrawBlocks(self):
		for blockIdx in self.m_oBlocks:#self.m_oBlocks is a dict!
			self.m_oBlocks[blockIdx].Redraw()
	
	def InsertBlock(self, a_nBlockType,x=None,y=None): #, a_oDictBlock = {}):
		if x == None:
			x_off = (self.get_hadjustment()).get_value()
			y_off = (self.get_vadjustment()).get_value()
			if self.lastClickecPt <> (None, None):
				x, y = self.world_to_window(self.lastClickecPt[0],self.lastClickecPt[1])
				x -= x_off
				y -= y_off
			else:
				x, y = (100-x_off, 100-x_off)
		self.InsertBlockPosId(a_nBlockType,x,y,self.m_nBlockCountId)
		self.m_nBlockCountId += 1
		self.UpdateScrolling()
		return self.m_nBlockCountId - 1
		
	def InsertBlockPosId(self, a_nBlockType,x,y,a_sBlockCountId):
		if a_nBlockType == 02: #show block
			t_oNewBlock = GcdBlock_Show.GcdBlock_Show(self,a_nBlockType,a_sBlockCountId)
		else:
			t_oNewBlock = GcdBlock.GcdBlock(self,a_nBlockType,a_sBlockCountId)
		
		#print "orig",x,",",y #relative coords
		
		x_off = (self.get_hadjustment()).get_value()
		#print "vadj",x_off
		
		y_off = (self.get_vadjustment()).get_value()
		#print "hadj",y_off

		#cSr = self.get_scroll_region()
		#print cSr[0],",",cSr[1],",",cSr[2],",",cSr[3]
		
		cPt = self.window_to_world(x,y)
		#print "win2wor",cPt[0],",",cPt[1]

		#cWt = self.world_to_window(x,y)
		#print "wor2win",cWt[0],",",cWt[1]

		#cCd = self.w2c_d(x,y)
		#print "w2c_d",cCd[0],",",cCd[1]

		
		t_oNewBlock.Move(x_off+cPt[0]-20.0,y_off+cPt[1]-60.0) #cPt[0],cPt[1])
		self.m_oBlocks[a_sBlockCountId] = t_oNewBlock
	
	def RemoveBlock( self, a_iBlockId=0):
		#print "Block " + str(a_iBlockId) + " deleted"
		self.UpdateFlows()
		
	def InsertReadyConnector(self, a_nFromId, a_nFromIdOut, a_nToId, a_nToIdIn):
		#print a_nFromId,",",a_nFromIdOut,",",a_nToId,",",a_nToIdIn
		t_oNewConn = GcdConnector.GcdConnector(self,self.m_nConnectorCountId, a_nFromId,a_nFromIdOut)
		t_oNewConn.SetEnd(a_nToId, a_nToIdIn)
		if self.ValidConnector(t_oNewConn):
			if self.ConnectorTypesMatch(t_oNewConn):
				self.m_oConnectors.append(t_oNewConn)#TODO: checar se ja existe este conector
				self.m_nConnectorCountId +=1
				self.UpdateFlows()
			else:
				print "Output and Input types don't match"
		else:
			print "Invalid Connector, not adding"
		
	def ClickedInput(self, a_nBlockCountId, a_nInput):#TODO na real, pegar em tempo real aonde tah aquela porta!!
		#print "block" + str(a_nBlockCountId) + "_In" + str(a_nInput)
		if self.m_oCurrConnector <> None:
			self.m_oCurrConnector.SetEnd(a_nBlockCountId, a_nInput)
			if self.ValidConnector(self.m_oCurrConnector):
				if self.ConnectorTypesMatch(self.m_oCurrConnector):
					self.m_oConnectors.append(self.m_oCurrConnector)#TODO: checar se ja existe este conector
					self.m_nConnectorCountId +=1
					self.m_oCurrConnector = None
					self.UpdateFlows()
					
				else:
					print "Output and Input types don't match"
					self.AbortConnection()
			else:
				print "Invalid Connector"
				self.AbortConnection()
			#print self.m_oConnectors

	def ConnectorTypesMatch(self, a_oConnector):
		outType = self.m_oBlocks[a_oConnector.fromBlock].m_oDictBlock["OutTypes"][a_oConnector.fromBlockOut]
		inType = self.m_oBlocks[a_oConnector.toBlock].m_oDictBlock["InTypes"][a_oConnector.toBlockIn]
		if not outType == inType:
			print "Types mismatch"
		return outType == inType
			

	def ValidConnector(self, newCon):#checks whether the new Cn links to a already used input (in this case, also invalidating cloned connectors)
		for oldCon in self.m_oConnectors:
			if oldCon.toBlock == newCon.toBlock \
					and oldCon.toBlockIn == newCon.toBlockIn:
				print "Cloned Connector"
				return False
		if newCon.toBlock == newCon.fromBlock:
			print "Recursive \"from future\" connector"
			return False
		return True

	def ClickedOutput(self, a_nBlockCountId, a_nOutput):
		self.AbortConnection()#abort any possibly running connections
		#print "block" + str(a_nBlockCountId) + "_Out" + str(a_nOutput)
		self.m_oCurrConnector = GcdConnector.GcdConnector(self,self.m_nConnectorCountId, a_nBlockCountId,a_nOutput)
		self.UpdateFlows()

	def AbortConnection(self):
		if self.m_oCurrConnector <> None:
			self.m_oCurrConnector.wGroup.destroy()## BUG!
			del self.m_oCurrConnector
			self.m_oCurrConnector = None

	def DeleteBlock(self, blockCountId):
		
		#print "removing block ",blockCountId
		
		#removing related connectors
		for idx in reversed(range(len(self.m_oConnectors))):
			if self.m_oConnectors[idx].fromBlock == blockCountId or self.m_oConnectors[idx].toBlock == blockCountId:
				self.m_oConnectors[idx].wGroup.destroy()
				connAtLimbo = self.m_oConnectors.pop(idx)
				del connAtLimbo

		#removing the block itself
		blockAtLimbo = self.m_oBlocks.pop(blockCountId)
		blockAtLimbo.wGroup.destroy()
		del blockAtLimbo
		
		self.UpdateFlows()
	
	def UpdateWhiteBoard(self):
		if self.wbWidget == None:
			clr = ColorFromList([255,255,255,255])
			self.wbWidget = self.root().add(gnomecanvas.CanvasRect,x1=-10000,y1=-10000,x2=10000,y2=10000,fill_color_rgba=clr)
			#should we change this size dynamically?? or make it simply a HUGE whiteboard?
			self.wbWidget.set_flags(gtk.CAN_FOCUS)
			self.wbWidget.connect("event", self.WhiteBoard_event)
		#else:
		
	def UpdateFlows(self):
		for checkTimeShifter in [False, True]:
			prevCount = -1
			newCount = self.CountFlowingComponents()
			while prevCount <> newCount:
				#print "newCount:",newCount
				#print "prevCount:",prevCount
				for blockIdx in self.m_oBlocks:#self.m_oBlocks is a dict!
					self.m_oBlocks[blockIdx].UpdateFlow(checkTimeShifter)
				#print "--------"
				
				for conn in self.m_oConnectors:
					conn.UpdateFlow()
				#print "-----------------"
				prevCount = newCount
				newCount = self.CountFlowingComponents()
		self.UpdateFlowsDisplays()
		
	def UpdateFlowsDisplays(self):
		for blockIdx in self.m_oBlocks:#self.m_oBlocks is a dict!
			self.m_oBlocks[blockIdx].UpdateFlowDisplay()
		for conn in self.m_oConnectors:
			conn.UpdateFlowDisplay()
	
	def GetConnectorsTo(self, a_nBlockCountId):
		result = []
		for conn in self.m_oConnectors:
			if conn.toBlock == a_nBlockCountId:
				result.append(conn)
		return result
	
	def CountFlowingComponents(self):
		count = 0
		for blockIdx in self.m_oBlocks:
			if self.m_oBlocks[blockIdx].m_bHasFlow:
				count += 1
		for conn in self.m_oConnectors:
			if conn.m_bHasFlow:
				count += 1
		return count
	
	def __BlockXMLOut(self, t_oBlockIdx, Properties, Network, a_bKeepNonFlowing=False):
		if self.m_oBlocks[t_oBlockIdx].GetState() or a_bKeepNonFlowing:
				Properties += self.m_oBlocks[t_oBlockIdx].GetPropertiesXML().properties.block.xml() + "\n  "
				Network += '<block type="' + str(self.m_oBlocks[t_oBlockIdx].GetType()) + '" id="' + str(self.m_oBlocks[t_oBlockIdx].GetId()) + '">\n'
				Network += "<inputs>\n"
				for t_nInputIdx in range(self.m_oBlocks[t_oBlockIdx].m_oDictBlock["Inputs"]):
					Network += '<input id="' + str(t_nInputIdx+1) + '"/>\n' #+1 pois o range eh de 0..x (precisamos do id 1...x+1)
				Network += "</inputs>\n"
	
				Network += "<outputs>\n"
				t_dConnectedOuts = {}
				for t_oConnector in self.m_oConnectors:
					if t_oConnector.fromBlock == self.m_oBlocks[t_oBlockIdx].GetId() and (self.m_oBlocks[t_oConnector.toBlock].GetState() or a_bKeepNonFlowing):
						Network += '<output id="' + str(t_oConnector.fromBlockOut+1) + '" inBlock="' + str(t_oConnector.toBlock) + '" input="' + str(t_oConnector.toBlockIn+1) + '"/>\n' #+1 pois o range eh de 0..x (precisamos do id 1...x+1)
						t_dConnectedOuts[t_oConnector.fromBlockOut] = 1
				for Output in range(self.m_oBlocks[t_oBlockIdx].m_oDictBlock["Outputs"]):
					if not t_dConnectedOuts.has_key(Output):
						Network += '<output id="' + str(Output+1) + '" inBlock="--" input="--"/>\n'
				Network += "</outputs>\n"
				Network += "</block>\n"
		return (Properties, Network)
	
	def GetProcessChain( self,a_bKeepNonFlowing=False ): #frontend will get only the valid chain although saving will include the invalid ones
		Properties = "<properties>\n  "
		Network = "<network>\n"

		##REAL TRICKY BUG solution here, source blocks must be processed in an earlier phase so assumptions as "live" or not will be valid 
		##throughout the whole code generation 
		
		for t_oBlockIdx in self.m_oBlocks:
			if self.m_oBlocks[t_oBlockIdx].m_bIsSource:
				(Properties, Network) = self.__BlockXMLOut(t_oBlockIdx,Properties, Network,a_bKeepNonFlowing)

		for t_oBlockIdx in self.m_oBlocks:
			if not self.m_oBlocks[t_oBlockIdx].m_bIsSource:
				(Properties, Network) = self.__BlockXMLOut(t_oBlockIdx,Properties, Network,a_bKeepNonFlowing)
		
		Properties += "</properties>\n"
		Network += "</network>\n"
		
		return Properties + Network

	def SetFilename( self, a_sFilename ):
		self.m_sFilename = a_sFilename

	def GetFilename( self ):
		return self.m_sFilename
	
	def LoadFromPopup(self, *args):
		filename = str(raw_input("Xunxo; Enter Filename:"))
		self.Load(filename)
	
	def Load( self, a_sFilename=None ):
		if a_sFilename <> None:
			self.SetFilename(a_sFilename)
		else:
			if self.m_sFilename == None:
				self.m_sFilename = "Cannot Load without filename"
				return False
		
		#reseting present diagram.. 
		self.m_oBlocks,self.m_oConnectors,self.m_oCurrConnector,self.m_nSessionId = {},[],None,0
		
		#this two must be updated at each block/conn insertion
		self.m_nBlockCountId = 1 #since block counts are kept, render this from the saved file
		self.m_nConnectorCountId = 1 #since connector Ids are generated from scratch, just reset it
		
		t_oLoad = bt.bind_file(self.m_sFilename) #binding saved project
		
		#loading blocks on canvas
		for block in t_oLoad.harpia.GcState.block:
			self.InsertBlockPosId(int(block.type),float(block.position.x),float(block.position.y),int(block.id))
			self.m_nBlockCountId = max(self.m_nBlockCountId,int(block.id))
		self.m_nBlockCountId += 1
			
		#loading connectors on canvas
		try:
			for block in t_oLoad.harpia.network.block:
				for connector in block.outputs.output:
					if connector.inBlock <> "--" and connector.input <> "--":
						self.InsertReadyConnector(int(block.id), (int(connector.id)-1), int(connector.inBlock), (int(connector.input)-1)) 
						#this "-1" are "paired" with those "+1" at line 286 (GetProcessChain:offset=14)
		except AttributeError:
			pass
		
		#loading properties
		for block in t_oLoad.harpia.properties.block:
			t_sBlockProperties = '<?xml version="1.0" encoding="UTF-8"?>\n<properties>\n' + block.xml() + '\n</properties>\n'
			self.m_oBlocks[int(block.id)].SetPropertiesXML(bt.bind_string(t_sBlockProperties))
		
		self.UpdateScrolling()
		self.GotoScrolling(0,0);
		return True

	def SaveFromPopup( self, *args):
		self.Save()
		
	def Save(self, a_sFilename=None): #saving project
		if a_sFilename <> None:
			self.SetFilename(a_sFilename)
		if self.m_sFilename == None:
			self.m_sFilename = "Cadeia_" + str(time.time()) + ".hrp"
			
		#saving blocks current state 
		t_sGcState = "<GcState>\n"
		for blockIdx in self.m_oBlocks:
			t_sGcState += '\t<block type="' + str(self.m_oBlocks[blockIdx].GetType()) + '" id="' + str(self.m_oBlocks[blockIdx].GetId()) + '">\n'
			t_tPos = self.m_oBlocks[blockIdx].GetPos()
			t_sGcState += '\t\t<position x="' + str(t_tPos[0]) + '" y="' + str(t_tPos[1]) + '"/>\n'
			t_sGcState += '\t</block>\n'
		t_sGcState += "</GcState>\n"
		
		#saving processing chain (which includes blocks properties and conectors)
		t_sProcessingChain = self.GetProcessChain(True)
		
		t_sOutFile = "<harpia>\n" + t_sGcState + t_sProcessingChain + "</harpia>\n"
		
		if self.m_sFilename.find(".hrp") == -1:
			self.m_sFilename += ".hrp"
		
		t_oSaveFile = open( str(self.m_sFilename) , "w" )
		t_oSaveFile.write(t_sOutFile)
		t_oSaveFile.close()
		
	def GetBlockOnFocus(self):
		for blockIdx in self.m_oBlocks:
			if self.m_oBlocks[blockIdx].m_bFocus:
				return blockIdx
		
	def SetIDBackendSession(self, a_nSessionId):
		self.m_nSessionId = a_nSessionId

	def GetIDBackendSession(self):
		return self.m_nSessionId
	
	def Export2Png(self, filepath="diagrama.png"):
		(x,y,t_nWidth,t_nHeight,t_nDepth) = self.window.get_geometry()
		
		t_oPixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,t_nWidth,t_nHeight)
		t_oBuffer = t_oPixbuf.get_from_drawable(self.window, self.get_colormap(),0, 0, 0, 0, t_nWidth, t_nHeight)
		# get_from_drawable(GdkWindow src, GdkColormap cmap, int src_x, int src_y, int dest_x, int dest_y, int width, int height);
		t_oBuffer.save(filepath, "png")
		#bugs:
		# *nao considera o que estiver fora do scroll region
		# *da um printScreen somente então pega qlqr outra coisa q estiver no caminho (incluindo o proprio menu ali do FILE)
		# *aparentemente é a maneira errada.

	def SetErrorLog(self, a_sErrorLog):
		self.m_sErrorLog = a_sErrorLog
	
	def Append2ErrorLog(self, a_sErrorLog):
		self.m_sErrorLog += a_sErrorLog
	
	def GetErrorLog(self):
		return self.m_sErrorLog
		
	def ZoomIn(self):
		self.m_fPixels_per_unit *= 1.1
		self.set_pixels_per_unit(self.m_fPixels_per_unit)
	
	def ZoomOut(self):
		self.m_fPixels_per_unit *= 0.9
		self.set_pixels_per_unit(self.m_fPixels_per_unit)
	
	def ZoomOrig(self):
		self.m_fPixels_per_unit = 1.0
		self.set_pixels_per_unit(self.m_fPixels_per_unit)

	#def RightClick(self, a_oEvent):
		#pass
		#t_oMenu = gtk.Menu()
	
		#t_oMenuItem = gtk.MenuItem("Save Diagram")
		#t_oMenuItem.connect("activate", self.SaveFromPopup)
		#t_oMenu.append(t_oMenuItem)

		#t_oMenuItem = gtk.MenuItem("Load Diagram")
		#t_oMenuItem.connect("activate", self.LoadFromPopup)
		#t_oMenu.append(t_oMenuItem)
		
		#t_oMenuItem = gtk.SeparatorMenuItem()
		#t_oMenu.append(t_oMenuItem)
		
		#t_oMenuItem = gtk.MenuItem("Delete Diagram")
		#t_oMenuItem.connect("activate", self.SaveFromPopup)
		#t_oMenu.append(t_oMenuItem)

		#t_oMenuItem = gtk.SeparatorMenuItem()
		#t_oMenu.append(t_oMenuItem)
		
		## Shows the menu
		#t_oMenu.show_all()
		#t_oMenu.popup(None, None, None, a_oEvent.button, a_oEvent.time)

def ColorFromList(rgba):
	color = int(rgba[0])*0x1000000+int(rgba[1])*0x10000+int(rgba[2])*0x100+(int(rgba[3])*0x01)
	return color