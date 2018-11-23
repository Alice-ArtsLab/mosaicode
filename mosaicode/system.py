# -*- coding: utf-8 -*-
"""
This module contains the System class.
"""
import os
import sys
import time
import datetime
from copy import copy
import inspect  # For module inspect
import mosaicode.extensions
import pkgutil  # For dynamic package load
from glob import glob  # To load examples
from mosaicode.persistence.preferencespersistence import PreferencesPersistence
from mosaicode.control.portcontrol import PortControl
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.control.codetemplatecontrol import CodeTemplateControl
from mosaicode.model.preferences import Preferences
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.plugin import Plugin
from mosaicode.model.port import Port

class System(object):
    """
    This class contains methods related the System class.
    """

    APP = 'mosaicode'
    DATA_DIR = "/usr/share/mosaicode/"
    DATA_EXTENSIONS = "/usr/lib/python2.7/dist-packages/"

    ZOOM_ORIGINAL = 1
    ZOOM_IN = 2
    ZOOM_OUT = 3

    VERSION = "0.0.1"
    # Instance variable to the singleton
    instance = None

    sys.path.insert(0, DATA_EXTENSIONS)

    # ----------------------------------------------------------------------
    # An inner class instance to be singleton
    # ----------------------------------------------------------------------
    class __Singleton:
        # ----------------------------------------------------------------------

        def __init__(self):
            self.Log = None
            self.__code_templates = {}
            self.__blocks = {}
            self.__ports = {}

            self.list_of_examples = []
            self.plugins = []
            # Create user directory if does not exist
            directories = ["/extensions/", "/examples/", "/images/", "/diagrams/", "/code-gen/"]
            for name in directories:
                if not os.path.isdir(System.get_user_dir() + name):
                    try:
                        os.makedirs(System.get_user_dir() + name)
                    except Exception as error:
                        System.log(error)

            self.preferences = PreferencesPersistence.load(System.get_user_dir())

        # ----------------------------------------------------------------------
        def reload(self):
            self.__load_examples()
            self.__load_extensions_and_plugins()

        # ----------------------------------------------------------------------
        def get_blocks(self):
            return copy(self.__blocks)

        # ----------------------------------------------------------------------
        def remove_block(self, block):
            try:
                return self.__blocks.pop(block.type)
            except:
                return None

        # ----------------------------------------------------------------------
        def get_code_templates(self):
            return copy(self.__code_templates)

        # ----------------------------------------------------------------------
        def get_ports(self):
            return copy(self.__ports)

        # ----------------------------------------------------------------------
        def __load_examples(self):
            # Load Examples from the system
            self.list_of_examples = []
            for root, subdirs, files in os.walk(System.DATA_DIR + "extensions/"):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    if filename.endswith(".mscd"):
                        self.list_of_examples.append(file_path)
            # Load Examples from the user space
            for root, subdirs, files in os.walk(System.get_user_dir() + "/examples/"):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    if filename.endswith(".mscd"):
                        self.list_of_examples.append(file_path)
            self.list_of_examples.sort()

        # ----------------------------------------------------------------------
        def __load_xml(self, data_dir):
            if not os.path.exists(data_dir):
                return
            for file_name in os.listdir(data_dir):
                full_file_path = data_dir + "/" + file_name

                # Recursion to make it more interesting...
                if os.path.isdir(full_file_path):
                    self.__load_xml(full_file_path)

                if not file_name.endswith(".xml"):
                    continue

                code_template = CodeTemplateControl.load(full_file_path)
                if code_template is not None:
                    code_template.file = full_file_path
                    self.__code_templates[code_template.type] = code_template

                port = PortControl.load(full_file_path)

                if port is not None:
                    port.file = full_file_path
                    self.__ports[port.type] = port

                block = BlockControl.load(full_file_path)
                if block is not None:
                    block.file = full_file_path
                    self.__blocks[block.type] = block

        # ----------------------------------------------------------------------
        def __load_extensions_and_plugins(self):
            # Load CodeTemplates, Blocks and Ports
            self.__code_templates.clear()
            self.__ports.clear()
            self.__blocks.clear()
            # First load ports on python classes.
            # They are installed with mosaicode as root

            def walk_lib_packages(path=None, name_par=""):
                for importer, name, ispkg in pkgutil.iter_modules(path, name_par + "."):
                    if path is None and name.startswith("." + System.APP):
                        name = name.replace('.', '', 1)
                    if not name.startswith(System.APP+"_lib") and not name_par.startswith(System.APP+"_lib") and not name.startswith(System.APP+"_plugin") and not name_par.startswith(System.APP+"_plugin"):
                        continue

                    if ispkg:
                        if name_par is not "" and not name.startswith(System.APP):
                            name = name_par + "." + name
                        __import__(name)
                        path = getattr(sys.modules[name], '__path__', None) or []
                        walk_lib_packages(path, name)
                    else:
                        module = __import__(name, fromlist="dummy")
                        for class_name, obj in inspect.getmembers(module):
                            if not inspect.isclass(obj):
                                continue
                            modname = inspect.getmodule(obj).__name__
                            if not modname.startswith(System.APP+"_lib") and not modname.startswith(System.APP+"_plugin"):
                                continue
                            try:
                                instance = obj()
                            except:
                                continue
                            if isinstance(instance, Plugin):
                                if instance.label != "":
                                    self.plugins.append(instance)
                            if isinstance(instance, CodeTemplate):
                                self.__code_templates[instance.type] = instance
                            if isinstance(instance, Port):
                                self.__ports[instance.type] = instance
                            if isinstance(instance, BlockModel):
                                if instance.label != "":
                                    self.__blocks[instance.type] = instance

            walk_lib_packages(None, "")

            # Load XML files in application space
            self.__load_xml(System.DATA_DIR + "extensions")
            # Load XML files in user space
            self.__load_xml(System.get_user_dir() + "/extensions")

            for key in self.__blocks:
                try:
                    block = self.__blocks[key]
                    BlockControl.load_ports(block, self.__ports)
                except:
                    print("Error in loading plugin " + key)

    # ----------------------------------------------------------------------
    def __init__(self):
        if not System.instance:
            System.instance = System.__Singleton()

    # ----------------------------------------------------------------------
    def __new__(cls):  # __new__ always a classmethod
        if System.instance is None:
            System.instance = System.__Singleton()
            # Add properties dynamically
            cls.preferences = System.instance.preferences
            cls.plugins = System.instance.plugins

    # ----------------------------------------------------------------------
    @classmethod
    def get_list_of_examples(cls):
        """
        This method returns System installed blocks.
        """
        return System.instance.list_of_examples

    # ----------------------------------------------------------------------
    @classmethod
    def remove_block(cls, block):
        """
        This method removes a block installed in the System.
        """
        return cls.instance.remove_block(block)

    # ----------------------------------------------------------------------
    @classmethod
    def get_blocks(cls):
        """
        This method returns System installed blocks.
        """
        return cls.instance.get_blocks()

    # ----------------------------------------------------------------------
    @classmethod
    def get_code_templates(cls):
        """
        This method returns System installed code templates.
        """
        return cls.instance.get_code_templates()

    # ----------------------------------------------------------------------
    @classmethod
    def get_ports(cls):
        """
        This method returns System installed ports.
        """
        return cls.instance.get_ports()

    # ----------------------------------------------------------------------
    @classmethod
    def reload(cls):
        """
        This method reload System installed libs.
        """
        return cls.instance.reload()

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

    # ----------------------------------------------------------------------
    @classmethod
    def replace_wildcards(cls, text, diagram):
        """
        This method replace the wildcards.

        Returns:

            * **Types** (:class:`str<str>`)
        """
        result = text.replace("%t", str(time.time()))
        date = datetime.datetime.now().strftime("(%Y-%m-%d-%H:%M:%S)")
        result = result.replace("%d", date)
        result = result.replace("%l", diagram.language)
        result = result.replace("%n", diagram.patch_name)
        result = result.replace(" ", "_")
        return result

    # ----------------------------------------------------------------------
    @classmethod
    def get_dir_name(cls, diagram):
        """
        This method return the directory name.

        Returns:

            * **Types** (:class:`str<str>`)
        """
        name = System.preferences.default_directory
        name = System.replace_wildcards(name, diagram)
        if not name.endswith("/"):
            name = name + "/"
        return name

    # ----------------------------------------------------------------------
    @classmethod
    def get_filename(cls, diagram):
        """
        This method return the filename

        Returns:

            * **Types** (:class:`str<str>`)
        """
        name = System.preferences.default_filename
        name = System.replace_wildcards(name, diagram)
        return name

# ------------------------------------------------------------------------------
