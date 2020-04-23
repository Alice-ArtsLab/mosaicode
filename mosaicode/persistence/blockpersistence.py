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

from mosaicode.model.blockmodel import BlockModel
from mosaicode.persistence.persistence import Persistence
from mosaicode.utils.PythonUtils import PythonParser
from mosaicode.utils.XMLUtils import XMLParser

tag_name = "MosaicodeBlock"


class BlockPersistence():
    """
    This class contains methods related the BlockPersistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def load_xml(cls, file_name):
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
        block.extension = parser.getTagAttr(tag_name, "extension")

        block.help = parser.getTagAttr(tag_name, "help")
        block.color = parser.getTagAttr(tag_name, "color")
        block.label = parser.getTagAttr(tag_name, "label")
        block.group = parser.getTagAttr(tag_name, "group")
        block.maxOI = parser.getTagAttr(tag_name, "maxOI")

        block.codes = ast.literal_eval(parser.getTagAttr(tag_name, "codes"))

        props = parser.getTag(tag_name).getTag(
            "properties").getChildTags("property")
        for prop in props:
            block.properties.append(ast.literal_eval(prop.getAttr("value")))

        ports = parser.getTag(tag_name).getTag("ports").getChildTags("port")
        for port in ports:
            dict_port = {}
            dict_port["type"] = str(port.getAttr("type_"))
            dict_port["name"] = str(port.getAttr("name_"))
            dict_port["label"] = str(port.getAttr("label"))
            dict_port["conn_type"] = str(port.getAttr("conn_type"))
            block.ports.append(dict_port)

        block.file = parser.getTagAttr(tag_name, "file")

        if block.type == "mosaicode.model.blockmodel":
            return None
        return block

    # ----------------------------------------------------------------------
    @classmethod
    def save_xml(cls, block, path=None):
        """
        This method save the block in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """

        block.source = "xml"
        parser = XMLParser()
        main = parser.addTag(tag_name)
        parser.setTagAttr(tag_name, 'type', block.type)
        parser.setTagAttr(tag_name, 'language', block.language)
        parser.setTagAttr(tag_name, 'extension', block.extension)

        parser.setTagAttr(tag_name, 'help', block.help)
        parser.setTagAttr(tag_name, 'label', block.label)
        parser.setTagAttr(tag_name, 'color', block.color)
        parser.setTagAttr(tag_name, 'group', block.group)
        parser.setTagAttr(tag_name, 'maxIO', block.maxIO)

        parser.setTagAttr(tag_name, 'codes', block.codes)

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

        if (path is not None) and not Persistence.create_dir(path):
            return False

        if (path is None) and (block.file is not None):
            path = block.file
        elif (path is not None):
            file_name = block.label
            path = os.path.join(path, file_name + '.xml')
        else:
            return False

        parser.setTagAttr(tag_name, 'file', path)

        try:
            block_file = file(path, 'w')
            block_file.write(parser.getXML())
            block_file.close()
        except IOError as e:
            return False
        return True

# ----------------------------------------------------------------------
