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
# ----------------------------------------------------------------------

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GooCanvas


from block import Block
from connector import Connector
import harpia.s2idirectory
from harpia.constants import *

#import time

from harpia.utils.graphicfunctions import *


class Diagram(GooCanvas.Canvas):

    #----------------------------------------------------------------------
    def __init__(self, main_window):
        GooCanvas.Canvas.__init__(self)

        self.last_clicked_point = (None, None)
        self.main_window = main_window

        self.zoom = 1.0 # pixels per unit
        self.show()
        self.blocks = {} # GUI blocks
        self.connectors = []
        self.curr_connector = None
        self.current_widget = None

        self.block_id = 1  # o primeiro bloco eh o n1 (incrementa a cada novo bloco
        self.connector_id = 1  # o primeiro conector eh o n1 (incrementa a cada novo conector

        Gtk.Widget.grab_focus(self)
        self.connect("motion-notify-event", self.__on_motion_notify)
        # Must be after block button press to allow connection
        self.connect_after("button_press_event", self.__on_button_press)
        self.connect("key-press-event", self.__on_key_press)

        self.connect("drag_data_received", self.drag_data_received)
        self.drag_dest_set(
            Gtk.DestDefaults.MOTION | Gtk.DestDefaults.HIGHLIGHT | Gtk.DestDefaults.DROP,
            [Gtk.TargetEntry.new('text/plain', Gtk.TargetFlags.SAME_APP, 1)],
            Gdk.DragAction.DEFAULT | Gdk.DragAction.COPY)

        self.file_name = None

        self.white_board = None
#        self.set_property("x2", self.main_window.get_size()[0])
        self.set_property("expand", True)
        self.__update_white_board()

    #----------------------------------------------------------------------
    def __del__(self):
        pass

    #----------------------------------------------------------------------
    def __on_motion_notify(self, canvas_item, event=None):
        if event.state & Gdk.ModifierType.BUTTON1_MASK:
            for connector in self.connectors:
                connector.update_flow()

        if self.curr_connector == None:
            return False
        point = (event.x,event.y)
        self.curr_connector.update_tracking(point)
        return False

    # ---------------------------------------------------------------------
    def delete(self):
        if self.current_widget != None:
            self.current_widget.delete()
            self.current_widget = None
            self.update_flows()

    #----------------------------------------------------------------------
    def __on_key_press(self, widget, event=None):
        if event.keyval == Gdk.KEY_Delete:
            self.delete()

    #----------------------------------------------------------------------
    def __on_button_press(self, widget, event=None):
        Gtk.Widget.grab_focus(self)
        if event.button == 1:
            self.last_clicked_point = (event.x, event.y)
            for blockIdx in self.blocks:
                # tricky cos we have a dict not a list (iterating through keys not elements)
                self.blocks[blockIdx].update_flow()
            for conn in self.connectors:
                conn.update_flow()
            self.current_widget = None
            self.__abort_connection()
            self.update_flows()
            return False
        return False


    # ----------------------------------------------------------------------
    def drag_data_received(self, widget, context, x, y, selection, targetType, time):
        block = self.main_window.main_control.get_selected_block()
        if block != None:
            self.insert_block(block, x, y)
        return

    #----------------------------------------------------------------------
    def update_scrolling(self):
        min_x = 0
        min_y = 0

        limit_x = self.white_board.get_property("width")
        limit_y = self.white_board.get_property("height")

        for blockIdx in self.blocks:
            bpos = self.blocks[blockIdx].get_position()
            if bpos[0] < min_x:
                min_x = bpos[0]
            if bpos[1] < min_y:
                min_y = bpos[1]

        if min_x < 0:
            for blockIdx in self.blocks:
                bpos = self.blocks[blockIdx].move(abs(min_x),0)

        if min_y < 0:
            for blockIdx in self.blocks:
                bpos = self.blocks[blockIdx].move(0, abs(min_y))

        for blockIdx in self.blocks:
            bpos = self.blocks[blockIdx].get_position()
            if bpos[0] > limit_x - self.blocks[blockIdx].width:
                self.blocks[blockIdx].move(limit_x - bpos[0] - self.blocks[blockIdx].width,0)
            if bpos[1] > limit_y - self.blocks[blockIdx].height:
                self.blocks[blockIdx].move(0, limit_y - bpos[1] - self.blocks[blockIdx].height)

        self.update_flows()

    #----------------------------------------------------------------------
    def insert_block(self, block, x=None, y=None):
        if x == None:
            x_off = (self.get_hadjustment()).get_value()
            y_off = (self.get_vadjustment()).get_value()
            if self.last_clicked_point != (None, None):
                x, y = (self.last_clicked_point[0], self.last_clicked_point[1])
                x -= x_off
                y -= y_off
            else:
                x, y = (100 - x_off, 100 - x_off)
        self.insert_blockPosId(block, x, y, self.block_id)
        self.block_id += 1
        self.update_scrolling()
        return self.block_id - 1

    #----------------------------------------------------------------------
    def insert_blockPosId(self, block, x, y, block_id):
        new_block = Block(self, block, block_id)
        new_block.translate(x - 20.0, y - 60.0)
        self.blocks[block_id] = new_block
        self.get_root_item().add_child(new_block, -1)

    #----------------------------------------------------------------------
    def insert_ready_connector(self, a_nFromId, a_nFromIdOut, a_nToId, a_nToIdIn):
        new_connection = Connector(self, a_nFromId, a_nFromIdOut)
        new_connection.set_end(a_nToId, a_nToIdIn)
        if self.__valid_connector(new_connection):
            if self.__connector_types_match(new_connection):
                self.connectors.append(new_connection)  # TODO: checar se ja existe este conector
                self.connector_id += 1
                self.update_flows()
                self.get_root_item().add_child(new_connection, -1)
            else:
                pass
        else:
            pass

    #----------------------------------------------------------------------
    def clicked_input(self, block_id, a_nInput):
        if self.curr_connector == None:
            return
        self.curr_connector.set_end(block_id, a_nInput)
        if not self.__valid_connector(self.curr_connector):
            self.__abort_connection()
            return
        if not self.__connector_types_match(self.curr_connector):
            self.__abort_connection()
            return
        self.connectors.append(self.curr_connector)

        self.connector_id += 1
        self.curr_connector = None
        self.update_flows()

    #----------------------------------------------------------------------
    def __connector_types_match(self, a_oConnector):
        outType = self.blocks[a_oConnector.from_block].block_description["OutTypes"][a_oConnector.from_block_out]
        inType = self.blocks[a_oConnector.to_block].block_description["InTypes"][a_oConnector.to_block_in]
        if not outType == inType:
            s2idirectory.Log.log("Connection Types mismatch")
        return outType == inType

    #----------------------------------------------------------------------
    def __valid_connector(self, newCon):
        for oldCon in self.connectors:
            if oldCon.to_block == newCon.to_block \
                    and oldCon.to_block_in == newCon.to_block_in:
                print "Cloned Connector"
                return False
        if newCon.to_block == newCon.from_block:
            print "Recursive \"from future\" connector"
            return False
        return True

    #----------------------------------------------------------------------
    def clicked_output(self, block_id, output):
        self.__abort_connection()  # abort any possibly running connections
        self.curr_connector = Connector(self, block_id, output)
        self.get_root_item().add_child(self.curr_connector, -1)
        self.update_flows()

    #----------------------------------------------------------------------
    def __abort_connection(self):
        if self.curr_connector == None:
            return
        self.get_root_item().remove_child(self.get_root_item().get_n_children() - 1)
        del self.curr_connector
        self.curr_connector = None

    #----------------------------------------------------------------------
    def delete_connection(self, connection):
        connection.remove()
        self.connectors.remove(connection)

    #----------------------------------------------------------------------
    def delete_block(self, block_id):
        # removing related connectors
        for idx in reversed(range(len(self.connectors))):
            if self.connectors[idx].from_block == block_id or self.connectors[idx].to_block == block_id:
                self.delete_connection(self.connectors[idx])

        # removing the block itself
        self.blocks[block_id].remove()
        del self.blocks[block_id]
        self.update_flows()

    #----------------------------------------------------------------------
    def __white_board_event(self, widget, event=None):
        if event.type == Gdk.EventType.BUTTON_PRESS:  # se temos um clique nao pego por ngm, abortar a conexao
            if event.button == 1:
                self.white_board.grab_focus()
                self.__abort_connection()
                return False
        return False

    #----------------------------------------------------------------------
    def __update_white_board(self):
        if self.white_board == None:
            self.white_board = GooCanvas.CanvasRect(
                            parent=self.get_root_item(),
                            x=0,
                            y=0,
                            width=self.main_window.get_size()[0],
                            height=1000,
                            stroke_color="white",
                            fill_color="white")
            self.white_board.connect("focus-in-event", self.__white_board_event)
        pass

    #----------------------------------------------------------------------
    def update_flows(self):
        for blockIdx in self.blocks:  # self.blocks is a dict!
            self.blocks[blockIdx].update_flow()
        for conn in self.connectors:
            conn.update_flow()

    #----------------------------------------------------------------------
    def get_connectors_to(self, block_id):
        result = []
        for conn in self.connectors:
            if conn.to_block == block_id:
                result.append(conn)
        return result

    #----------------------------------------------------------------------
    def set_file_name(self, file_name):
        self.file_name = file_name

    #----------------------------------------------------------------------
    def get_file_name(self):
        return self.file_name

    #----------------------------------------------------------------------
    def get_block_on_focus(self):
        for blockIdx in self.blocks:
            if self.blocks[blockIdx].focus:
                return blockIdx

    #----------------------------------------------------------------------
    def set_zoom(self, value):
        if value == ZOOM_ORIGINAL:
            self.zoom = ZOOM_ORIGINAL
        else:
            self.zoom *= value
        self.set_scale(self.zoom)
        self.update_scrolling()

    #----------------------------------------------------------------------
    def set_selected_block(self, block):
        self.main_window.main_control.set_selected_block(block)

    # ----------------------------------------------------------------------
    def resize(self, data):
        print "RESIZE DO CANVAS"
        self.set_property("x2", self.main_window.get_size()[0])
        self.white_board.set_property("width", self.main_window.get_size()[0])

#----------------------------------------------------------------------

    
