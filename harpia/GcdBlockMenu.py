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

class GcdBlockMenu:

    def __init__(self, block, event):
        self.block = block
        t_oMenu = gtk.Menu()

        t_oMenuItem = gtk.MenuItem("Properties")
        t_oMenuItem.connect("activate", self.ShowBlockGUI )
        t_oMenu.append(t_oMenuItem)

#        t_oMenuItem = gtk.MenuItem("PrintXML")
#        t_oMenuItem.connect("activate", self.PrintXML )
#        t_oMenu.append(t_oMenuItem)

#        t_oMenuItem = gtk.MenuItem("PrintPOS")
#        t_oMenuItem.connect("activate", self.PrintPOS )
#        t_oMenu.append(t_oMenuItem)

        t_oMenuItem = gtk.SeparatorMenuItem()
        t_oMenu.append(t_oMenuItem)

        t_oMenuItem = gtk.MenuItem("Delete")
        t_oMenuItem.connect("activate", self.DeleteClicked )
        t_oMenu.append(t_oMenuItem)

        # Shows the menu
        t_oMenu.show_all()
        t_oMenu.popup(None, None, None, event.button, event.time)

    def ShowBlockGUI(self, *args):
        PropertiesGUI = s2iblockpropertiesgui.S2iBlockPropertiesGUI( self.block )
        PropertiesGUI.EditProperties( self.block.m_oPropertiesXML )

    def DeleteClicked(self, *args ): #this strongly depends on the garbage collector
        self.block.ParentDiagram.DeleteBlock(self.block.m_nBlockCountId)

    def PrintPOS(self, *args):
        print "(",self.block.wGroup.get_property('x'),",",self.block.wGroup.get_property('y'),")"

    def PrintXML(self, *args):
        print self.block.m_oPropertiesXML.getXML()

