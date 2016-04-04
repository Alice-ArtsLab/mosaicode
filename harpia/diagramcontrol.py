# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------

import gnomecanvas
import GcdBlock
import GcdConnector
import GcDiagram
import gtk
import time

from exceptions import AttributeError

from utils.XMLUtils import XMLParser
from utils.graphicfunctions import *


class DiagramControl():
    def __init__(self, diagram):
        self.diagram = diagram

    def __del__(self):
        pass

    def __block_XML_out(self, t_oBlockIdx, Properties, Network, a_bKeepNonFlowing=False):
        if self.diagram.blocks[t_oBlockIdx].get_state() or a_bKeepNonFlowing:
            props = self.diagram.blocks[t_oBlockIdx].GetPropertiesXML()
            block_xml = props.getTagXML(props.getTagChild("properties", "block"))

            Properties += block_xml + "\n  "
            Network += '<block type="' + str(self.diagram.blocks[t_oBlockIdx].get_type()) + '" id="' + str(
                self.diagram.blocks[t_oBlockIdx].get_id()) + '">\n'
            Network += "<inputs>\n"
            for t_nInputIdx in range(len(self.diagram.blocks[t_oBlockIdx].block_description["InTypes"])):
                Network += '<input id="' + str(t_nInputIdx + 1) + '"/>\n'
                # +1 pois o range eh de 0..x (precisamos do id 1...x+1)
            Network += "</inputs>\n"

            Network += "<outputs>\n"
            t_dConnectedOuts = {}
            for t_oConnector in self.diagram.connectors:
                if t_oConnector.from_block == self.diagram.blocks[t_oBlockIdx].get_id() and (
                    self.diagram.blocks[t_oConnector.to_block].get_state() or a_bKeepNonFlowing):
                    Network += '<output id="' + str(t_oConnector.from_block_out + 1) + '" inBlock="' + str(
                        t_oConnector.to_block) + '" input="' + str(
                        t_oConnector.to_block_in + 1) + '"/>\n'  # +1 pois o range eh de 0..x (precisamos do id 1...x+1)
                    t_dConnectedOuts[t_oConnector.from_block_out] = 1
            for Output in range(len(self.diagram.blocks[t_oBlockIdx].block_description["OutTypes"])):
                if not t_dConnectedOuts.has_key(Output):
                    Network += '<output id="' + str(Output + 1) + '" inBlock="--" input="--"/>\n'
            Network += "</outputs>\n"
            Network += "</block>\n"
        return (Properties, Network)

    def __get_process_chain(self, a_bKeepNonFlowing=False):
    # frontend will get only the valid chain although saving will include the invalid ones
        Properties = "<properties>\n  "
        Network = "<network>\n"

        ##REAL TRICKY BUG solution here, source blocks must be processed in an earlier phase so assumptions as "live" or not will be valid
        ##throughout the whole code generation

        for t_oBlockIdx in self.diagram.blocks:
            if self.diagram.blocks[t_oBlockIdx].is_source:
                (Properties, Network) = self.__block_XML_out(t_oBlockIdx, Properties, Network, a_bKeepNonFlowing)

        for t_oBlockIdx in self.diagram.blocks:
            if not self.diagram.blocks[t_oBlockIdx].is_source:
                (Properties, Network) = self.__block_XML_out(t_oBlockIdx, Properties, Network, a_bKeepNonFlowing)

        Properties += "</properties>\n"
        Network += "</network>\n"

        return Properties + Network

    def load(self, file_name=None):
        if file_name != None:
            self.diagram.set_file_name(file_name)
        else:
            if self.diagram.file_name == None:
                self.diagram.file_name = "Cannot Load without filename"
                return False

        # reseting present diagram..
        self.diagram.blocks = {}
        self.diagram.connectors = []
        self.diagram.curr_connector = None
        self.diagram.session_id = 0

        # this two must be updated at each block/conn insertion
        self.diagram.block_id = 1  # since block counts are kept, render this from the saved file
        self.diagram.connector_id = 1  # since connector Ids are generated from scratch, just reset it

        t_oLoad = XMLParser(self.diagram.file_name)
        blocks = t_oLoad.getTag("harpia").getTag("GcState").getChildTags("block")

        #for block in t_oLoad.harpia.GcState.block:
        for block in blocks:
            block_id =  block.getAttr("id")
            block_type =  block.getAttr("type")
            position = block.getTag("position")
            x = position.getAttr("x")
            y = position.getAttr("y")

            self.diagram.insert_blockPosId(int(block_type), float(x), float(y), int(block_id))
            self.diagram.block_id = max(self.diagram.block_id, int(block_id))

        self.diagram.block_id += 1

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

                    if conn_inblock != "--" and conn_input != "--":
                        #(int(connector.input) - 1))
                        self.diagram.insert_ready_connector(
                                                int(block_id),
                                                (int(conn_id) - 1),
                                                int(conn_inblock),
                                                (int(conn_input) - 1))
                        # this "-1" are "paired" with those "+1" at line 286 (__get_process_chain:offset=14)
        except AttributeError:
            pass

        # loading properties
        blocks = t_oLoad.getTag("harpia").getTag("properties").getChildTags("block")

        for block in blocks:
            block_xml = str(block)
            block_id =  block.getAttr("id")
            t_sBlockProperties = '<?xml version="1.0" encoding="UTF-8"?>\n<properties>\n' + block_xml + '\n</properties>\n'
            self.diagram.blocks[int(block_id)].SetPropertiesXML(XMLParser(t_sBlockProperties, fromString=True))

        self.diagram.update_scrolling()
        self.diagram.goto_scrolling(0, 0)
        return True

    def save(self, file_name=None):  # saving project
        if file_name != None:
            self.diagram.set_file_name(file_name)
        if self.diagram.file_name == None:
            self.diagram.file_name = "Cadeia_" + str(time.time()) + ".hrp"

            # saving blocks current state
        t_sGcState = "<GcState>\n"
        for blockIdx in self.diagram.blocks:
            t_sGcState += '\t<block type="' + str(self.diagram.blocks[blockIdx].get_type()) + '" id="' + str(
                self.diagram.blocks[blockIdx].get_id()) + '">\n'
            t_tPos = self.diagram.blocks[blockIdx].get_position()
            t_sGcState += '\t\t<position x="' + str(t_tPos[0]) + '" y="' + str(t_tPos[1]) + '"/>\n'
            t_sGcState += '\t</block>\n'
        t_sGcState += "</GcState>\n"

        # saving processing chain (which includes blocks properties and conectors)
        t_sProcessingChain = self.__get_process_chain(True)

        t_sOutFile = "<harpia>\n" + t_sGcState + t_sProcessingChain + "</harpia>\n"

        if self.diagram.file_name.find(".hrp") == -1:
            self.diagram.file_name += ".hrp"

        t_oSaveFile = open(str(self.diagram.file_name), "w")
        t_oSaveFile.write(t_sOutFile)
        t_oSaveFile.close()

    def export_png(self, filepath="diagrama.png"):
        (x, y, t_nWidth, t_nHeight, t_nDepth) = self.diagram.window.get_geometry()
        t_oPixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, t_nWidth, t_nHeight)
        t_oBuffer = t_oPixbuf.get_from_drawable(self.diagram.window, self.diagram.get_colormap(), 0, 0, 0, 0, t_nWidth, t_nHeight)
        # get_from_drawable(GdkWindow src, GdkColormap cmap, int src_x, int src_y, int dest_x, int dest_y, int width, int height);
        t_oBuffer.save(filepath, "png")
        # bugs:

    # *nao considera o que estiver fora do scroll region
    # *da um printScreen somente então pega qlqr outra coisa q estiver no caminho
    # (incluindo o proprio menu ali do FILE)
    # *aparentemente é a maneira errada.

