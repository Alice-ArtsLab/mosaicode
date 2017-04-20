# -*- coding: utf-8 -*-
# [HARPIA PROJECT]
#
#
# S2i - Intelligent Industrial Systems
# DAS - Automation and Systems Department
# UFSC - Federal University of Santa Catarina
# Copyright: 2006 - 2007 Luis Carlos Dill Junges (lcdjunges@yahoo.com.br),
#                        Clovis Peruchi Scotti (scotti@ieee.org),
#                        Guilherme Augusto Rutzen (rutzen@das.ufsc.br),
#                        Mathias Erdtmann (erdtmann@gmail.com)
#                        and S2i (www.s2i.das.ufsc.br)
#            2007 - 2009 Clovis Peruchi Scotti (scotti@ieee.org),
#                        S2i (www.s2i.das.ufsc.br)
#
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License version 3, as published
#    by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranties of
#    MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#    PURPOSE.  See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    For further information, check the COPYING file distributed with this
#    software.
"""
This module contains the System class.
"""
import os
import sys
import copy
import inspect  # For module inspect
import pkgutil  # For dynamic package load
import harpia.plugins
from glob import glob  # To load examples
from harpia.control.preferencescontrol import PreferencesControl
from harpia.control.portcontrol import PortControl
from harpia.control.plugincontrol import PluginControl
from harpia.control.codetemplatecontrol import CodeTemplateControl
from harpia.model.preferences import Preferences
from harpia.model.codetemplate import CodeTemplate
from harpia.model.plugin import Plugin
from harpia.model.port import Port


class System(object):
    """
    This class contains methods related the System class.
    """

    APP = 'harpia'
    DATA_DIR = "/usr/share/harpia/"

    ZOOM_ORIGINAL = 1
    ZOOM_IN = 2
    ZOOM_OUT = 3

    VERSION = "0.0.1"
    # Instance variable to the singleton
    instance = None

    # ----------------------------------------------------------------------
    # An inner class instance to be singleton
    # ----------------------------------------------------------------------
    class __Singleton:
        # ----------------------------------------------------------------------

        def __init__(self):
            self.Log = None
            self.properties = Preferences()
            self.code_templates = {}
            self.plugins = {}
            self.list_of_examples = []
            self.ports = {}
            self.__load()

        # ----------------------------------------------------------------------
        def __load_xml(self, data_dir):
            if not os.path.exists(data_dir):
                return
            for file in os.listdir(data_dir):
                if not file.endswith(".xml"):
                    continue
                code_template = CodeTemplateControl.load(data_dir + "/" + file)
                if code_template is not None:
                    code_template.source = "xml"
                    self.code_templates[code_template.name] = code_template
                port = PortControl.load(data_dir + "/" + file)
                if port is not None:
                    port.source = "xml"
                    self.ports[port.type] = port
                plugin = PluginControl.load(data_dir + "/" + file)
                if plugin is not None:
                    plugin.source = "xml"
                    self.plugins[plugin.type] = plugin

        # ----------------------------------------------------------------------
        def __load(self):
            # Create user directory if does not exist
            if not os.path.isdir(System.get_user_dir() + "/extensions/"):
                try:
                    os.makedirs(System.get_user_dir() + "/extensions/")
                except:
                    pass
            # Load the preferences
            PreferencesControl(self.properties).load()
            # Load Examples
            examples = glob(System.DATA_DIR + "examples/*")
            for example in examples:
                self.list_of_examples.append(example)
            self.list_of_examples.sort()

            # Load CodeTemplates, Plugins and Ports
            self.code_templates.clear()
            self.ports.clear()
            self.plugins.clear()
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
                    if isinstance(instance, CodeTemplate):
                        self.code_templates[instance.name] = instance
                    if isinstance(instance, Port):
                        instance.source = "Python"
                        self.ports[instance.type] = instance
                    if isinstance(instance, Plugin):
                        if instance.label != "":
                            self.plugins[instance.type] = instance

            # Load XML files in application space
            self.__load_xml(System.get_user_dir() + "/extensions/")
            # Load XML files in user space
            self.__load_xml(System.DATA_DIR + "extensions/")

    # ----------------------------------------------------------------------
    def __init__(self):
        if not System.instance:
            System.instance = System.__Singleton()

    # ----------------------------------------------------------------------
    def __new__(cls):  # __new__ always a classmethod
        if System.instance is None:
            System.instance = System.__Singleton()
            # Add properties dynamically
            cls.properties = System.instance.properties
            cls.plugins = System.instance.plugins
            cls.list_of_examples = System.instance.list_of_examples
            cls.ports = System.instance.ports
            cls.code_templates = System.instance.code_templates

    # ----------------------------------------------------------------------
    @classmethod
    def set_log(cls, Logger):
        """
        This method set the log.
        """
        try:
            cls.instance.Log = Logger
        except:
            print "Could not set logger"

    # ----------------------------------------------------------------------
    @classmethod
    def log(cls, msg):
        "This metho show the log."
        try:
            cls.instance.Log.log(msg)
        except:
            print msg

    # ----------------------------------------------------------------------
    @classmethod
    def get_user_dir(cls):
        home_dir = os.path.expanduser("~")
        home_dir = home_dir + "/" + System.APP
        return home_dir

# ------------------------------------------------------------------------------
