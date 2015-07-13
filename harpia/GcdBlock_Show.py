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


import GcdBlock
import gobject
import gtk
from harpia import showimage

class GcdBlock_Show( GcdBlock.GcdBlock):
	
	def ShowBlockGUI(self, *args):
		t_sPath = "/tmp/harpiaBETMP0" + str(self.ParentDiagram.GetIDBackendSession()) + "/block" + str(self.GetId()) + "_OUT.png"
		
		ShowGUI = showimage.ShowImage(t_sPath, self.ParentDiagram.m_sErrorLog )
		ShowGUI.show()
		
		#execfile("showimage.py", {"ImagePath":t_sPath,"ErrorLog":self.ParentDiagram.m_sErrorLog })
	
	def RightClick(self, a_oEvent):
		t_oMenu = gtk.Menu()
	
		t_oMenuItem = gtk.MenuItem("Show Image")
		t_oMenuItem.connect("activate", self.ShowBlockGUI)
		t_oMenu.append(t_oMenuItem)
		
		t_oMenuItem = gtk.MenuItem("PrintXML")
		t_oMenuItem.connect("activate", self.PrintXML )
		t_oMenu.append(t_oMenuItem)
		
		t_oMenuItem = gtk.SeparatorMenuItem()
		t_oMenu.append(t_oMenuItem)
		
		t_oMenuItem = gtk.MenuItem("Delete")
		t_oMenuItem.connect("activate", self.DeleteClicked )
		t_oMenu.append(t_oMenuItem)

		t_oMenuItem = gtk.SeparatorMenuItem()
		t_oMenu.append(t_oMenuItem)
		
		# Shows the menu
		t_oMenu.show_all()
		t_oMenu.popup(None, None, None, a_oEvent.button, a_oEvent.time)