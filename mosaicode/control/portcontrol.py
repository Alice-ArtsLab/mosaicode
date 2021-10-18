# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PortControl class.
"""
import inspect  # For module inspect
import os
import pkgutil  # For dynamic package load
from os.path import expanduser

from mosaicode.model.port import Port
from mosaicode.persistence.portpersistence import PortPersistence
from mosaicode.utils.XMLUtils import XMLParser


class PortControl():
    """
    This class contains methods related the PortControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self):
        pass

    # ----------------------------------------------------------------------
    @classmethod
    def export(cls):
        from mosaicode.system import System as System
        System()
        ports = System.get_ports()
        result = True
        for key in ports:
            path = System.get_user_dir()
            path = os.path.join(path,
                                'extensions',
                                ports[key].language,
                                'ports')
            result = result and PortPersistence.save(ports[key], path)
        return result

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        """
        This method loads the port from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        return PortPersistence.load(file_name)

    # ----------------------------------------------------------------------
    @classmethod
    def add_port(cls, port):
        # first, save it
        from mosaicode.system import System as System
        System()
        path = System.get_user_dir() + "/extensions/"
        path = path + port.language + "/ports/"
        PortPersistence.save(port, path)

    # ----------------------------------------------------------------------
    @classmethod
    def delete_port(cls, port_key):
        from mosaicode.system import System
        ports = System.get_ports()
        if port_key not in ports:
            return False
        port = ports[port_key]
        if port.file is not None:
            os.remove(port.file)
            return True
        else:
            return False
# ----------------------------------------------------------------------
