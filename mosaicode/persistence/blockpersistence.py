# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the BlockPersistence class.
"""
import ast
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
from os.path import expanduser
from mosaicode.utils.XMLUtils import XMLParser
from mosaicode.utils.PythonUtils import PythonParser
from mosaicode.model.plugin import Plugin

class BlockPersistence():
    """
    This class contains methods related the BlockPersistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        """
        This method loads the block from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        if os.path.exists(file_name) is False:
            return
        parser = XMLParser(file_name)

        if parser.getTag("MosaicodePlugin") is None:
            return None

        plugin = Plugin()

        plugin.type = parser.getTagAttr("MosaicodePlugin", "type")
        plugin.language = parser.getTagAttr("MosaicodePlugin", "language")
        plugin.framework = parser.getTagAttr("MosaicodePlugin", "framework")

        plugin.label = parser.getTagAttr("MosaicodePlugin", "label")
        plugin.group = parser.getTagAttr("MosaicodePlugin", "group")
        plugin.color = parser.getTagAttr("MosaicodePlugin", "color")
        plugin.help = parser.getTagAttr("MosaicodePlugin", "help")
        plugin.source = parser.getTagAttr("MosaicodePlugin", "source")

        count = 0
        for code in plugin.codes:
            plugin.codes[count] = parser.getTag("MosaicodePlugin").getTag("code" + str(count)).getText()
            count = count + 1

        props = parser.getTag("MosaicodePlugin").getTag(
                    "properties").getChildTags("property")
        for prop in props:
            plugin.properties.append(ast.literal_eval(prop.getAttr("value")))

        in_ports = parser.getTag("MosaicodePlugin").getTag(
                    "in_ports").getChildTags("port")
        for port in in_ports:
            plugin.in_ports.append(ast.literal_eval(port.getAttr("value")))

        out_ports = parser.getTag("MosaicodePlugin").getTag(
                    "out_ports").getChildTags("port")
        for port in out_ports:
            plugin.out_ports.append(ast.literal_eval(port.getAttr("value")))

        if plugin.type == "mosaicode.model.plugin":
            return None
        return plugin

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, plugin):
        """
        This method save the plugin in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        from mosaicode.system import System
        plugin.source = "xml"
        parser = XMLParser()
        main = parser.addTag('MosaicodePlugin')
        parser.setTagAttr('MosaicodePlugin','type', plugin.type)
        parser.setTagAttr('MosaicodePlugin','language', plugin.language)
        parser.setTagAttr('MosaicodePlugin','framework', plugin.framework)

        parser.setTagAttr('MosaicodePlugin','label', plugin.label)
        parser.setTagAttr('MosaicodePlugin','group', plugin.group)
        parser.setTagAttr('MosaicodePlugin','color', plugin.color)
        parser.setTagAttr('MosaicodePlugin','help', plugin.help)
        parser.setTagAttr('MosaicodePlugin','source', plugin.source)

        count = 0
        for code in plugin.codes:
            parser.appendToTag('MosaicodePlugin', 'code' + str(count)).string = str(plugin.codes[count])
            count = count + 1

        parser.appendToTag('MosaicodePlugin', 'properties')
        for key in plugin.properties:
            parser.appendToTag('properties', 'property', value=key)

        parser.appendToTag('MosaicodePlugin', 'in_ports')
        for key in plugin.in_ports:
            parser.appendToTag('in_ports', 'port', value=key)

        parser.appendToTag('MosaicodePlugin', 'out_ports')
        for key in plugin.out_ports:
            parser.appendToTag('out_ports', 'port', value=key)

        try:
            data_dir = System.get_user_dir() + "/extensions/"
            data_dir = data_dir + plugin.language + "/" + plugin.framework + "/"
            if not os.path.isdir(data_dir):
                try:
                    os.makedirs(data_dir)
                except:
                    pass
            file_name = data_dir + plugin.type + ".xml"
            plugin_file = file(os.path.expanduser(file_name), 'w')
            plugin_file.write(parser.getXML())
            plugin_file.close()
        except IOError as e:
            return False
        return True
    # ----------------------------------------------------------------------
    @classmethod
    def save_python(cls, plugin):
        """
        This method save the port in user space in python extension.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        from mosaicode.system import System
        parser = PythonParser()

        parser.class_name = plugin.label.replace(' ', '')
        parser.dependencies = [{'from':'mosaicode.model.plugin', 'import':'Plugin'}]
        parser.inherited_classes = ['Plugin']
        parser.setAttribute('id', plugin.id)
        parser.setAttribute('type', plugin.type)
        parser.setAttribute('language', plugin.language)
        parser.setAttribute('framework', 'python')
        parser.setAttribute('source', plugin.source)
        parser.setAttribute('help', plugin.help)
        parser.setAttribute('label', plugin.label)
        parser.setAttribute('color', plugin.color)
        parser.setAttribute('group', plugin.group)
        parser.setAttribute('help', plugin.help)
        parser.setAttribute('in_ports', plugin.in_ports)
        parser.setAttribute('out_ports', plugin.out_ports)
        parser.setAttribute('properties', plugin.properties)
        parser.setAttribute('codes', plugin.codes)

        try:
            data_dir = System.get_user_dir() + "/extensions/"
            data_dir = data_dir + plugin.language + "/" + plugin.framework + "/"
            if not os.path.isdir(data_dir):
                try:
                    os.makedirs(data_dir)
                except:
                    pass
            file_name = data_dir + plugin.label.lower().replace(' ', '_') + ".py"
            parser.save(file_name)
        except IOError as e:
            return False
        return True
# ----------------------------------------------------------------------
