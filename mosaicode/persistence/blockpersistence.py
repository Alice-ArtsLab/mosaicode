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
            return None
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

        for code in block.codes:
            block.codes[code] = parser.getTag(tag_name).getTag(code).getText()

        props = parser.getTag(tag_name).getTag(
                    "properties").getChildTags("property")
        for prop in props:
            block.properties.append(ast.literal_eval(prop.getAttr("value")))

        ports = parser.getTag(tag_name).getTag("ports").getChildTags("port")
        for port in ports:
            dict_port = {}
            dict_port["type"]= str(port.getAttr("type_"))
            dict_port["name"]= str(port.getAttr("name_"))
            dict_port["label"]= str(port.getAttr("label"))
            dict_port["conn_type"]= str(port.getAttr("conn_type"))
            block.ports.append(dict_port)

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

        for code in block.codes:
            parser.appendToTag(tag_name, code, value=block.codes[code])

        parser.appendToTag(tag_name, 'properties')
        for key in block.properties:
            parser.appendToTag('properties', 'property', value=key)

        parser.appendToTag(tag_name, 'ports')
        for port in block.ports:
            parser.appendToTag('ports', 'port',
                conn_type=port.conn_type,
                name_=port.name,
                label=port.label,
                type_=port.type)

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
        parser.setAttribute('help', block.help)
        parser.setAttribute('label', block.label)
        parser.setAttribute('color', block.color)
        parser.setAttribute('group', block.group)
        parser.setAttribute('help', block.help)
        parser.setAttribute('ports', block.ports)
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
