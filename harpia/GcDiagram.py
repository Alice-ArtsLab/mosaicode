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

import gnomecanvas
import GcdBlock
import GcdConnector
import gtk
import time

from exceptions import AttributeError

from utils.graphicfunctions import *

ZOOM_IN = 1.1
ZOOM_OUT = 0.9
ZOOM_ORIGINAL = 1.0

class GcDiagram(gnomecanvas.Canvas):
    def __init__(self):
        self.__gobject_init__()
        gnomecanvas.Canvas.__init__(self, aa=True)

        self.last_clicked_point = (None, None)

        # must be called everytime a block is moved or inserted with the new scroll region
        self.set_scroll_region(0, 0, 800, 600)

        self.zoom = 1.0 # pixels per unit
        self.show()
        self.blocks = {}
        self.connectors = []
        self.curr_connector = None
        self.session_id = 0

        self.block_id = 1  # o primeiro bloco eh o n1 (incrementa a cada novo bloco
        self.connector_id = 1  # o primeiro conector eh o n1 (incrementa a cada novo conector

        self.set_flags(gtk.CAN_FOCUS)
        self.grab_focus()
        self.root().connect("event", self.__canvas_root_event)
        self.connect("event",self.__canvas_event)  

        self.file_name = None
        self.error_log = ""

        self.white_board = None
        self.__update_white_board()

    def __del__(self):
        pass

    def __canvas_event(self, widget, event=None):  # nao serve pq QUALQUER EVENTO do canvas passa por aqui
        if self.curr_connector != None:
            if event.type == gtk.gdk.MOTION_NOTIFY:  # se temos um conector aberto, atualizar sua posicao
                # as coordenadas recebidas no widget canvas estao no coord "window", passando as p/ world
                point = self.window_to_world(event.x,event.y)
                self.curr_connector.update_tracking(point)
                return False
        return False

    def __canvas_root_event(self, widget, event=None):
        if event.type == gtk.gdk.KEY_PRESS:
            if event.keyval == gtk.keysyms.Delete:
                current_widget = self.get_property('focused-item')

                searching = True
                for blockIdx in self.blocks:
                    if self.blocks[blockIdx].group == current_widget:
                        self.delete_block(blockIdx)
                        searching = False
                        break

                if searching:
                    for connIdx in reversed(range(len(self.connectors))):
                        if self.connectors[connIdx].group == current_widget:
                            connAtLimbo = self.connectors.pop(connIdx)
                            connAtLimbo.group.destroy()
                            del connAtLimbo  # this line won't do much.. but helps understanding..
                            break
                self.__update_flows()

        # updating focus whenever button 1 is pressed
        if event.type == gtk.gdk.BUTTON_PRESS:  # se temos um clique nao pego por ngm, abortar a conexao
            if event.button == 1:
                self.last_clicked_point = (event.x, event.y)
                for blockIdx in self.blocks:
                    # tricky cos we have a dict not a list (iterating through keys not elements)
                    self.blocks[blockIdx].update_focus()
                for conn in self.connectors:
                    conn.update_focus()
            else:  # event.button == 3:
                return False
                # print "right button nowhere"
                # self.RightClick(event)

        if event.type == gtk.gdk.BUTTON_PRESS:  # se temos um clique nao pego por ngm, abortar a conexao
            if event.button == 1:
                self.grab_focus()
                # print "aborting conn on root"
                self.__abort_connection()
                self.__update_flows()
                return False
        elif event.type == gtk.gdk.MOTION_NOTIFY:
            if event.state & gtk.gdk.BUTTON1_MASK:
                for connector in self.connectors:
                    connector.update_connectors()
                return False
        return False

    def __white_board_event(self, widget, event=None):
        if event.type == gtk.gdk.BUTTON_PRESS:  # se temos um clique nao pego por ngm, abortar a conexao
            if event.button == 1:
                self.white_board.grab_focus()
                self.__abort_connection()
                return False
        return False

    def goto_scrolling(self, x, y):
        t_oHa = self.get_hadjustment()
        t_oVa = self.get_vadjustment()
        t_oHa.set_value(x)
        t_oVa.set_value(y)

    def update_scrolling(self):
        t_aSr = self.get_scroll_region()

        minX = t_aSr[0]
        minY = t_aSr[1]

        maxX = t_aSr[0] + t_aSr[2]
        maxY = t_aSr[1] + t_aSr[3]

        for blockIdx in self.blocks:
            bpos = self.blocks[blockIdx].get_block_pos()
            minX = min(minX, bpos[0])
            minY = min(minY, bpos[1])

            maxX = max(maxX, bpos[0] + self.blocks[blockIdx].width)
            maxY = max(maxY, bpos[1] + self.blocks[blockIdx].height)

        self.set_scroll_region(minX, minY, maxX - minX, maxY - minY)

        for blockIdx in self.blocks:  # self.blocks is a dict!
            self.blocks[blockIdx].redraw()

    def insert_block(self, block_type, x=None, y=None):
        if x == None:
            x_off = (self.get_hadjustment()).get_value()
            y_off = (self.get_vadjustment()).get_value()
            if self.last_clicked_point != (None, None):
                x, y = self.world_to_window(self.last_clicked_point[0], self.last_clicked_point[1])
                x -= x_off
                y -= y_off
            else:
                x, y = (100 - x_off, 100 - x_off)
        self.insert_blockPosId(block_type, x, y, self.block_id)
        self.block_id += 1
        self.update_scrolling()
        return self.block_id - 1

    def insert_blockPosId(self, block_type, x, y, block_id):
        new_block = GcdBlock.GcdBlock(self, block_type, block_id)

        x_off = (self.get_hadjustment()).get_value()
        y_off = (self.get_vadjustment()).get_value()
        cPt = self.window_to_world(x, y)

        new_block.move(x_off + cPt[0] - 20.0, y_off + cPt[1] - 60.0)  # cPt[0],cPt[1])
        self.blocks[block_id] = new_block

    def insert_ready_connector(self, a_nFromId, a_nFromIdOut, a_nToId, a_nToIdIn):
        t_oNewConn = GcdConnector.GcdConnector(self, a_nFromId, a_nFromIdOut)
        t_oNewConn.set_end(a_nToId, a_nToIdIn)
        if self.__valid_connector(t_oNewConn):
            if self.__connector_types_match(t_oNewConn):
                self.connectors.append(t_oNewConn)  # TODO: checar se ja existe este conector
                self.connector_id += 1
                self.__update_flows()
            else:
                pass
        else:
            pass

    def clicked_input(self, block_id, a_nInput):  # TODO na real, pegar em tempo real aonde tah aquela porta!!
        if self.curr_connector != None:
            self.curr_connector.set_end(block_id, a_nInput)
            if self.__valid_connector(self.curr_connector):
                if self.__connector_types_match(self.curr_connector):
                    self.connectors.append(self.curr_connector)  # TODO: checar se ja existe este conector
                    self.connector_id += 1
                    self.curr_connector = None
                    self.__update_flows()

                else:
                    self.__abort_connection()
            else:
                self.__abort_connection()
                # print self.connectors

    def __connector_types_match(self, a_oConnector):
        outType = self.blocks[a_oConnector.from_block].block_description["OutTypes"][a_oConnector.from_block_out]
        inType = self.blocks[a_oConnector.to_block].block_description["InTypes"][a_oConnector.to_block_in]
        if not outType == inType:
            print "Types mismatch"
        return outType == inType

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

    def clicked_output(self, block_id, a_nOutput):
        self.__abort_connection()  # abort any possibly running connections
        # print "block" + str(block_id) + "_Out" + str(a_nOutput)
        self.curr_connector = GcdConnector.GcdConnector(self, block_id, a_nOutput)
        self.__update_flows()

    def __abort_connection(self):
        if self.curr_connector != None:
            self.curr_connector.group.destroy()  ## BUG!
            del self.curr_connector
            self.curr_connector = None

    def delete_block(self, blockCountId):
        # removing related connectors
        for idx in reversed(range(len(self.connectors))):
            if self.connectors[idx].from_block == blockCountId or self.connectors[idx].to_block == blockCountId:
                self.connectors[idx].group.destroy()
                connAtLimbo = self.connectors.pop(idx)
                del connAtLimbo

        # removing the block itself
        blockAtLimbo = self.blocks.pop(blockCountId)
        blockAtLimbo.group.destroy()
        del blockAtLimbo

        self.__update_flows()

    def __update_white_board(self):
        if self.white_board == None:
            clr = ColorFromList([255, 255, 255, 255])
            self.white_board = self.root().add(gnomecanvas.CanvasRect, x1=-10000, y1=-10000, x2=10000, y2=10000,
                                            fill_color_rgba=clr)
            # should we change this size dynamically?? or make it simply a HUGE whiteboard?
            self.white_board.set_flags(gtk.CAN_FOCUS)
            self.white_board.connect("event", self.__white_board_event)

    # else:

    def __update_flows(self):
        for checkTimeShifter in [False, True]:
            prevCount = -1
            newCount = self.__count_flowing_components()
            while prevCount != newCount:
                # print "newCount:",newCount
                # print "prevCount:",prevCount
                for blockIdx in self.blocks:  # self.blocks is a dict!
                    self.blocks[blockIdx].update_flow(checkTimeShifter)
                for conn in self.connectors:
                    conn.update_flow()
                prevCount = newCount
                newCount = self.__count_flowing_components()

    def get_connectors_to(self, a_nBlockCountId):
        result = []
        for conn in self.connectors:
            if conn.to_block == a_nBlockCountId:
                result.append(conn)
        return result

    def __count_flowing_components(self):
        count = 0
        for blockIdx in self.blocks:
            if self.blocks[blockIdx].has_flow:
                count += 1
        for conn in self.connectors:
            if conn.has_flow:
                count += 1
        return count

    def set_file_name(self, file_name):
        self.file_name = file_name

    def get_file_name(self):
        return self.file_name

    def get_block_on_focus(self):
        for blockIdx in self.blocks:
            if self.blocks[blockIdx].focus:
                return blockIdx

    def set_session_id(self, session_id):
        self.session_id = session_id

    def get_session_id(self):
        return self.session_id

    def set_error_log(self, a_sErrorLog):
        self.error_log = a_sErrorLog

    def append_error_log(self, a_sErrorLog):
        self.error_log += a_sErrorLog

    def get_error_log(self):
        return self.error_log

    def set_zoom(self, value):
        if value == ZOOM_ORIGINAL:
            self.zoom = ZOOM_ORIGINAL
        else:
            self.zoom *= value
        self.set_pixels_per_unit(self.zoom)
        self.update_scrolling()
