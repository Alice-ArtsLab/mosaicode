# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the BlockControl class.
"""
import ast
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
import copy
from os.path import expanduser
from mosaicode.utils.XMLUtils import XMLParser
from mosaicode.utils.PythonUtils import PythonParser
from mosaicode.persistence.blockpersistence import BlockPersistence
from mosaicode.model.port import Port


class BlockControl():
    """
    This class contains methods related the BlockControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self):
        pass

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
                continue
            if "type" not in port:
                continue
            port_type = port["type"]
            # Create a copy from the port instance loaded in the System
            if port_type not in ports:
                continue
            new_port = copy.deepcopy(ports[port_type])

            if "conn_type" not in port:
                port["conn_type"] = Port.INPUT
            if port["conn_type"].upper() == "INPUT":
                new_port.conn_type = Port.INPUT
            else:
                new_port.conn_type = Port.OUTPUT

            new_port.index = i
            i += 1
            if new_port.is_input():
                new_port.type_index = in_port
                in_port += 1
            else:
                new_port.type_index = out_port
                out_port += 1
            new_port.name = port["name"]
            new_port.label = port["label"]
            new_ports.append(new_port)
        block.maxIO = max(in_port, out_port)
        block.ports = new_ports

    # ----------------------------------------------------------------------
    @classmethod
    def export_xml(cls):
        from mosaicode.system import System as System
        System()
        blocks = System.get_blocks()
        for block in blocks:
            path = System.get_user_dir() + "/extensions/"
            path = path + block.language + "/" + block.framework + "/"
            BlockPersistence.save_xml(blocks[block], path)

    # ----------------------------------------------------------------------
    @classmethod
    def export_python(cls):
        from mosaicode.system import System
        System()
        blocks = System.get_blocks()
        for block in blocks:
            path = System.get_user_dir() + "/extensions/"
            path = path + block.language + "/" + block.framework + "/"
            BlockPersistence.save_python(blocks[block], path)

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        """
        This method loads the block from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        file_name = file_name.replace(" ", "\\ ")
        try:
            return BlockPersistence.load_xml(file_name)
        except:
            from mosaicode.system import System
            System.log("Block " + file_name + " could not load")
    # ----------------------------------------------------------------------

    @classmethod
    def add_new_block(cls, block):
        # Save it
        from mosaicode.system import System
        System()
        path = System.get_user_dir() + "/extensions/"
        path = path + block.language + "/" + block.framework + "/"
        BlockPersistence.save_xml(block, path)

    # ----------------------------------------------------------------------
    @classmethod
    def delete_block(cls, block):
        if block.file is not None:
            os.remove(block.file)
            return True
        else:
            return False

    # ----------------------------------------------------------------------
    @classmethod
    def print_block(cls, block):
        """
        This method prints the block properties.
        """
        print 'block.id =', block.id
        print 'block.x =', block.x
        print 'block.y =', block.y

        print 'block.type =', block.type
        print 'block.language =', block.language
        print 'block.framework =', block.framework
        print 'block.file =', block.file

        # Appearance
        print 'block.help =', block.help
        print 'block.label =', block.label
        print 'block.color =', block.color
        print 'block.group =', block.group
        print 'block.ports =', block.ports

        # Code generation
        print 'block.properties =', block.properties
        print 'block.codes =', block.codes
# ----------------------------------------------------------------------
