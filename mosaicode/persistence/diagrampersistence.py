# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the DiagramPersistence class.
"""
import os
import gi
import json
from copy import deepcopy
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from datetime import datetime
from mosaicode.system import System as System
from mosaicode.model.connectionmodel import ConnectionModel
from mosaicode.model.commentmodel import CommentModel
from mosaicode.model.authormodel import AuthorModel
from mosaicode.model.diagrammodel import DiagramModel

class DiagramPersistence():
    """
    This class contains methods related the DiagramPersistence class.
    """
    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, diagram):
        """
        This method load the JSON file that represents the diagram.

            :param diagram: diagram to load.
            :return: operation status (True or False)
        """
        if os.path.exists(diagram.file_name) is False:
            System.log("Problem loading the diagram. File does not exist.")
            return None

        if not isinstance(diagram, DiagramModel):
            System.log("Problem loading the diagram. Is this a Diagram?")
            return False
        from mosaicode.control.diagramcontrol import DiagramControl
        dc = DiagramControl(diagram)
        # load the diagram

        data = ""

        try:
            data_file = open(diagram.file_name, 'r')
            data = json.load(data_file)
            data_file.close()

            if data["data"] != "DIAGRAM":
                System.log("Problem loading the diagram. Are you sure this is a valid file?")
                return False

            diagram.zoom = float(data["zoom"])
            diagram.language = data["language"]

            # Loading Code Template
            code_template_data = data["code_template"]
            code_template = code_template_data["type"]
            if code_template not in System.get_code_templates():
                System.log("Code Template " + code_template + " not found")
            else:
                code_template = System.get_code_templates()[code_template]
                diagram.code_template = deepcopy(code_template)
            properties = code_template_data["properties"]
            props = {}
            for prop in properties:
                props[prop["key"]] = prop["value"]
            diagram.code_template.set_properties(props)

            # Loading Blocks
            blocks = data["blocks"]
            system_blocks = System.get_blocks()
            for block in blocks:
                block_type = block["type"]
                if block_type not in system_blocks:
                    System.log("Block " + block_type + " not found")
                    continue
                block_id = int(block["id"])
                collapsed = block["collapsed"]
                x = block["x"]
                y = block["y"]
                properties = block["properties"]
                props = {}
                for prop in properties:
                    props[prop["key"]] = prop["value"]
                new_block = deepcopy(system_blocks[block_type])
                new_block.set_properties(props)
                new_block.id = block_id
                new_block.x = float(x)
                new_block.y = float(y)
                new_block.is_collapsed = collapsed
                dc.add_block(new_block)

            # Loading connections
            connections = data["connections"]
            for conn in connections:
                try:
                    from_block = diagram.blocks[int(conn["from_block"])]
                    to_block = diagram.blocks[int(conn["to_block"])]
                    port_index = int(conn["from_out"])
                    if port_index >= 0 and port_index < len(from_block.ports):
                        from_block_out = from_block.ports[port_index]
                        if from_block_out.is_input():
                            System.log("Diagram error: Output port is an input port")
                            continue
                    else:
                        System.log("Diagram error: invalid output port index " + str(port_index))
                        continue
                    port_index = int(conn["to_in"])
                    if port_index >= 0 and port_index < len(to_block.ports):
                        to_block_in = to_block.ports[port_index]
                        if not to_block_in.is_input():
                            System.log("Diagram error: Input port is an output port")
                            continue
                    else:
                        System.log("Diagram error: invalid input port index " + str(port_index))
                        continue
                except Exception as e:
                    System.log("Diagram error:" + str(e))
                    continue
                connection = ConnectionModel(diagram,
                                    from_block,
                                    from_block_out,
                                    to_block,
                                    to_block_in)
                dc.add_connection(connection)

            # Loading comments
            comments = data["comments"]
            for com in comments:
                comment = CommentModel()
                comment.x = float(com["x"])
                comment.y = float(com["y"])
                properties = com["properties"]
                props = {}
                for prop in properties:
                    props[prop["key"]] = prop["value"]
                comment.set_properties(props)
                dc.add_comment(comment)

            # Loading authors
            authors = data["authors"]
            for author in authors:
                auth = AuthorModel()
                auth.name = author["author"]
                auth.license = author["license"]
                auth.date = author["date"]
                diagram.authors.append(auth)

            diagram.redraw()


        except:
            return False

        return True

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, diagram):
        """
        This method save a file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """

        x = {
            "source": "JSON",
            "data": "DIAGRAM",
            "version": System.VERSION,
            "zoom": diagram.zoom,
            "language": diagram.language,
            "code_template": {},
            "blocks": [],
            "connections": [],
            "comments": [],
            "authors": []
        }

        code_template_data = {
            "type": diagram.code_template.type,
            "properties": []
            }
        props = diagram.code_template.properties
        for prop in props:
            code_template_data["properties"].append({
                    "key": str(prop["name"]),
                    "value": str(prop["value"])
                    })
        x["code_template"] = code_template_data

        for block_id in diagram.blocks:
            block = diagram.blocks[block_id]
            pos = block.get_position()
            block_data = {
                    "type": block.type,
                    "id": block.id,
                    "collapsed": block.is_collapsed,
                    "x": pos[0],
                    "y": pos[1],
                    "properties": []
                }
            props = block.get_properties()
            for prop in props:
                block_data["properties"].append({
                        "key": str(prop["name"]),
                        "value": str(prop["value"])
                        }
                        )
            x["blocks"].append(block_data)

        for connector in diagram.connectors:
            x["connections"].append({
                               "from_block": connector.output.id,
                               "from_out": int(connector.output_port.index),
                               "to_block": connector.input.id,
                               "to_in": int(connector.input_port.index)
                               })

        for comment in diagram.comments:
            pos = comment.get_position()
            comment_data = {
                               "x": pos[0],
                               "y": pos[1],
                               "properties": []
                               }
            props = comment.get_properties()
            for prop in props:
                comment_data["properties"].append({
                                       "key": str(prop["name"]),
                                       "value": str(prop["value"])
                                       })
            x["comments"].append(comment_data)

        auth = AuthorModel()
        auth.name = System.get_preferences().author
        auth.license = System.get_preferences().license
        auth.date = str(datetime.now())
        diagram.authors.insert(0,auth)

        for author in diagram.authors:
            x["authors"].append({
                               "author": author.name,
                               "license": author.license,
                               "date": author.date
                               })

        try:
            save_file = open(str(diagram.file_name), "w")
            save_file.write(json.dumps(x, indent=4))
            save_file.close()
        except IOError as e:
            System.log(e.strerror)
            return False, e.strerror

        diagram.set_modified(False)
        return True, "Success"
# ------------------------------------------------------------------------------
