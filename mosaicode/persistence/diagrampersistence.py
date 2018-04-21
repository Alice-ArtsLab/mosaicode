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
from mosaicode.model.commentmodel import CommentModel

tag_name = "mosaicode"

class DiagramPersistence():
    """
    This class contains methods related the DiagramPersistence class.
    """
    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, diagram):
        """
        This method load the xml file that represents the diagram.

            :param diagram: diagram to load.
            :return: operation status (True or False)
        """
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
            collapsed = False
            if hasattr(block, "collapsed"):
                collapsed = block.collapsed == "True"
            position = block.getTag("position")
            x = position.getAttr("x")
            y = position.getAttr("y")
            properties = block.getChildTags("property")
            props = {}
            for prop in properties:
                if hasattr(prop, 'key') and hasattr(prop, 'value'):
                    props[prop.key] = prop.value
            new_block = deepcopy(system_blocks[block_type])
            new_block.set_properties(props)
            new_block.id = block_id
            new_block.x = float(x)
            new_block.y = float(y)
            new_block.is_collapsed = collapsed
            DiagramControl.add_block(diagram, new_block)

        connections = parser.getTag(tag_name).getTag("connections").getChildTags("connection")
        for conn in connections:
            if not hasattr(conn, 'from_block'):
                continue
            elif not hasattr(conn, 'to_block'):
                continue
            from_block = diagram.blocks[int(conn.from_block)]
            from_block_out = int(conn.getAttr("from_out"))
            to_block_in = int(conn.getAttr("to_in"))
            to_block = diagram.blocks[int(conn.to_block)]
            connection = ConnectionModel(diagram, from_block,
                                from_block.ports[from_block_out],
                                to_block,
                                to_block.ports[to_block_in])
            DiagramControl.add_connection(diagram, connection)

        comments = parser.getTag(tag_name).getTag(
                    "comments").getChildTags("comment")
        for com in comments:
            comment = CommentModel()
            comment.x = float(com.getAttr("x"))
            comment.y = float(com.getAttr("y"))
            comment.text = com.getAttr("text")
            diagram.comments.append(comment)

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
            block = diagram.blocks[block_id]
            pos = block.get_position()
            parser.appendToTag('blocks', 'block',
                    type=block.type,
                    id=block.id,
                    collapsed=block.is_collapsed)
            parser.appendToLastTag('block', 'position', x=pos[0], y=pos[1])
            props = block.get_properties()
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

        parser.appendToTag(tag_name, 'comments')
        for comment in diagram.comments:
            pos = comment.get_position()
            parser.appendToTag('comments', 'comment',
                               text=comment.text,
                               x=pos[0],
                               y=pos[1])

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
