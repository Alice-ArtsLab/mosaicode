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
from harpia.utils.XMLUtils import XMLParser
from harpia.utils.PythonUtils import PythonParser
from harpia.model.plugin import Plugin
from harpia.persistence.blockpersistence import BlockPersistence

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
        from harpia.system import System as System
        System()
        for plugin in System.plugins:
            print "Exporting plugin " + plugin
            BlockPersistence.save(System.plugins[plugin])

    # ----------------------------------------------------------------------
    @classmethod
    def export_python(cls):
        from harpia.system import System as System
        System()
        for plugin in System.plugins:
            print "Exporting plugin " + plugin
            BlockPersistence.save_python(System.plugins[plugin])

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        """
        This method loads the block from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        BlockPersistence.load(file_name)
    # ----------------------------------------------------------------------
    @classmethod
    def add_plugin(cls, plugin):
        # first, save it
        BlockPersistence.save(plugin)
        # Then add it to system
        from harpia.system import System
        System.plugins[plugin.type] = plugin

    # ----------------------------------------------------------------------
    @classmethod
    def delete_plugin(cls, plugin):
        from harpia.system import System
        if plugin.source == "xml":
            data_dir = System.get_user_dir() + "/extensions/"
            file_name = data_dir + plugin.type + ".xml"
            os.remove(file_name)
            System.plugins.pop(plugin.type, None)
            return True
        else:
            return False

    # ----------------------------------------------------------------------
    @classmethod
    def print_plugin(cls, plugin):
        """
        This method prints the plugin properties.
        """
        print 'Plugin.id =', plugin.id
        print 'Plugin.x =', plugin.x
        print 'Plugin.y =', plugin.y

        print 'Plugin.type =', plugin.type
        print 'Plugin.language =', plugin.language
        print 'Plugin.framework =', plugin.framework
        print 'Plugin.source =', plugin.source

        # Appearance
        print 'Plugin.help =', plugin.help
        print 'Plugin.label =', plugin.label
        print 'Plugin.color =', plugin.color
        print 'Plugin.group =', plugin.group
        print 'Plugin.in_ports =', plugin.in_ports
        print 'Plugin.out_ports =', plugin.out_ports

        # Code generation
        print 'Plugin.properties =', plugin.properties
        print 'Plugin.codes =', plugin.codes
# ----------------------------------------------------------------------
