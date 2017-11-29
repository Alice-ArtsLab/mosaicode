# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PortPersistence class.
"""
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
from os.path import expanduser
from mosaicode.utils.XMLUtils import XMLParser
from mosaicode.utils.PythonUtils import PythonParser
from mosaicode.model.port import Port

tag_name = "MosaicodePort"

class PortPersistence():
    """
    This class contains methods related the PortPersistence class.
    """

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
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
        port.label = parser.getTagAttr(tag_name, "label")
        port.color = parser.getTagAttr(tag_name, "color")
        port.multiple = parser.getTagAttr(tag_name, "multiple")
        port.source = parser.getTagAttr(tag_name, "source")
        port.code = parser.getTag(tag_name).getTag("code").getText()

        if port.type == "":
            return None
        
        return port

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, port):
        """
        This method save the port in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        from mosaicode.system import System
        port.source = "xml"
        parser = XMLParser()
        parser.addTag(tag_name)

        parser.setTagAttr(tag_name, 'type', port.type)
        parser.setTagAttr(tag_name, 'language', port.language)
        parser.setTagAttr(tag_name, 'label', port.label)
        parser.setTagAttr(tag_name, 'color', port.color)
        parser.setTagAttr(tag_name, 'multiple', port.multiple)
        parser.setTagAttr(tag_name, 'source', port.source)
        parser.appendToTag(tag_name, 'code').string = str(port.code)

        try:
            data_dir = System.get_user_dir() + "/extensions/"
            data_dir = data_dir + port.language + "/ports/"
            if not os.path.isdir(data_dir):
                try:
                    os.makedirs(data_dir)
                except:
                    pass
            file_name = data_dir + port.type + ".xml"
            port_file = file(os.path.expanduser(file_name), 'w')
            port_file.write(parser.prettify())
            port_file.close()
        except IOError as e:
            return False
        return True

    # ----------------------------------------------------------------------
    @classmethod
    def save_python(cls, port):
        """
        This method save the port in user space in python extension.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        from mosaicode.system import System
        parser = PythonParser()
        parser.class_name = port.label.replace(' ', '')
        parser.dependencies = [{'from':'mosaicode.model.port', 'import':'Port'}]
        parser.inherited_classes = ['Port']
        parser.setAttribute('type', port.type)
        parser.setAttribute('language', port.language)
        parser.setAttribute('label', port.label)
        parser.setAttribute('color', port.color)
        parser.setAttribute('multiple', port.multiple)
        parser.setAttribute('source', 'python')
        parser.setAttribute('code', str(port.code))

        try:
            data_dir = System.get_user_dir() + "/extensions/"
            data_dir = data_dir + port.language + "/ports/"
            if not os.path.isdir(data_dir):
                try:
                    os.makedirs(data_dir)
                except:
                    pass
            file_name = data_dir + port.label.lower().replace(' ', '_') + ".py"
            parser.save(file_name)
        except IOError as e:
            return False
        return True
# ----------------------------------------------------------------------
