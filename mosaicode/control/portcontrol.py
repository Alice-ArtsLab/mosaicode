# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PortControl class.
"""
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
from os.path import expanduser
from mosaicode.utils.XMLUtils import XMLParser
from mosaicode.utils.PythonUtils import PythonParser
from mosaicode.model.port import Port
from mosaicode.persistence.portpersistence import PortPersistence


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
        return PortPersistence.load_xml(file_name)

    # ----------------------------------------------------------------------
    @classmethod
    def export_xml(cls):
        from mosaicode.system import System as System
        System()
        ports = System.get_ports()
        for port in ports:
            path = System.get_user_dir() + "/extensions/"
            path = path + port.language + "/ports/"
            PortPersistence.save_xml(ports[port], path)

    # ----------------------------------------------------------------------
    @classmethod
    def export_python(cls):
        from mosaicode.system import System as System
        System()
        ports = System.get_ports()
        for port in ports:
            path = System.get_user_dir() + "/extensions/"
            path = path + port.language + "/ports/"
            PortPersistence.save_python(ports[port])

    # ----------------------------------------------------------------------
    @classmethod
    def print_port(cls, port):
        """
        This method prints the port properties.
        """
        print 'Port.type =', port.type
        print 'Port.language =', port.language
        print 'Port.hint =', port.hint
        print 'Port.color =', port.color
        print 'Port.multiple =',  port.multiple
        print 'Port.file =', port.file
        print 'Port.code =', port.code
        print 'Port.var_name =', port.var_name

    # ----------------------------------------------------------------------
    @classmethod
    def add_port(cls, port):
        # first, save it
        from mosaicode.system import System as System
        System()
        path = System.get_user_dir() + "/extensions/"
        path = path + port.language + "/ports/"
        PortPersistence.save_xml(port, path)

    # ----------------------------------------------------------------------
    @classmethod
    def delete_port(cls, port_key):
        from mosaicode.system import System
        ports = System.get_ports()
        port = ports[port_key]
        if port.file is not None:
            os.remove(port.file)
            return True
        else:
            return False
# ----------------------------------------------------------------------
