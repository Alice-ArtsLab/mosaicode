# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PortControl class.
"""
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
import harpia.plugins
from os.path import expanduser
from harpia.utils.XMLUtils import XMLParser
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
    def load_ports(cls, system):
        system.ports.clear()
        # First load ports on python classes.
        # They are installed with harpia as root 
        for importer, modname, ispkg in pkgutil.walk_packages(
                harpia.plugins.__path__,
                harpia.plugins.__name__ + ".",
                None):
            if ispkg:
                continue
            module = __import__(modname, fromlist="dummy")
            for name, obj in inspect.getmembers(module):
                if not inspect.isclass(obj):
                    continue
                modname = inspect.getmodule(obj).__name__
                if not modname.startswith("harpia.plugins"):
                    continue
                instance = obj()
                if not isinstance(instance, Port):
                    continue
                instance.source = "Python"
                system.ports[instance.get_type()] = instance

        #Now load the XML from user space
        from harpia.system import System
        home_dir = System.get_user_dir()
        if not os.path.isdir(home_dir):
            return
        if not os.path.exists(home_dir):
            return
        for file in os.listdir(home_dir):
            if not file.endswith(".xml"):
                continue
            port = PortControl.load(home_dir + "/" + file)
            if port is None:
                continue
            port.source = "xml"
            system.ports[port.get_type()] = port

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
        xml_loader = XMLParser(file_name)
        properties = xml_loader.getTag(
                "HarpiaPort").getChildTags("property")
        port = Port()
        for prop in properties:
            try:
                prop.getAttr("key")
            except:
                continue
            if prop.getAttr("key") in port.__dict__:
                port.__dict__[prop.getAttr("key")] = prop.getAttr("value")
        if port.get_type() == "":
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
        for key in port.__dict__:
            parser.appendToTag('HarpiaPort', 'property',
                               key=key, value=port.__dict__[key])
        try:
            file_name = System.get_user_dir() + "/" + port.get_type() + ".xml"
            port_file = file(os.path.expanduser(file_name), 'w')
            port_file.write(parser.prettify())
            port_file.close()
        except IOError as e:
            return False
        return True

    # ----------------------------------------------------------------------
    @classmethod
    def add_port(cls, port):
        # first, save it
        PortControl.save(port)
        # Then add it to system
        from harpia.system import System
        System.ports[port.get_type()] = port

    # ----------------------------------------------------------------------
    @classmethod
    def delete_port(cls, port_key):
        from harpia.system import System
        port = System.ports[port_key]
        if port.source == "xml":
            file_name = System.get_user_dir() + "/" + port.get_type() + ".xml"
            os.remove(file_name)
            PortControl.load_ports(System)
            return True
        else:
            return False
# ----------------------------------------------------------------------
