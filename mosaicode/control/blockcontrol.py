# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the BlockControl class.
"""
import ast
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
from os.path import expanduser
from mosaicode.utils.XMLUtils import XMLParser
from mosaicode.utils.PythonUtils import PythonParser
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
    def export_xml(cls):
        from mosaicode.system import System as System
        System()
        for block in System.blocks:
            print "Exporting block " + block
            BlockPersistence.save(System.blocks[block])

    # ----------------------------------------------------------------------
    @classmethod
    def export_python(cls):
        from mosaicode.system import System as System
        System()
        for block in System.blocks:
            print "Exporting block " + block
            BlockPersistence.save_python(System.blocks[block])

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        """
        This method loads the block from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        try:
            BlockPersistence.load(file_name)
        except:
            from mosaicode.system import System
            System.log("Block " + file_name + " could not load")
    # ----------------------------------------------------------------------
    @classmethod
    def add_new_block(cls, block):
        # first, save it
        BlockPersistence.save(block)
        # Then add it to system
        from mosaicode.system import System
        System.blocks[block.type] = block

    # ----------------------------------------------------------------------
    @classmethod
    def delete_block(cls, block):
        from mosaicode.system import System
        if block.source == "xml":
            data_dir = System.get_user_dir() + "/extensions/"
            file_name = data_dir + block.type + ".xml"
            os.remove(file_name)
            System.blocks.pop(block.type, None)
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
        print 'block.source =', block.source

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
