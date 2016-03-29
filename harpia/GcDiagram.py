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

import gnomecanvas.Canvas
import harpia.GcdBlock
import harpia.GcdConnector
import gtk
import time

from exceptions import AttributeError

from utils.XMLUtils import XMLParser
from utils.graphicfunctions import *


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
        self.root().connect("event", self.canvas_root_event)
        self.connect("event",self.canvas_event)  

        self.file_name = None
        self.error_log = ""

        self.white_board = None
        self.UpdateWhiteBoard()

    def __del__(self):
        pass

    def canvas_event(self, widget, event=None):  # nao serve pq QUALQUER EVENTO do canvas passa por aqui
        if self.curr_connector != None:
            if event.type == gtk.gdk.MOTION_NOTIFY:  # se temos um conector aberto, atualizar sua posicao
                # as coordenadas recebidas no widget canvas estao no coord "window", passando as p/ world
                point = self.window_to_world(event.x,event.y)
                self.curr_connector.update_tracking(point)
                return False
        return False

    def canvas_root_event(self, widget, event=None):
        if event.type == gtk.gdk.KEY_PRESS:
            if event.keyval == gtk.keysyms.Delete:
                current_widget = self.get_property('focused-item')

                searching = True
                for blockIdx in self.blocks:
                    if self.blocks[blockIdx].group == current_widget:
                        self.DeleteBlock(blockIdx)
                        searching = False
                        break

                if searching:
                    for connIdx in reversed(range(len(self.connectors))):
                        if self.connectors[connIdx].group == current_widget:
                            connAtLimbo = self.connectors.pop(connIdx)
                            connAtLimbo.group.destroy()
                            del connAtLimbo  # this line won't do much.. but helps understanding..
                            break
                self.update_flows()

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
                self.AbortConnection()
                self.update_flows()
                return False
        elif event.type == gtk.gdk.MOTION_NOTIFY:
            if event.state & gtk.gdk.BUTTON1_MASK:
                for connector in self.connectors:
                    connector.update_connectors()
                    # self.update_flows()
                return False
        return False

    def __white_board_event(self, widget, event=None):
        if event.type == gtk.gdk.BUTTON_PRESS:  # se temos um clique nao pego por ngm, abortar a conexao
            if event.button == 1:
                self.white_board.grab_focus()
                self.AbortConnection()
                return False
        return False

    def GotoScrolling(self, x, y):
        t_oHa = self.get_hadjustment()
        t_oVa = self.get_vadjustment()
        t_oHa.set_value(x)
        t_oVa.set_value(y)

    def UpdateScrolling(self):
        t_aSr = self.get_scroll_region()

        # print t_aSr[0],",",t_aSr[1],",",t_aSr[2],",",t_aSr[3]

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

        self.redraw_blocks()

    def redraw_blocks(self):
        for blockIdx in self.blocks:  # self.blocks is a dict!
            self.blocks[blockIdx].redraw()

    def InsertBlock(self, block_type, x=None, y=None):  # , a_oDictBlock = {}):
        if x == None:
            x_off = (self.get_hadjustment()).get_value()
            y_off = (self.get_vadjustment()).get_value()
            if self.last_clicked_point != (None, None):
                x, y = self.world_to_window(self.last_clicked_point[0], self.last_clicked_point[1])
                x -= x_off
                y -= y_off
            else:
                x, y = (100 - x_off, 100 - x_off)
        self.__insert_blockPosId(block_type, x, y, self.block_id)
        self.block_id += 1
        self.UpdateScrolling()
        return self.block_id - 1

    def __insert_blockPosId(self, block_type, x, y, block_id):
        new_block = GcdBlock.GcdBlock(self, block_type, block_id)

        x_off = (self.get_hadjustment()).get_value()
        y_off = (self.get_vadjustment()).get_value()
        cPt = self.window_to_world(x, y)

        new_block.move(x_off + cPt[0] - 20.0, y_off + cPt[1] - 60.0)  # cPt[0],cPt[1])
        self.blocks[block_id] = new_block

    def InsertReadyConnector(self, a_nFromId, a_nFromIdOut, a_nToId, a_nToIdIn):
        t_oNewConn = GcdConnector.GcdConnector(self, a_nFromId, a_nFromIdOut)
        t_oNewConn.set_end(a_nToId, a_nToIdIn)
        if self.ValidConnector(t_oNewConn):
            if self.ConnectorTypesMatch(t_oNewConn):
                self.connectors.append(t_oNewConn)  # TODO: checar se ja existe este conector
                self.connector_id += 1
                self.update_flows()
            else:
                print "Output and Input types don't match"
        else:
            print "Invalid Connector, not adding"

    def ClickedInput(self, block_id, a_nInput):  # TODO na real, pegar em tempo real aonde tah aquela porta!!
        if self.curr_connector != None:
            self.curr_connector.set_end(block_id, a_nInput)
            if self.ValidConnector(self.curr_connector):
                if self.ConnectorTypesMatch(self.curr_connector):
                    self.connectors.append(self.curr_connector)  # TODO: checar se ja existe este conector
                    self.connector_id += 1
                    self.curr_connector = None
                    self.update_flows()

                else:
                    print "Output and Input types don't match"
                    self.AbortConnection()
            else:
                print "Invalid Connector"
                self.AbortConnection()
                # print self.connectors

    def ConnectorTypesMatch(self, a_oConnector):
        outType = self.blocks[a_oConnector.from_block].block_description["OutTypes"][a_oConnector.from_block_out]
        inType = self.blocks[a_oConnector.to_block].block_description["InTypes"][a_oConnector.to_block_in]
        if not outType == inType:
            print "Types mismatch"
        return outType == inType

    def ValidConnector(self,
                       newCon):  # checks whether the new Cn links to a already used input (in this case, also invalidating cloned connectors)
        for oldCon in self.connectors:
            if oldCon.to_block == newCon.to_block \
                    and oldCon.to_block_in == newCon.to_block_in:
                print "Cloned Connector"
                return False
        if newCon.to_block == newCon.from_block:
            print "Recursive \"from future\" connector"
            return False
        return True

    def ClickedOutput(self, block_id, a_nOutput):
        self.AbortConnection()  # abort any possibly running connections
        # print "block" + str(block_id) + "_Out" + str(a_nOutput)
        self.curr_connector = GcdConnector.GcdConnector(self, block_id, a_nOutput)
        self.update_flows()

    def AbortConnection(self):
        if self.curr_connector != None:
            self.curr_connector.group.destroy()  ## BUG!
            del self.curr_connector
            self.curr_connector = None

    def DeleteBlock(self, blockCountId):
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

        self.update_flows()

    def UpdateWhiteBoard(self):
        if self.white_board == None:
            clr = ColorFromList([255, 255, 255, 255])
            self.white_board = self.root().add(gnomecanvas.CanvasRect, x1=-10000, y1=-10000, x2=10000, y2=10000,
                                            fill_color_rgba=clr)
            # should we change this size dynamically?? or make it simply a HUGE whiteboard?
            self.white_board.set_flags(gtk.CAN_FOCUS)
            self.white_board.connect("event", self.__white_board_event)

    # else:

    def update_flows(self):
        for checkTimeShifter in [False, True]:
            prevCount = -1
            newCount = self.CountFlowingComponents()
            while prevCount != newCount:
                # print "newCount:",newCount
                # print "prevCount:",prevCount
                for blockIdx in self.blocks:  # self.blocks is a dict!
                    self.blocks[blockIdx].update_flow(checkTimeShifter)
                for conn in self.connectors:
                    conn.update_flow()
                prevCount = newCount
                newCount = self.CountFlowingComponents()

    def GetConnectorsTo(self, a_nBlockCountId):
        result = []
        for conn in self.connectors:
            if conn.to_block == a_nBlockCountId:
                result.append(conn)
        return result

    def CountFlowingComponents(self):
        count = 0
        for blockIdx in self.blocks:
            if self.blocks[blockIdx].has_flow:
                count += 1
        for conn in self.connectors:
            if conn.has_flow:
                count += 1
        return count

    def __block_XML_out(self, t_oBlockIdx, Properties, Network, a_bKeepNonFlowing=False):
        if self.blocks[t_oBlockIdx].get_state() or a_bKeepNonFlowing:
            props = self.blocks[t_oBlockIdx].GetPropertiesXML()
            block_xml = props.getTagXML(props.getTagChild("properties", "block"))

            #Properties += self.blocks[t_oBlockIdx].GetPropertiesXML().properties.block.xml() + "\n  "
            Properties += block_xml + "\n  "
            Network += '<block type="' + str(self.blocks[t_oBlockIdx].get_type()) + '" id="' + str(
                self.blocks[t_oBlockIdx].get_id()) + '">\n'
            Network += "<inputs>\n"
            for t_nInputIdx in range(len(self.blocks[t_oBlockIdx].block_description["InTypes"])):
                Network += '<input id="' + str(
                    t_nInputIdx + 1) + '"/>\n'  # +1 pois o range eh de 0..x (precisamos do id 1...x+1)
            Network += "</inputs>\n"

            Network += "<outputs>\n"
            t_dConnectedOuts = {}
            for t_oConnector in self.connectors:
                if t_oConnector.from_block == self.blocks[t_oBlockIdx].get_id() and (
                    self.blocks[t_oConnector.to_block].get_state() or a_bKeepNonFlowing):
                    Network += '<output id="' + str(t_oConnector.from_block_out + 1) + '" inBlock="' + str(
                        t_oConnector.to_block) + '" input="' + str(
                        t_oConnector.to_block_in + 1) + '"/>\n'  # +1 pois o range eh de 0..x (precisamos do id 1...x+1)
                    t_dConnectedOuts[t_oConnector.from_block_out] = 1
            for Output in range(len(self.blocks[t_oBlockIdx].block_description["OutTypes"])):
                if not t_dConnectedOuts.has_key(Output):
                    Network += '<output id="' + str(Output + 1) + '" inBlock="--" input="--"/>\n'
            Network += "</outputs>\n"
            Network += "</block>\n"
        return (Properties, Network)

    def GetProcessChain(self, a_bKeepNonFlowing=False):
    # frontend will get only the valid chain although saving will include the invalid ones
        Properties = "<properties>\n  "
        Network = "<network>\n"

        ##REAL TRICKY BUG solution here, source blocks must be processed in an earlier phase so assumptions as "live" or not will be valid
        ##throughout the whole code generation

        for t_oBlockIdx in self.blocks:
            if self.blocks[t_oBlockIdx].m_bIsSource:
                (Properties, Network) = self.__block_XML_out(t_oBlockIdx, Properties, Network, a_bKeepNonFlowing)

        for t_oBlockIdx in self.blocks:
            if not self.blocks[t_oBlockIdx].m_bIsSource:
                (Properties, Network) = self.__block_XML_out(t_oBlockIdx, Properties, Network, a_bKeepNonFlowing)

        Properties += "</properties>\n"
        Network += "</network>\n"

        return Properties + Network

    def set_file_name(self, file_name):
        self.file_name = file_name

    def get_file_name(self):
        return self.file_name

    def Load(self, file_name=None):
        if file_name != None:
            self.set_file_name(file_name)
        else:
            if self.file_name == None:
                self.file_name = "Cannot Load without filename"
                return False

                # reseting present diagram..
        self.blocks, self.connectors, self.curr_connector, self.session_id = {}, [], None, 0

        # this two must be updated at each block/conn insertion
        self.block_id = 1  # since block counts are kept, render this from the saved file
        self.connector_id = 1  # since connector Ids are generated from scratch, just reset it

        #t_oLoad = bt.bind_file(self.file_name)  # binding saved project
        #print t_oLoad.xml()
        t_oLoad = XMLParser(self.file_name)

        # loading blocks on canvas
        #GcState_root = t_oLoad.getTagChild("harpia", "GcState")
        #blocks = t_oLoad.getChildTags(GcState_root, "block")
        blocks = t_oLoad.getTag("harpia").getTag("GcState").getChildTags("block")
        
        #for block in t_oLoad.harpia.GcState.block:
        for block in blocks:
            #block_id =  t_oLoad.getTagAttr(block, "id")
            #block_type =  t_oLoad.getTagAttr(block, "type")
            block_id =  block.getAttr("id")
            block_type =  block.getAttr("type")
            position = block.getTag("position")
            x = position.getAttr("x")
            y = position.getAttr("y")

            self.__insert_blockPosId(int(block_type), float(x), float(y), int(block_id))
            self.block_id = max(self.block_id, int(block_id))

        self.block_id += 1

        blocks = t_oLoad.getTag("harpia").getTag("network").getChildTags("block")

        # loading connectors on canvas
        try:
            #for block in t_oLoad.harpia.network.block:
            for block in blocks:
                block_id =  block.getAttr("id")
                outputs = block.getTag("outputs")

                #for connector in block.outputs.output:
                for connector in outputs.getChildTags("output"):
                    conn_input = connector.getAttr("input")
                    conn_inblock = connector.getAttr("inBlock")
                    conn_id = connector.getAttr("id")

                    print conn_input, conn_inblock, conn_id

                        #self.InsertReadyConnector(int(block.id), (int(connector.id) - 1), int(connector.inBlock),
                    if conn_inblock != "--" and conn_input != "--":
                                                  #(int(connector.input) - 1))
                        self.InsertReadyConnector(int(block_id), (int(conn_id) - 1), int(conn_inblock),
                                                  (int(conn_input) - 1))
                        # this "-1" are "paired" with those "+1" at line 286 (GetProcessChain:offset=14)
        except AttributeError:
            pass

        # loading properties
        blocks = t_oLoad.getTag("harpia").getTag("properties").getChildTags("block")

        for block in blocks:
            block_xml = str(block)
            block_id =  block.getAttr("id")
            #t_sBlockProperties = '<?xml version="1.0" encoding="UTF-8"?>\n<properties>\n' + block.xml() + '\n</properties>\n'
            t_sBlockProperties = '<?xml version="1.0" encoding="UTF-8"?>\n<properties>\n' + block_xml + '\n</properties>\n'

            #self.blocks[int(block.id)].SetPropertiesXML(bt.bind_string(t_sBlockProperties))
            self.blocks[int(block_id)].SetPropertiesXML(XMLParser(t_sBlockProperties, fromString=True))

        self.UpdateScrolling()
        self.GotoScrolling(0, 0)
        return True

    def Save(self, file_name=None):  # saving project
        if file_name != None:
            self.set_file_name(file_name)
        if self.file_name == None:
            self.file_name = "Cadeia_" + str(time.time()) + ".hrp"

            # saving blocks current state
        t_sGcState = "<GcState>\n"
        for blockIdx in self.blocks:
            t_sGcState += '\t<block type="' + str(self.blocks[blockIdx].get_type()) + '" id="' + str(
                self.blocks[blockIdx].get_id()) + '">\n'
            t_tPos = self.blocks[blockIdx].get_position()
            t_sGcState += '\t\t<position x="' + str(t_tPos[0]) + '" y="' + str(t_tPos[1]) + '"/>\n'
            t_sGcState += '\t</block>\n'
        t_sGcState += "</GcState>\n"

        # saving processing chain (which includes blocks properties and conectors)
        t_sProcessingChain = self.GetProcessChain(True)

        t_sOutFile = "<harpia>\n" + t_sGcState + t_sProcessingChain + "</harpia>\n"

        if self.file_name.find(".hrp") == -1:
            self.file_name += ".hrp"

        t_oSaveFile = open(str(self.file_name), "w")
        t_oSaveFile.write(t_sOutFile)
        t_oSaveFile.close()

    def GetBlockOnFocus(self):
        for blockIdx in self.blocks:
            if self.blocks[blockIdx].focus:
                return blockIdx

    def SetIDBackendSession(self, session_id):
        self.session_id = session_id

    def GetIDBackendSession(self):
        return self.session_id

    def Export2Png(self, filepath="diagrama.png"):
        (x, y, t_nWidth, t_nHeight, t_nDepth) = self.window.get_geometry()
        t_oPixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, t_nWidth, t_nHeight)
        t_oBuffer = t_oPixbuf.get_from_drawable(self.window, self.get_colormap(), 0, 0, 0, 0, t_nWidth, t_nHeight)
        # get_from_drawable(GdkWindow src, GdkColormap cmap, int src_x, int src_y, int dest_x, int dest_y, int width, int height);
        t_oBuffer.save(filepath, "png")
        # bugs:

    # *nao considera o que estiver fora do scroll region
    # *da um printScreen somente então pega qlqr outra coisa q estiver no caminho
    # (incluindo o proprio menu ali do FILE)
    # *aparentemente é a maneira errada.

    def set_error_log(self, a_sErrorLog):
        self.error_log = a_sErrorLog

    def append_error_log(self, a_sErrorLog):
        self.error_log += a_sErrorLog

    def get_error_log(self):
        return self.error_log

    def zoom_in(self):
        self.zoom *= 1.1
        self.set_pixels_per_unit(self.zoom)

    def zoom_out(self):
        self.zoom *= 0.9
        self.set_pixels_per_unit(self.zoom)

    def zoom_orig(self):
        self.zoom = 1.0
        self.set_pixels_per_unit(self.zoom)

