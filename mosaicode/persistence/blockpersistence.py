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
from mosaicode.model.blockmodel import BlockModel

tag_name = "MosaicodeBlock"

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

        if parser.getTag(tag_name) is None:
            return None

        block = BlockModel()

        block.type = parser.getTagAttr(tag_name, "type")
        block.language = parser.getTagAttr(tag_name, "language")
        block.framework = parser.getTagAttr(tag_name, "framework")

        block.label = parser.getTagAttr(tag_name, "label")
        block.group = parser.getTagAttr(tag_name, "group")
        block.color = parser.getTagAttr(tag_name, "color")
        block.help = parser.getTagAttr(tag_name, "help")
        block.source = parser.getTagAttr(tag_name, "source")

        for code in block.codes:
            block.codes[code] = parser.getTag(tag_name).getTag(code).getText()

        props = parser.getTag(tag_name).getTag(
                    "properties").getChildTags("property")
        for prop in props:
            block.properties.append(ast.literal_eval(prop.getAttr("value")))

        in_ports = parser.getTag(tag_name).getTag(
                    "in_ports").getChildTags("port")
        for port in in_ports:
            block.in_ports.append(ast.literal_eval(port.getAttr("value")))

        out_ports = parser.getTag(tag_name).getTag(
                    "out_ports").getChildTags("port")
        for port in out_ports:
            block.out_ports.append(ast.literal_eval(port.getAttr("value")))

        if block.type == "mosaicode.model.blockmodel":
            return None
        return block

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, block):
        """
        This method save the block in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        from mosaicode.system import System
        block.source = "xml"
        parser = XMLParser()
        main = parser.addTag(tag_name)
        parser.setTagAttr(tag_name,'type', block.type)
        parser.setTagAttr(tag_name,'language', block.language)
        parser.setTagAttr(tag_name,'framework', block.framework)

        parser.setTagAttr(tag_name,'label', block.label)
        parser.setTagAttr(tag_name,'group', block.group)
        parser.setTagAttr(tag_name,'color', block.color)
        parser.setTagAttr(tag_name,'help', block.help)
        parser.setTagAttr(tag_name,'source', block.source)

        for code in block.codes:
            parser.appendToTag(tag_name, code = block.codes[code])

        parser.appendToTag(tag_name, 'properties')
        for key in block.properties:
            parser.appendToTag('properties', 'property', value=key)

        parser.appendToTag(tag_name, 'in_ports')
        for key in block.in_ports:
            parser.appendToTag('in_ports', 'port', value=key)

        parser.appendToTag(tag_name, 'out_ports')
        for key in block.out_ports:
            parser.appendToTag('out_ports', 'port', value=key)

        try:
            data_dir = System.get_user_dir() + "/extensions/"
            data_dir = data_dir + block.language + "/" + block.framework + "/"
            if not os.path.isdir(data_dir):
                try:
                    os.makedirs(data_dir)
                except:
                    pass
            file_name = data_dir + block.type + ".xml"
            block_file = file(os.path.expanduser(file_name), 'w')
            block_file.write(parser.getXML())
            block_file.close()
        except IOError as e:
            return False
        return True
    # ----------------------------------------------------------------------
    @classmethod
    def save_python(cls, block):
        """
        This method save the port in user space in python extension.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        from mosaicode.system import System
        parser = PythonParser()

        parser.class_name = block.label.replace(' ', '')
        parser.dependencies = [{'from':'mosaicode.model.blockmodel', 'import':'BlockModel'}]
        parser.inherited_classes = ['BlockModel']
        parser.setAttribute('id', block.id)
        parser.setAttribute('type', block.type)
        parser.setAttribute('language', block.language)
        parser.setAttribute('framework', 'python')
        parser.setAttribute('source', block.source)
        parser.setAttribute('help', block.help)
        parser.setAttribute('label', block.label)
        parser.setAttribute('color', block.color)
        parser.setAttribute('group', block.group)
        parser.setAttribute('help', block.help)
        parser.setAttribute('in_ports', block.in_ports)
        parser.setAttribute('out_ports', block.out_ports)
        parser.setAttribute('properties', block.properties)
        parser.setAttribute('codes', block.codes)

        try:
            data_dir = System.get_user_dir() + "/extensions/"
            data_dir = data_dir + block.language + "/" + block.framework + "/"
            if not os.path.isdir(data_dir):
                try:
                    os.makedirs(data_dir)
                except:
                    pass
            file_name = data_dir + block.label.lower().replace(' ', '_') + ".py"
            parser.save(file_name)
        except IOError as e:
            return False
        return True
# ----------------------------------------------------------------------
