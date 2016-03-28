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
      menu = gtk.Menu()

      # Excluir (delete) item
      menu_item = gtk.MenuItem("Delete")
      menu_item.connect("activate", self.__delete_clicked )
      menu.append(menu_item)

      # Shows the menu
      menu.show_all()
      menu.popup(None, None, None, event.button, event.time)

   def __delete_clicked(self, *args ): #this strongly depends on the garbage collector
      for connIdx in range(len(self.connector.diagram.connectors)):
         if self.connector.diagram.connectors[connIdx] == self.connector:
            self.connector.diagram.connectors.pop(connIdx)
            self.connector.group.destroy()
            break #faster, necessary (not iteraring on reverse!)

