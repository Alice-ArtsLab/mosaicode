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
            return
        parser = XMLParser(file_name)
        if parser.getTag("MosaicodePort") is None:
            return None

        port = Port()
        port.type = parser.getTagAttr("MosaicodePort", "type")
        port.language = parser.getTagAttr("MosaicodePort", "language")
        port.label = parser.getTagAttr("MosaicodePort", "label")
        port.color = parser.getTagAttr("MosaicodePort", "color")
        port.multiple = parser.getTagAttr("MosaicodePort", "multiple")
        port.source = parser.getTagAttr("MosaicodePort", "source")
        port.code = parser.getTag("MosaicodePort").getTag("code").getText()

        count = 0
        for code in port.input_codes:
            port.input_codes[count] = parser.getTag('MosaicodePort').getTag('input_code' + str(count)).getText()
            port.output_codes[count] = parser.getTag('MosaicodePort').getTag('output_code' + str(count)).getText()
            count = count + 1

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
        parser.addTag('MosaicodePort')

        parser.setTagAttr('MosaicodePort','type', port.type)
        parser.setTagAttr('MosaicodePort','language', port.language)
        parser.setTagAttr('MosaicodePort','label', port.label)
        parser.setTagAttr('MosaicodePort','color', port.color)
        parser.setTagAttr('MosaicodePort','multiple', port.multiple)
        parser.setTagAttr('MosaicodePort','source', port.source)
        parser.appendToTag('MosaicodePort','code').string = str(port.code)

        count = 0
        for code in port.input_codes:
            parser.appendToTag('MosaicodePort', 'input_code' + \
                        str(count)).string = str(port.input_codes[count])
            parser.appendToTag('MosaicodePort', 'output_code' + \
                        str(count)).string = str(port.output_codes[count])
            count = count + 1


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
        parser.setAttribute('input_codes', [])
        parser.setAttribute('output_codes', [])

        for index, code in enumerate(port.input_codes, start=0):
            parser.attributes['input_codes'].append(str(port.input_codes[index]))
            parser.attributes['output_codes'].append(str(port.output_codes[index]))

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
