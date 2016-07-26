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
from gi.repository import Gtk
from gi.repository import Gdk

#from harpia.s2iblockpropertiesgui import *
#from harpia import showimage

class BlockMenu:

    def __init__(self, block, event):
        self.block = block

        # Double click
        if event.type == Gdk.EventType._2BUTTON_PRESS and self.block.get_type() == 2:
             self.__show_image_GUI()
             return
        # Double click
        if event.type == Gdk.EventType._2BUTTON_PRESS and self.block.get_type() != 2:
             self.__show_block_properties()
             return

        menu = Gtk.Menu()

        menu_item = Gtk.MenuItem("Properties")
        menu_item.connect("activate", self.__show_block_properties)
        menu.append(menu_item)

        if self.block.get_type() == 2:
            menu_item = gtk.MenuItem("Show Image")
            menu_item.connect("activate", self.__show_image_GUI)
            menu.append(menu_item)

#        menu_item = gtk.MenuItem("PrintXML")
#        menu_item.connect("activate", self.__print_XML)
#        menu.append(menu_item)

#        menu_item = gtk.MenuItem("PrintPOS")
#        menu_item.connect("activate", self.__print_position)
#        menu.append(menu_item)

        menu_item = Gtk.SeparatorMenuItem()
        menu.append(menu_item)

        menu_item = Gtk.MenuItem("Delete")
        menu_item.connect("activate", self.__delete_clicked)
        menu.append(menu_item)

        # Shows the menu
        menu.show_all()
        menu.popup(None, None, None, None, event.button, event.time)

    def __show_block_properties(self, *args):
#        PropertiesGUI = s2iblockpropertiesgui.S2iBlockPropertiesGUI(self.block)
#        PropertiesGUI.EditProperties(self.block.m_oPropertiesXML)
        pass

    def __delete_clicked(self, *args ): #this strongly depends on the garbage collector
        self.block.diagram.delete_block(self.block.block_id)

    def __print_position(self, *args):
        print "(",self.block.wGroup.get_property('x'),",",self.block.group.get_property('y'),")"

    def __print_XML(self, *args):
        print self.block.m_oPropertiesXML.getXML()

    def __show_image_GUI(self, *args):
#        path = "/tmp/harpiaBETMP0" + str(self.block.diagram.get_session_id()) + "/block" + str(self.block.get_id()) + "_OUT.png"
#        ShowGUI = showimage.ShowImage(path, self.block.diagram.get_error_log())
#        ShowGUI.show()
        pass


