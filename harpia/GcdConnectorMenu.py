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

import s2iblockpropertiesgui
from harpia import showimage

class GcdConnectorMenu:
   def __init__(self, connector, event):
      self.connector = connector
      t_oMenu = gtk.Menu()

#      t_oMenuItem = gtk.MenuItem("Properties")
#      t_oMenuItem.connect("activate", self.ShowPropertiesGUI )
#      t_oMenu.append(t_oMenuItem)

      # Menu separator
#      t_oMenuItem = gtk.SeparatorMenuItem()
#      t_oMenu.append(t_oMenuItem)
      
      # Excluir (delete) item
      t_oMenuItem = gtk.MenuItem("Delete")
      t_oMenuItem.connect("activate", self.DeleteClicked )
      t_oMenu.append(t_oMenuItem)

      # Shows the menu
      t_oMenu.show_all()
      t_oMenu.popup(None, None, None, event.button, event.time)

   def DeleteClicked(self, *args ): #this strongly depends on the garbage collector
      for connIdx in range(len(self.connector.ParentDiagram.m_oConnectors)):
         if self.connector.ParentDiagram.m_oConnectors[connIdx] == self.connector:
            self.connector.ParentDiagram.m_oConnectors.pop(connIdx)
            self.connector.wGroup.destroy()
            break #faster, necessary (not iteraring on reverse!)

