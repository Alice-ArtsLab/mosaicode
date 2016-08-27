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
from harpia.constants import *


class DiagramControl():

    # ----------------------------------------------------------------------
    def __init__(self, diagram):
        self.diagram = diagram

# ----------------------------------------------------------------------
    def __del__(self):
        pass

# ----------------------------------------------------------------------
    def load(self, file_name=None):
        if file_name != None:
            self.diagram.set_file_name(file_name)
        else:
            if self.diagram.get_file_name() == None:
                harpia.s2idirectory.Log.log("Cannot Load without filename")
                return False
        if not os.path.exists(self.diagram.get_file_name()):
            harpia.s2idirectory.Log.log("File '" + self.diagram.get_file_name() + "' does not exist!")
            return False

        # load the diagram
        xml_loader = XMLParser(self.diagram.get_file_name())

        # test for old version
        blocks = xml_loader.getTag("harpia").getTag("GcState").getChildTags("block")
        if len(blocks) > 0:
            return self.__load_old(xml_loader)

        zoom = xml_loader.getTag("harpia").getTag("zoom").getAttr("value")
        self.diagram.set_zoom(float(zoom))

        # new version load
        blocks = xml_loader.getTag("harpia").getTag("blocks").getChildTags("block")
        for block in blocks:
            block_type =  block.getAttr("type")
            if block_type not in harpia.s2idirectory.block:
                continue
            block_id =  block.getAttr("id")
            position = block.getTag("position")
            x = position.getAttr("x")
            y = position.getAttr("y")
            properties = block.getChildTags("property")
            props = {}
            for prop in properties:
                props[prop.name] = prop.value
            new_block = harpia.s2idirectory.block[block_type]()
            new_block.set_properties(props)
            new_block.set_id(block_id)
            new_block.x = float(x)
            new_block.y = float(y)
            self.diagram.load_block(new_block)
            self.diagram.block_id = max(self.diagram.block_id, block_id)
        self.diagram.block_id = int(self.diagram.block_id) + 1

        connections = xml_loader.getTag("harpia").getTag("connections").getChildTags("connection")
        for conn in connections:
            from_block = conn.getAttr("from")
            to_block = conn.getAttr("to")
            from_block_out = conn.getAttr("from_out")
            to_block_in = conn.getAttr("to_in")
            self.diagram.insert_ready_connector(
                                    from_block,
                                    (int(from_block_out) - 1),
                                    to_block,
                                    (int(to_block_in) - 1))
        self.diagram.update_scrolling()

# ----------------------------------------------------------------------
    def __load_old(self, xml_loader):
        blocks = xml_loader.getTag("harpia").getTag("GcState").getChildTags("block")

        for block in blocks:
            if block.getAttr("type") not in harpia.s2idirectory.block:
                continue
            block_id =  block.getAttr("id")
            block_type =  block.getAttr("type")
            position = block.getTag("position")
            x = position.getAttr("x")
            y = position.getAttr("y")
            new_block = harpia.s2idirectory.block[block_type]()
            new_block.set_id(block_id)
            new_block.x = float(x)
            new_block.y = float(y)
            self.diagram.load_block(new_block)
            self.diagram.block_id = max(self.diagram.block_id, block_id)

        self.diagram.block_id = int(self.diagram.block_id) + 1

        # loading connectors on canvas
        blocks = xml_loader.getTag("harpia").getTag("network").getChildTags("block")
        try:
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
            props = {}
            properties = block.getChildTags("property")
            for prop in properties:
                props[prop.name] = prop.value

            if block_id in self.diagram.blocks:
                self.diagram.blocks[block_id].set_properties(props)
            else:
                harpia.s2idirectory.Log.log("Block " + str(block_id) + "not found!")

        self.diagram.update_scrolling()
        return True

# ----------------------------------------------------------------------
    def save(self, file_name=None):  # saving project

        output = "<harpia>\n"

        output += "<version value='" + str(VERSION) + "' />\n"
        output += "<zoom value='" + str(self.diagram.get_zoom()) + "' />\n"
        output += "<blocks>\n  "
        for block_id in self.diagram.blocks:
            block_type = str(self.diagram.blocks[block_id].get_type())
            pos = self.diagram.blocks[block_id].get_position()

            output += "\t<block type='" + block_type + "' id='" + str(block_id) + "'>\n"
            output += '\t\t<position x="' + str(pos[0]) + '" y="' + str(pos[1]) + '"/>\n'
            output += self.diagram.blocks[block_id].get_xml()
            output += "\t</block>\n"
        output += "</blocks>\n"

        output += "<connections>\n  "
        for connector in self.diagram.connectors:
            output += '\t<connection from="' + str(connector.from_block) + \
                            '" from_out="' + str(connector.from_block_out + 1) + \
                            '" to="' + str(connector.to_block) + \
                            '" to_in="' + str(connector.to_block_in + 1) + '"/>\n'
        output += "</connections>\n"

        output += "</harpia>\n"

        if file_name != None:
            self.diagram.set_file_name(file_name)
        if self.diagram.get_file_name() == None:
            self.diagram.set_file_name("Cadeia_" + str(time.time()) + ".hrp")
        if self.diagram.get_file_name().find(".hrp") == -1:
            self.diagram.set_file_name(self.diagram.get_file_name() + ".hrp")

        try:
            save_file = open(str(self.diagram.get_file_name()), "w")
            output = output.encode('utf-8')
            save_file.write(output)
            save_file.close()
        except IOError as e:
            harpia.s2idirectory.Log.log(e.strerror)
            return False, e.strerror

        self.diagram.set_modified(False)
        return True, "Success"

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

