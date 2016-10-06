# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------

import os
import gi
from gi.repository import Gdk
from exceptions import AttributeError
from harpia.utils.XMLUtils import XMLParser
from harpia.system import System as System
from harpia.control.codegenerator import CodeGenerator


class DiagramControl():

    # ----------------------------------------------------------------------
    def __init__(self, diagram):
        self.diagram = diagram

# ----------------------------------------------------------------------
    def __del__(self):
        pass

# ----------------------------------------------------------------------
    def get_generator(self):
        try:
            generator = System.generators[self.diagram.language](self.diagram)
        except:
            generator = CodeGenerator(self.diagram)
            System.log("Language generator not available")
        return generator

# ----------------------------------------------------------------------
    def load(self, file_name=None):
        if file_name is not None:
            self.diagram.set_file_name(file_name)
        else:
            if self.diagram.get_file_name() is None:
                System.log("Cannot Load without filename")
                return False
        if not os.path.exists(self.diagram.get_file_name()):
            System.log("File '" + self.diagram.get_file_name() +
                       "' does not exist!")
            return False

        # load the diagram
        xml_loader = XMLParser(self.diagram.get_file_name())

        zoom = xml_loader.getTag("harpia").getTag("zoom").getAttr("value")
        self.diagram.set_zoom(float(zoom))
        try:
            language = xml_loader.getTag("harpia").getTag(
                "language").getAttr("value")
            self.diagram.language = language
        except:
            pass

        # new version load
        blocks = xml_loader.getTag("harpia").getTag(
            "blocks").getChildTags("block")
        for block in blocks:
            block_type = block.getAttr("type")
            if block_type not in System.blocks:
                continue
            block_id = block.getAttr("id")
            position = block.getTag("position")
            x = position.getAttr("x")
            y = position.getAttr("y")
            properties = block.getChildTags("property")
            props = {}
            for prop in properties:
                props[prop.name] = prop.value
            new_block = System.blocks[block_type]()
            new_block.set_properties(props)
            new_block.set_id(block_id)
            new_block.x = float(x)
            new_block.y = float(y)
            self.diagram.add_block(new_block)

        connections = xml_loader.getTag("harpia").getTag(
            "connections").getChildTags("connection")
        for conn in connections:
            from_block = conn.getAttr("from")
            to_block = conn.getAttr("to")
            from_block_out = int(conn.getAttr("from_out"))
            to_block_in = int(conn.getAttr("to_in"))
            self.diagram.start_connection(
                self.diagram.blocks[from_block], from_block_out - 1)
            self.diagram.end_connection(
                self.diagram.blocks[to_block], to_block_in - 1)
        self.diagram.update_scrolling()
        self.diagram.reset_undo()

# ----------------------------------------------------------------------
    def save(self, file_name=None):

        output = "<harpia>\n"

        output += "<version value='" + str(System.VERSION) + "' />\n"
        output += "<zoom value='" + str(self.diagram.get_zoom()) + "' />\n"
        output += "<language value='" + str(self.diagram.language) + "' />\n"
        output += "<blocks>\n  "
        for block_id in self.diagram.blocks:
            block_type = str(self.diagram.blocks[block_id].get_type())
            pos = self.diagram.blocks[block_id].get_position()

            output += "\t<block type='" + block_type + \
                "' id='" + str(block_id) + "'>\n"
            output += '\t\t<position x="' + \
                str(pos[0]) + '" y="' + str(pos[1]) + '"/>\n'
            output += self.diagram.blocks[block_id].get_xml()
            output += "\t</block>\n"
        output += "</blocks>\n"

        output += "<connections>\n  "
        for connector in self.diagram.connectors:
            output += '\t<connection from="' + str(connector.from_block) + \
                '" from_out="' + str(connector.from_block_out + 1) + \
                '" to="' + str(connector.to_block) + \
                '" to_in="' + \
                str(connector.to_block_in + 1) + '"/>\n'
        output += "</connections>\n"

        output += "</harpia>\n"

        if file_name is not None:
            self.diagram.set_file_name(file_name)
        if self.diagram.get_file_name() is None:
            self.diagram.set_file_name("Cadeia_" + str(time.time()) + ".hrp")
        if self.diagram.get_file_name().find(".hrp") == -1:
            self.diagram.set_file_name(self.diagram.get_file_name() + ".hrp")

        try:
            save_file = open(str(self.diagram.get_file_name()), "w")
            output = output
            save_file.write(output)
            save_file.close()
        except IOError as e:
            System.log(e.strerror)
            return False, e.strerror

        self.diagram.set_modified(False)
        return True, "Success"

# ----------------------------------------------------------------------
    def export_png(self, file_name="diagrama.png"):
        if file_name is None:
            file_name = "diagrama.png"

        x, y, width, height = self.diagram.get_min_max()

        if x < 0 or y < 0:
            self.diagram.reload()
            x, y, width, height = self.diagram.get_min_max()

        pixbuf = Gdk.pixbuf_get_from_window(
            self.diagram.get_window(), x, y, width, height)

        if pixbuf is None:
            return False, "No image to export"

        test, tmp_buffer = pixbuf.save_to_bufferv("png",  [], [])

        try:
            save_file = open(file_name, "w")
            save_file.write(tmp_buffer)
            save_file.close()
        except IOError as e:
            System.log(e.strerror)
            return False, e.strerror

        return True, ""
# ------------------------------------------------------------------------------
