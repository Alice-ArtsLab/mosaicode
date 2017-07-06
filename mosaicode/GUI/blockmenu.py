# -*- coding: utf-8 -*-
# [MOSAICODE PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org),
# S2i (www.s2i.das.ufsc.br)
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
#    For further information, check the COPYING file distributed with
#    this software.
#
# ----------------------------------------------------------------------
"""
This module contains the BlockMenu class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.GUI.blockeditor import BlockEditor

class BlockMenu(Gtk.Menu):
    """
    This class contains methods related the BlockMenu class
    """

    # ----------------------------------------------------------------------
    def __init__(self, block, event):
        """
        This method show the block menu.

            Parameters:
                * **block**
                * **event**
        """
        Gtk.Notebook.__init__(self)
        self.block = block

        menu_item = Gtk.MenuItem("Delete")
        menu_item.connect("activate", self.__delete_clicked)
        self.append(menu_item)

        menu_item = Gtk.MenuItem("Edit Block")
        menu_item.connect("activate", self.__edit_clicked)
        self.append(menu_item)

        # Shows the menu
        self.show_all()
        self.popup(None, None, None, None, event.button.button, event.time)

    # ----------------------------------------------------------------------
    def __delete_clicked(self, *args):
        """
        This method monitors if the button delete was clicked.

            Parameters:
            * **args**

        """
        self.block.delete()
        
    # ----------------------------------------------------------------------
    def __edit_clicked(self, *args):
        """
        This method monitors if the button delete was clicked.

            Parameters:
            * **args**

        """
        from mosaicode.system import System as System
        BlockEditor(self.block.diagram.main_window,
                System.blocks[self.block.type])
