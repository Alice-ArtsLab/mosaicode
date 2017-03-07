# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the DiagramControl class.
"""
import os
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from harpia.utils.XMLUtils import XMLParser
from harpia.system import System as System
from harpia.control.codegenerator import CodeGenerator
from harpia.model.codetemplate import CodeTemplate


class DiagramControl():
    """
    This class contains methods related the DiagramControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self, diagram):
        self.diagram = diagram

# ----------------------------------------------------------------------
    def get_code_template(self):
        try:
            generator = CodeGenerator(self.diagram,
                    System.code_templates[self.diagram.language])
        except:
            generator = CodeGenerator(self.diagram, CodeTemplate())
            System.log("Language generator not available")
        return generator

# ----------------------------------------------------------------------
    def load(self, file_name=None):
        """
        This method load a file.

        Returns:
            * **Types** (:class:`boolean<boolean>`)
        """
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
        parser = XMLParser(self.diagram.get_file_name())

        zoom = parser.getTag("harpia").getTag("zoom").getAttr("value")
        self.diagram.set_zoom(float(zoom))
        try:
            language = parser.getTag("harpia").getTag(
                "language").getAttr("value")
            self.diagram.language = language
        except:
            pass

        # new version load
        blocks = parser.getTag("harpia").getTag(
            "blocks").getChildTags("block")
        for block in blocks:
            block_type = block.getAttr("type")
            if block_type not in System.plugins:
                continue
            block_id = block.getAttr("id")
            position = block.getTag("position")
            x = position.getAttr("x")
            y = position.getAttr("y")
            properties = block.getChildTags("property")
            props = {}
            for prop in properties:
                try:
                    props[prop.key] = prop.value
                except:
                    pass
            new_block = System.plugins[block_type]
            new_block.set_properties(props)
            new_block.set_id(block_id)
            new_block.x = float(x)
            new_block.y = float(y)
            self.diagram.add_block(new_block)

        connections = parser.getTag("harpia").getTag(
            "connections").getChildTags("connection")
        for conn in connections:
            try:
                from_block = self.diagram.blocks[
                    int(conn.getAttr("from_block"))]
                to_block = self.diagram.blocks[int(conn.getAttr("to_block"))]
            except:
                continue
            from_block_out = int(conn.getAttr("from_out"))
            to_block_in = int(conn.getAttr("to_in"))
            self.diagram.start_connection(from_block, int(from_block_out) - 1)
            self.diagram.end_connection(to_block, int(to_block_in) - 1)
        self.diagram.reset_undo()

# ----------------------------------------------------------------------
    def save(self, file_name=None):
        """
        This method save a file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """

        parser = XMLParser()
        parser.addTag('harpia')
        parser.appendToTag('harpia', 'version', value=System.VERSION)
        parser.appendToTag('harpia', 'zoom', value=self.diagram.get_zoom())
        parser.appendToTag('harpia', 'language', value=self.diagram.language)

        parser.appendToTag('harpia', 'blocks')
        for block_id in self.diagram.blocks:
            block_type = self.diagram.blocks[block_id].get_type()
            pos = self.diagram.blocks[block_id].get_position()
            parser.appendToTag('blocks', 'block', type=block_type, id=block_id)
            parser.appendToLastTag('block', 'position', x=pos[0], y=pos[1])
            props = self.diagram.blocks[block_id].get_properties()
            for prop in props:
                parser.appendToLastTag('block',
                                       'property',
                                       key=str(prop["name"]),
                                       value=str(prop["value"])
                                       )

        parser.appendToTag('harpia', 'connections')
        for connector in self.diagram.connectors:
            parser.appendToTag('connections', 'connection',
                               from_block=connector.source.get_id(),
                               from_out=int(connector.source_port) + 1,
                               to_block=connector.sink.get_id(),
                               to_in=int(connector.sink_port) + 1)

        if file_name is not None:
            self.diagram.set_file_name(file_name)
        if self.diagram.get_file_name() is None:
            self.diagram.set_file_name("Cadeia_" + str(time.time()) + ".hrp")
        if self.diagram.get_file_name().find(".hrp") == -1:
            self.diagram.set_file_name(self.diagram.get_file_name() + ".hrp")

        try:
            save_file = open(str(self.diagram.get_file_name()), "w")
            save_file.write(parser.prettify())
            save_file.close()
        except IOError as e:
            System.log(e.strerror)
            return False, e.strerror

        self.diagram.set_modified(False)
        return True, "Success"

# ----------------------------------------------------------------------
    def export_png(self, file_name="diagrama.png"):
        """
        This method export a png.

        Returns:

            * **Types** (:class:`boolean<boolean>`): True to Success.
        """
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
