# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the BlockPersistence class.
"""
import ast
import inspect  # For module inspect
import os
import pkgutil  # For dynamic package load
from os.path import join
import json
from mosaicode.model.blockmodel import BlockModel
from mosaicode.persistence.persistence import Persistence

class BlockPersistence():
    """
    This class contains methods related the BlockPersistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        """
        This method loads the block from JSON file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        if os.path.exists(file_name) is False:
            return None

        data = ""
        block = BlockModel()

        try:
            data_file = open(file_name, 'r')
            data = json.load(data_file)
            data_file.close()

            if data["data"] != "BLOCK":
                return None

            block.type = data["type"]
            block.language = data["language"]
            block.extension = data["extension"]
            block.help = data["help"]
            block.color = data["color"]
            block.label = data["label"]
            block.group = data["group"]

            codes = data["codes"]
            if codes:
                for code in codes:
                    block.codes[code["name"]] = code["code"]

            props = data["properties"]
            for prop in props:
                block.properties.append(prop)

            ports = data["ports"]
            for port in ports:
                block.ports.append(port)

            block.file = file_name

        except:
            return None


        if block.type == "mosaicode.model.blockmodel":
            return None
        return block

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, block, path=None):
        """
        This method save the block in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """

        x = {
            "source": "JSON",
            "data": "BLOCK",
            "version": block.version,
            "type": block.type,
            "language": block.language,
            "extension": block.extension,
            "help": block.help,
            "label": block.label,
            "color": block.color,
            "group": block.group,
            "codes": [],
            "properties":[],
            "ports":[]
        }
        
        for key in block.codes:
            x["codes"].append({
                "name":key,
                "code": block.codes[key]
                })

        for key in block.properties:
            x["properties"].append(key)

        for port in block.ports:
            x["ports"].append({
                        "conn_type": port.conn_type,
                        "name": port.name,
                        "label": port.label,
                        "type":port.type
                        }
                        )

        if (path is not None) and not Persistence.create_dir(path):
            from mosaicode.system import System as System
            System.log("Problem saving Blocks")
            return False

        if (path is None) and (block.file is not None):
            path = block.file
        elif (path is not None):
            file_name = block.label
            path = os.path.join(path, file_name + '.json')
        else:
            from mosaicode.system import System as System
            System.log("Problem saving Blocks")
            return False

        try:
            data_file = open(path, 'w')
            data_file.write(json.dumps(x, indent=4))
            data_file.close()
        except IOError as e:
            from mosaicode.system import System as System
            System.log("Problem saving Blocks")
            return False
        return True
# ----------------------------------------------------------------------
