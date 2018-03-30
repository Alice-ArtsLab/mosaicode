# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the DiagramPersistence class.
"""
import os
import gi
from copy import deepcopy
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from mosaicode.utils.XMLUtils import XMLParser
from mosaicode.system import System as System
from mosaicode.model.connectionmodel import ConnectionModel

tag_name = "mosaicode"

class DiagramPersistence():
    """
    This class contains methods related the DiagramPersistence class.
    """
    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, diagram):

        from mosaicode.control.diagramcontrol import DiagramControl
        # load the diagram
        parser = XMLParser(diagram.file_name)

        zoom = parser.getTag(tag_name).getTag("zoom").getAttr("value")
        diagram.zoom = float(zoom)
        try:
            language = parser.getTag(tag_name).getTag(
                "language").getAttr("value")
            diagram.language = language
        except:
            pass

        # new version load
        blocks = parser.getTag(tag_name).getTag("blocks").getChildTags("block")
        system_blocks = System.get_blocks()
        for block in blocks:
            block_type = block.getAttr("type")
            if block_type not in system_blocks:
                continue
            block_id = int(block.getAttr("id"))
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
            new_block = deepcopy(system_blocks[block_type])
            new_block.set_properties(props)
            new_block.id = block_id
            new_block.x = float(x)
            new_block.y = float(y)
            DiagramControl.add_block(diagram, new_block)

        connections = parser.getTag(tag_name).getTag(
            "connections").getChildTags("connection")
        for conn in connections:
            try:
                from_block = diagram.blocks[int(conn.getAttr("from_block"))]
                to_block = diagram.blocks[int(conn.getAttr("to_block"))]
            except:
                continue
            from_block_out = int(conn.getAttr("from_out"))
            to_block_in = int(conn.getAttr("to_in"))
            connection = ConnectionModel(diagram, from_block, from_block.ports[from_block_out])
            connection.input = to_block
            connection.input_port = to_block.ports[to_block_in]
            diagram.connectors.append(connection)
        return True

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, diagram):
        """
        This method save a file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """

        parser = XMLParser()
        parser.addTag(tag_name)
        parser.appendToTag(tag_name, 'version', value=System.VERSION)
        parser.appendToTag(tag_name, 'zoom', value=diagram.zoom)
        parser.appendToTag(tag_name, 'language', value=diagram.language)

        parser.appendToTag(tag_name, 'blocks')
        for block_id in diagram.blocks:
            block_type = diagram.blocks[block_id].type
            pos = diagram.blocks[block_id].get_position()
            parser.appendToTag('blocks', 'block', type=block_type, id=block_id)
            parser.appendToLastTag('block', 'position', x=pos[0], y=pos[1])
            props = diagram.blocks[block_id].get_properties()
            for prop in props:
                parser.appendToLastTag('block',
                                       'property',
                                       key=str(prop["name"]),
                                       value=str(prop["value"])
                                       )

        parser.appendToTag(tag_name, 'connections')
        for connector in diagram.connectors:
            parser.appendToTag('connections', 'connection',
                               from_block=connector.output.id,
                               from_out=int(connector.output_port.index),
                               to_block=connector.input.id,
                               to_in=int(connector.input_port.index))

        try:
            save_file = open(str(diagram.file_name), "w")
            save_file.write(parser.prettify())
            save_file.close()
        except IOError as e:
            System.log(e.strerror)
            return False, e.strerror

        diagram.set_modified(False)
        return True, "Success"
# ------------------------------------------------------------------------------
