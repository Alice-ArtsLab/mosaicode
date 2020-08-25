# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PortPersistence class.
"""
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
from os.path import join
from mosaicode.utils.XMLUtils import XMLParser
from mosaicode.model.port import Port
from mosaicode.persistence.persistence import Persistence

tag_name = "MosaicodePort"

class PortPersistence():
    """
    This class contains methods related the PortPersistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def load_xml(cls, file_name):
        """
        This method loads the port from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        # load the port
        if os.path.exists(file_name) is False:
            return None
        parser = XMLParser(file_name)
        if parser.getTag(tag_name) is None:
            return None

        port = Port()
        port.type = parser.getTagAttr(tag_name, "type")
        port.language = parser.getTagAttr(tag_name, "language")
        port.hint = parser.getTagAttr(tag_name, "hint")
        port.color = parser.getTagAttr(tag_name, "color")
        port.multiple = parser.getTagAttr(tag_name, "multiple")
        port.var_name = parser.getTagAttr(tag_name, "var_name")
        port.code = parser.getTag(tag_name).getTag("code").getText()

        if port.type == "":
            return None

        return port

    # ----------------------------------------------------------------------
    @classmethod
    def save_xml(cls, port, path):
        """
        This method save the port in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        port.source = "xml"
        parser = XMLParser()
        parser.addTag(tag_name)

        parser.setTagAttr(tag_name, 'type', port.type)
        parser.setTagAttr(tag_name, 'language', port.language)
        parser.setTagAttr(tag_name, 'hint', port.hint)
        parser.setTagAttr(tag_name, 'color', port.color)
        parser.setTagAttr(tag_name, 'multiple', port.multiple)
        parser.setTagAttr(tag_name, 'var_name', port.var_name)
        parser.appendToTag(tag_name, 'code').string = str(port.code)

        if not Persistence.create_dir(path):
            return False
        try:
            file_name = port.hint
            port_file = file(os.path.join(path, file_name + '.xml'), 'w')
            port_file.write(parser.prettify())
            port_file.close()
        except IOError as e:
            return False
        return True

# ----------------------------------------------------------------------
