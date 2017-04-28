# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PortControl class.
"""
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
from os.path import expanduser
from harpia.utils.XMLUtils import XMLParser
from harpia.utils.PythonUtils import PythonParser
from harpia.model.port import Port

class PortControl():
    """
    This class contains methods related the PortControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self):
        pass


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
        if parser.getTag("HarpiaPort") is None:
            return None

        port = Port()
        port.type = parser.getTagAttr("HarpiaPort", "type")
        port.language = parser.getTagAttr("HarpiaPort", "language")
        port.label = parser.getTagAttr("HarpiaPort", "label")
        port.color = parser.getTagAttr("HarpiaPort", "color")
        port.multiple = parser.getTagAttr("HarpiaPort", "multiple")
        port.source = parser.getTagAttr("HarpiaPort", "source")
        port.code = parser.getTag("HarpiaPort").getTag("code").getText()

        count = 0
        for code in port.input_codes:
            port.input_codes[count] = parser.getTag('HarpiaPort').getTag('input_code' + str(count)).getText()
            port.output_codes[count] = parser.getTag('HarpiaPort').getTag('output_code' + str(count)).getText()
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
        from harpia.system import System
        port.source = "xml"
        parser = XMLParser()
        parser.addTag('HarpiaPort')

        parser.setTagAttr('HarpiaPort','type', port.type)
        parser.setTagAttr('HarpiaPort','language', port.language)
        parser.setTagAttr('HarpiaPort','label', port.label)
        parser.setTagAttr('HarpiaPort','color', port.color)
        parser.setTagAttr('HarpiaPort','multiple', port.multiple)
        parser.setTagAttr('HarpiaPort','source', port.source)
        parser.appendToTag('HarpiaPort','code').string = str(port.code)

        count = 0
        for code in port.input_codes:
            parser.appendToTag('HarpiaPort', 'input_code' + \
                        str(count)).string = str(port.input_codes[count])
            parser.appendToTag('HarpiaPort', 'output_code' + \
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
        from harpia.system import System
        parser = PythonParser()

        parser.class_name = port.label
        parser.dependencies = [{'from':'harpia.model.port', 'import':'Port'}]
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
            file_name = data_dir + port.type + ".py"
            parser.save(file_name)
        except IOError as e:
            return False
        return True


    # ----------------------------------------------------------------------
    @classmethod
    def print_port(cls, port):
        """
        This method prints the port properties.
        """
        print 'Port.type =', port.type
        print 'Port.language =', port.language
        print 'Port.label =', port.label
        print 'Port.color =', port.color
        print 'Port.multiple =',  port.multiple
        print 'Port.source =', port.source
        print 'Port.code =', port.code
        print 'Port.input_codes =', port.input_codes
        print 'Port.output_codes =', port.output_codes
        print 'Port.var_name =', port.var_name

    # ----------------------------------------------------------------------
    @classmethod
    def add_port(cls, port):
        # first, save it
        PortControl.save(port)
        # Then add it to system
        from harpia.system import System
        System.ports[port.type] = port

    # ----------------------------------------------------------------------
    @classmethod
    def delete_port(cls, port_key):
        from harpia.system import System
        port = System.ports[port_key]
        if port.source == "xml":
            data_dir = System.get_user_dir() + "/extensions/"
            file_name = data_dir + port.type + ".xml"
            os.remove(file_name)
            System.ports.pop(port_key, None)
            return True
        else:
            return False
# ----------------------------------------------------------------------
