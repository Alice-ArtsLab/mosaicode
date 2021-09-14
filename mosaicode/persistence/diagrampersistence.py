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
from datetime import datetime
from mosaicode.utils.XMLUtils import XMLParser
from mosaicode.system import System as System
from mosaicode.model.connectionmodel import ConnectionModel
from mosaicode.model.commentmodel import CommentModel
from mosaicode.model.authormodel import AuthorModel
from mosaicode.model.diagrammodel import DiagramModel

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
        if not isinstance(diagram, DiagramModel):
            return False
        from mosaicode.control.diagramcontrol import DiagramControl
        dc = DiagramControl(diagram)
        # load the diagram
        parser = XMLParser(diagram.file_name)

        # Loading from tags
        if parser.getTag(tag_name) is None:
            return False

        zoom = 1.0
        if parser.getTagAttr(tag_name, "zoom"):
            zoom = parser.getTagAttr(tag_name, "zoom")
        diagram.zoom = float(zoom)

        language = ""
        if parser.getTagAttr(tag_name, "language"):
            language = parser.getTagAttr(tag_name, "language")
        diagram.language = language

        code_template = parser.getTag(tag_name).getTag("code_template")
        if code_template is not None and hasattr(code_template, "value"):
            code_template = code_template.getAttr("value")
            if code_template not in System.get_code_templates():
                System.log("Code Template " + code_template + " not found")
            else:
                code_template = System.get_code_templates()[code_template]
                diagram.code_template = deepcopy(code_template)

        parser = parser.getTag(tag_name)
        # new version load
        blocks = parser.getTag("blocks").getChildTags("block")
        system_blocks = System.get_blocks()
        for block in blocks:
            block_type = block.getAttr("type")
            if block_type not in system_blocks:
                System.log("Block " + block_type + " not found")
                continue
            block_id = int(block.getAttr("id"))
            collapsed = False
            if hasattr(block, "collapsed"):
                collapsed = block.collapsed == "True"
            if hasattr(block, "x"):
                x = block.x
            if hasattr(block, "y"):
                y = block.y
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
            dc.add_block(new_block)

        connections = parser.getTag("connections")
        connections = connections.getChildTags("connection")
        for conn in connections:
            try:
                from_block = diagram.blocks[int(conn.from_block)]
                to_block = diagram.blocks[int(conn.to_block)]
                port_index = int(conn.getAttr("from_out"))
                if port_index >= 0 and port_index < len(from_block.ports):
                    from_block_out = from_block.ports[port_index]
                    if from_block_out.is_input():
                        System.log("Loading error: Output port is an input port")
                        continue
                else:
                    System.log("Loading error: invalid output port index " + str(port_index))
                    continue
                port_index = int(conn.getAttr("to_in"))
                if port_index >= 0 and port_index < len(to_block.ports):
                    to_block_in = to_block.ports[port_index]
                    if not to_block_in.is_input():
                        System.log("Loading error: Input port is an output port")
                        continue
                else:
                    System.log("Loading error: invalid input port index " + str(port_index))
                    continue
            except Exception as e:
                System.log("Loading error:" + str(e))
                continue
            connection = ConnectionModel(diagram,
                                from_block,
                                from_block_out,
                                to_block,
                                to_block_in)
            dc.add_connection(connection)

        comments = parser.getTag("comments")
        if comments is not None:
            comments = comments.getChildTags("comment")
            for com in comments:
                comment = CommentModel()
                comment.x = float(com.getAttr("x"))
                comment.y = float(com.getAttr("y"))
                properties = com.getChildTags("property")
                props = {}
                for prop in properties:
                    if hasattr(prop, 'key') and hasattr(prop, 'value'):
                        props[prop.key] = prop.value
                comment.set_properties(props)
                dc.add_comment(comment)

        authors = parser.getTag("authors")
        if authors is not None:
            authors = authors.getChildTags("author")
            for author in authors:
                auth = AuthorModel()
                auth.name = author.getAttr("author")
                auth.license = author.getAttr("license")
                auth.date = author.getAttr("date")
                diagram.authors.append(auth)

        diagram.redraw()
        
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
        parser.setTagAttr(tag_name,'version', value=System.VERSION)
        parser.setTagAttr(tag_name,'zoom', value=diagram.zoom)
        parser.setTagAttr(tag_name,'language', value=diagram.language)

        parser.appendToTag(tag_name, 'code_template', value=diagram.code_template)

        parser.appendToTag(tag_name, 'blocks')
        for block_id in diagram.blocks:
            block = diagram.blocks[block_id]
            pos = block.get_position()
            parser.appendToTag(
                    'blocks',
                    'block',
                    type=block.type,
                    id=block.id,
                    collapsed=block.is_collapsed,
                    x=pos[0],
                    y=pos[1]
                    )
            props = block.get_properties()
            for prop in props:
                if "name" in prop and "value" in prop:
                    parser.appendToLastTag(
                            'block',
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
                               x=pos[0],
                               y=pos[1])
            props = comment.get_properties()
            for prop in props:
                parser.appendToLastTag('comment',
                                       'property',
                                       key=str(prop["name"]),
                                       value=str(prop["value"])
                                       )

        auth = AuthorModel()
        auth.name = System.get_preferences().author
        auth.license = System.get_preferences().license
        auth.date = datetime.now()
        diagram.authors.insert(0,auth)

        parser.appendToTag(tag_name, 'authors')
        for author in diagram.authors:
            parser.appendToTag('authors', 'author',
                               author=author.name,
                               license=author.license,
                               date=author.date)

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
