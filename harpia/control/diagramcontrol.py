# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import GooCanvas

from exceptions import AttributeError

from harpia.utils.XMLUtils import XMLParser
from harpia.utils.graphicfunctions import *

import harpia.s2idirectory
from harpia.s2idirectory import *


class DiagramControl():

# ----------------------------------------------------------------------
    def __init__(self, diagram):
        self.diagram = diagram

# ----------------------------------------------------------------------
    def __del__(self):
        pass

# ----------------------------------------------------------------------
    def __block_XML_out(self, t_oBlockIdx, Properties, Network):
        props = self.diagram.blocks[t_oBlockIdx].get_xml()
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
            if t_oConnector.from_block == self.diagram.blocks[t_oBlockIdx].get_id():
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

# ----------------------------------------------------------------------
    def load(self, file_name=None):
        if file_name != None:
            self.diagram.set_file_name(file_name)
        else:
            if self.diagram.file_name == None:
                self.diagram.file_name = "Cannot Load without filename"
                return False

        # reseting present diagram..
#        self.diagram.blocks = {}
#        self.diagram.connectors = []
#        self.diagram.curr_connector = None
#        self.diagram.session_id = 0
#        self.diagram.block_id = 1  # since block counts are kept, render this from the saved file
#        self.diagram.connector_id = 1  # since connector Ids are generated from scratch, just reset it

        # load the diagram
        xml_loader = XMLParser(self.diagram.file_name)
        blocks = xml_loader.getTag("harpia").getTag("GcState").getChildTags("block")

        for block in blocks:
            if block.getAttr("type") not in harpia.s2idirectory.block:
                continue
            block_id =  block.getAttr("id")
            block_type =  block.getAttr("type")
            position = block.getTag("position")
            x = position.getAttr("x")
            y = position.getAttr("y")


            self.diagram.insert_blockPosId(harpia.s2idirectory.block[block_type](), float(x), float(y), int(block_id))
            self.diagram.block_id = max(self.diagram.block_id, int(block_id))

        self.diagram.block_id += 1

        # loading connectors on canvas
        blocks = xml_loader.getTag("harpia").getTag("network").getChildTags("block")
        try:
            #for block in xml_loader.harpia.network.block:
            for block in blocks:
                if block.getAttr("type") not in harpia.s2idirectory.block:
                    
                    continue
                block_id =  block.getAttr("id")
                outputs = block.getTag("outputs")

                #for connector in block.outputs.output:
                for connector in outputs.getChildTags("output"):
                    conn_input = connector.getAttr("input")
                    conn_inblock = connector.getAttr("inBlock")
                    conn_id = connector.getAttr("id")

                    if conn_inblock != "--" and conn_input != "--":
                        self.diagram.insert_ready_connector(
                                                int(block_id),
                                                (int(conn_id) - 1),
                                                int(conn_inblock),
                                                (int(conn_input) - 1))
        except AttributeError:
            pass

        # loading properties
        blocks = xml_loader.getTag("harpia").getTag("properties").getChildTags("block")
        for block in blocks:
            block_xml = str(block)
            block_id =  block.getAttr("id")
            t_sBlockProperties = '<?xml version="1.0" encoding="UTF-8"?>\n<properties>\n' + block_xml + '\n</properties>\n'
            self.diagram.blocks[int(block_id)].set_xml(XMLParser(t_sBlockProperties, fromString=True))

        self.diagram.update_scrolling()
        return True

# ----------------------------------------------------------------------
    def save(self, file_name=None):  # saving project
        if file_name != None:
            self.diagram.set_file_name(file_name)
        if self.diagram.file_name == None:
            self.diagram.file_name = "Cadeia_" + str(time.time()) + ".hrp"

        # saving blocks current state
        t_sGcState = "<GcState>\n"
        for blockIdx in self.diagram.blocks:
            t_sGcState += '\t<block type="' + str(self.diagram.blocks[blockIdx].get_type()) + '" id="' + str(self.diagram.blocks[blockIdx].get_id()) + '">\n'
            t_tPos = self.diagram.blocks[blockIdx].get_position()
            t_sGcState += '\t\t<position x="' + str(t_tPos[0]) + '" y="' + str(t_tPos[1]) + '"/>\n'
            t_sGcState += '\t</block>\n'
        t_sGcState += "</GcState>\n"

        # saving processing chain (which includes blocks properties and conectors)
        Properties = "<properties>\n  "
        Network = "<network>\n"

        for t_oBlockIdx in self.diagram.blocks:
            if self.diagram.blocks[t_oBlockIdx].is_source:
                (Properties, Network) = self.__block_XML_out(t_oBlockIdx, Properties, Network)

        for t_oBlockIdx in self.diagram.blocks:
            if not self.diagram.blocks[t_oBlockIdx].is_source:
                (Properties, Network) = self.__block_XML_out(t_oBlockIdx, Properties, Network)

        Properties += "</properties>\n"
        Network += "</network>\n"
        t_sProcessingChain =  Properties + Network

        t_sOutFile = "<harpia>\n" + t_sGcState + t_sProcessingChain + "</harpia>\n"

        if self.diagram.file_name.find(".hrp") == -1:
            self.diagram.file_name += ".hrp"

        try:
            save_file = open(str(self.diagram.file_name), "w")
            t_sOutFile = t_sOutFile.encode('utf-8')
            save_file.write(t_sOutFile)
            save_file.close()
        except IOError as e:
            return False,e.strerror
        return True,"Success"

# ----------------------------------------------------------------------
    def export_png(self, filepath="diagrama.png"):
        (x, y, width, height) = self.diagram.get_parent_window().get_geometry()
        pixbuf = Gdk.pixbuf_get_from_window(
                self.diagram.get_parent_window(), x, y, width, height)

        test, tmp_buffer = pixbuf.save_to_bufferv("png",  [], [])

        save_file = open(filepath, "w")
        save_file.write(tmp_buffer)
        save_file.close()

# ----------------------------------------------------------------------

