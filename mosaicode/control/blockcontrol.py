# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the BlockControl class.
"""
import ast
import copy
import inspect  # For module inspect
import os
import pkgutil  # For dynamic package load
from os.path import expanduser

from mosaicode.model.port import Port
from mosaicode.persistence.blockpersistence import BlockPersistence


class BlockControl():
    """
    This class contains methods related the BlockControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self):
        pass

    # ----------------------------------------------------------------------
    @classmethod
    def export(cls):
        from mosaicode.system import System as System
        System()
        blocks = System.get_blocks()
        result = True
        for key in blocks:
            path = System.get_user_dir()
            path = os.path.join(path,
                                'extensions',
                                blocks[key].language,
                                'blocks',
                                blocks[key].extension,
                                blocks[key].group)

            result = result and BlockPersistence.save(blocks[key], path)
        return result

    # ----------------------------------------------------------------------
    @classmethod
    def load_ports(cls, block, ports):
        # Adjust ports attributes
        i = 0
        in_port = 0
        out_port = 0
        new_ports = []
        for port in block.ports:
            # if it is not a dictionary, dunno what to do. What happened?
            if not isinstance(port, dict):
                System.log("Error Loading a Block: Port is not a dictionary?");
                continue
            if "type" not in port:
                System.log("Error Loading a Block: Port should have a type");
                continue
            port_type = port["type"]
            # Create a copy from the port instance loaded in the System
            if port_type not in ports:
                System.log("Error Loading a Block: Port is not present in System");
                continue
            new_port = copy.deepcopy(ports[port_type])

            if "conn_type" not in port:
                port["conn_type"] = Port.INPUT
            if port["conn_type"].upper() == "INPUT":
                new_port.conn_type = Port.INPUT
            else:
                new_port.conn_type = Port.OUTPUT

            new_port.index = i
            if new_port.is_input():
                new_port.type_index = in_port
                in_port += 1
            else:
                new_port.type_index = out_port
                out_port += 1
            new_port.name = port["name"]
            new_port.label = port["label"]
            new_ports.append(new_port)
            i += 1
        block.maxIO = max(in_port, out_port)
        block.ports = new_ports
    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        """
        This method loads the block from JSON file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        block = BlockPersistence.load(file_name)
        return block
    # ----------------------------------------------------------------------
    @classmethod
    def add_new_block(cls, block):
        # Save it
        from mosaicode.system import System
        System()
        path = System.get_user_dir() + "/extensions/"
        path = path + block.language + "/blocks/" + block.extension + "/"
        BlockPersistence.save(block, path)

    # ----------------------------------------------------------------------
    @classmethod
    def delete_block(cls, block):
        if block.file is not None:
            os.remove(block.file)
            return True
        else:
            return False

# ----------------------------------------------------------------------
