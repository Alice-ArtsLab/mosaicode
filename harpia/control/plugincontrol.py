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
from harpia.model.plugin import Plugin

class PluginControl():
    """
    This class contains methods related the PortControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self):
        pass

    # ----------------------------------------------------------------------
    @classmethod
    def load_plugins(cls, system):
        system.plugins.clear()
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
                if not isinstance(instance, Plugin):
                    continue
                if instance.get_label() == "":
                    continue
                system.plugins[instance.type] = obj

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
            plugin = PluginControl.load(home_dir + "/" + file)
            if plugin is None:
                continue
            plugin.source = "xml"
            system.plugins[plugin.get_type()] = plugin

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        """
        This method loads the plugin from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        # load the port
        if os.path.exists(file_name) is False:
            return
        xml_loader = XMLParser(file_name)
        properties = xml_loader.getTag("HarpiaPlugin").getChildTags("property")
        plugin = Plugin()
        for prop in properties:
            try:
                prop.getAttr("key")
            except:
                continue
            if prop.getAttr("key") in plugin.__dict__:
                plugin.__dict__[prop.getAttr("key")] = prop.getAttr("value")
        if plugin.get_type() == "harpia.model.plugin":
            return None
        return plugin

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, plugin):
        """
        This method save the plugin in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        from harpia.system import System
        plugin.source = "xml"
        parser = XMLParser()
        parser.addTag('HarpiaPlugin')
        for key in port.__dict__:
            parser.appendToTag('HarpiaPlugin', 'property',
                               key=key,
                               value=plugin.__dict__[key])
        try:
            file_name = System.get_user_dir() + "/" + plugin.get_type() + ".xml"
            plugin_file = file(os.path.expanduser(file_name), 'w')
            plugin_file.write(parser.prettify())
            plugin_file.close()
        except IOError as e:
            return False
        return True

    # ----------------------------------------------------------------------
    @classmethod
    def add_plugin(cls, plugin):
        # first, save it
        PluginControl.save(plugin)
        # Then add it to system
        from harpia.system import System
        System.plugins[plugin.get_type()] = plugin

    # ----------------------------------------------------------------------
    @classmethod
    def delete_plugin(cls, plugin_key):
        from harpia.system import System
        plugin = System.plugins[plugin_key]
        if plugin.source == "xml":
            file_name = System.get_user_dir() + "/" + plugin.get_type() + ".xml"
            os.remove(file_name)
            PluginControl.load_plugin(System)
            return True
        else:
            return False
# ----------------------------------------------------------------------
