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

from harpia.s2idirectory import *


class DiagramControl():

    # ----------------------------------------------------------------------
    def __init__(self, diagram):
        self.diagram = diagram

# ----------------------------------------------------------------------
    def __del__(self):
        pass

# ----------------------------------------------------------------------
    def __block_XML_out(self, block_id, properties, network):
        props = self.diagram.blocks[block_id].get_xml()
        if isinstance(props, (str, unicode)):
            props = XMLParser(props, fromString=True)
        block_xml = props.getTagXML(props.getTagChild("properties", "block"))

        properties += block_xml + "\n  "
        network += '<block type="' + str(self.diagram.blocks[block_id].get_type()) + '" id="' + str(
            self.diagram.blocks[block_id].get_id()) + '">\n'
        network += "<inputs>\n"
        for t_nInputIdx in range(len(self.diagram.blocks[block_id].get_description()["InTypes"])):
            network += '<input id="' + str(t_nInputIdx + 1) + '"/>\n'
            # +1 pois o range eh de 0..x (precisamos do id 1...x+1)
        network += "</inputs>\n"

        network += "<outputs>\n"
        connected_outs = {}
        for connector in self.diagram.connectors:
            if connector.from_block == self.diagram.blocks[block_id].get_id():
                network += '<output id="' + str(connector.from_block_out + 1) + '" inBlock="' + str(
                    connector.to_block) + '" input="' + str(
                    connector.to_block_in + 1) + '"/>\n'  # +1 pois o range eh de 0..x (precisamos do id 1...x+1)
                connected_outs[connector.from_block_out] = 1
        for Output in range(len(self.diagram.blocks[block_id].get_description()["OutTypes"])):
            if not connected_outs.has_key(Output):
                network += '<output id="' + str(Output + 1) + '" inBlock="--" input="--"/>\n'
        network += "</outputs>\n"
        network += "</block>\n"
        return (properties, network)

# ----------------------------------------------------------------------
    def load(self, file_name=None):
        if file_name != None:
            self.diagram.set_file_name(file_name)
        else:
            if self.diagram.get_file_name() == None:
                harpia.s2idirectory.Log.log("Cannot Load without filename")
                return False

        # load the diagram
        xml_loader = XMLParser(self.diagram.get_file_name())
        blocks = xml_loader.getTag("harpia").getTag("GcState").getChildTags("block")

        for block in blocks:
            if block.getAttr("type") not in harpia.s2idirectory.block:
                continue
            block_id =  block.getAttr("id")
            block_type =  block.getAttr("type")
            position = block.getTag("position")
            x = position.getAttr("x")
            y = position.getAttr("y")


            self.diagram.insert_blockPosId(harpia.s2idirectory.block[block_type](), float(x), float(y), block_id)
            self.diagram.block_id = max(self.diagram.block_id, block_id)

        self.diagram.block_id = int(self.diagram.block_id) + 1

        # loading connectors on canvas
        blocks = xml_loader.getTag("harpia").getTag("network").getChildTags("block")
        try:
            #for block in xml_loader.harpia.network.block:
            for block in blocks:
                if block.getAttr("type") not in harpia.s2idirectory.block:
                    harpia.s2idirectory.Log.log("Block not found: " + block.getAttr("type"))
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
                                                block_id,
                                                (int(conn_id) - 1),
                                                conn_inblock,
                                                (int(conn_input) - 1))
        except AttributeError:
            pass

        # loading properties
        blocks = xml_loader.getTag("harpia").getTag("properties").getChildTags("block")
        for block in blocks:
            block_xml = str(block)
            block_id =  block.getAttr("id")
            block_properties = '<?xml version="1.0" encoding="UTF-8"?>\n<properties>\n' + block_xml + '\n</properties>\n'
            if block_id in self.diagram.blocks:
                self.diagram.blocks[block_id].set_xml(XMLParser(block_properties, fromString=True))
            else:
                self.diagram.main_window.status.append_text("Block not found!")
                self.diagram.main_window.status.append_text(str(block_id))

        self.diagram.update_scrolling()
        return True

# ----------------------------------------------------------------------
    def save(self, file_name=None):  # saving project
        if file_name != None:
            self.diagram.set_file_name(file_name)
        if self.diagram.get_file_name() == None:
            self.diagram.set_file_name("Cadeia_" + str(time.time()) + ".hrp")

        # saving blocks current state
        state = "<GcState>\n"
        for blockIdx in self.diagram.blocks:
            state += '\t<block type="' + \
                    str(self.diagram.blocks[blockIdx].get_type()) + \
                    '" id="' + str(self.diagram.blocks[blockIdx].get_id()) + \
                    '">\n'
            pos = self.diagram.blocks[blockIdx].get_position()
            state += '\t\t<position x="' + str(pos[0]) + '" y="' + str(pos[1]) + '"/>\n'
            state += '\t</block>\n'
        state += "</GcState>\n"

        # saving processing chain (which includes blocks properties and conectors)
        properties = "<properties>\n  "
        network = "<network>\n"

        for block_id in self.diagram.blocks:
            (properties, network) = self.__block_XML_out(block_id, properties, network)

        properties += "</properties>\n"
        network += "</network>\n"


        out_file = "<harpia>\n" + state + properties + network + "</harpia>\n"

        if self.diagram.get_file_name().find(".hrp") == -1:
            self.diagram.set_file_name(self.diagram.get_file_name() + ".hrp")

        try:
            save_file = open(str(self.diagram.get_file_name()), "w")
            out_file = out_file.encode('utf-8')
            save_file.write(out_file)
            save_file.close()
        except IOError as e:
            return False,e.strerror

        self.diagram.set_modified(False)
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

