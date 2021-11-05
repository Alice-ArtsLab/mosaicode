# -*- coding: utf-8 -*-
"""
This module contains the System class.
"""
import datetime
import inspect  # For module inspect
import os
import pkgutil  # For dynamic package load
import sys
import time
from copy import copy
import mosaicode.extensions
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.control.codetemplatecontrol import CodeTemplateControl
from mosaicode.control.portcontrol import PortControl
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.model.port import Port
from mosaicode.model.preferences import Preferences
from mosaicode.persistence.preferencespersistence import PreferencesPersistence


class System(object):
    """
    This class contains methods related the System class.
    """

    APP = 'mosaicode'
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
            self.__code_templates = {}
            self.__blocks = {}
            self.__ports = {}

            self.list_of_examples = []
            # Create user directory if does not exist
            directories = ["extensions",
                           "images",
                           "code-gen"]
            for name in directories:
                path = os.path.join(System.get_user_dir(), name)
                if not os.path.isdir(path):
                    try:
                        os.makedirs(path)
                    except Exception as error:
                        System.log(error)

            self.__preferences = PreferencesPersistence.load(
                        System.get_user_dir())

        # ----------------------------------------------------------------------
        def reload(self):
            self.__load_examples()
            self.__load_extensions()

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
        def get_preferences(self):
            return self.__preferences

        # ----------------------------------------------------------------------
        def __load_examples(self):
            # Load Examples from the system
            self.list_of_examples = []
            # Load Examples from the user space
            file_path = os.path.join(System.get_user_dir(),"extensions")
            for language in os.listdir(file_path):
                path = os.path.join(file_path, language)
                path = os.path.join(path, "examples")
                for filename in os.listdir(path):
                    file_path = os.path.join(path, filename)
                    if filename.endswith(".mscd"):
                        self.list_of_examples.append(file_path)
            self.list_of_examples.sort()

        # ----------------------------------------------------------------------
        def __load_extensions(self):
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
                    if not name.startswith(System.APP + "_lib") and not name_par.startswith(System.APP + "_lib"):
                        continue

                    if ispkg:
                        if name_par != "" and not name.startswith(System.APP):
                            name = name_par + "." + name
                        __import__(name)
                        path = getattr(
                            sys.modules[name], '__path__', None) or []
                        walk_lib_packages(path, name)
                    else:
                        module = __import__(name, fromlist="dummy")
                        for class_name, obj in inspect.getmembers(module):
                            if not inspect.isclass(obj):
                                continue
                            modname = inspect.getmodule(obj).__name__
                            if not modname.startswith(System.APP + "_lib"):
                                continue
                            try:
                                instance = obj()
                            except Exception as error:
                                continue
                            if isinstance(instance, BlockModel):
                                if instance.label != "":
                                    self.__blocks[instance.type] = instance
                                    continue
                            elif isinstance(instance, Port):
                                self.__ports[instance.type] = instance
                                continue
                            elif isinstance(instance, CodeTemplate):
                                self.__code_templates[instance.type] = instance
                                continue

            walk_lib_packages(None, "")

            # Load XML files in user space
            data_dir = System.get_user_dir() + "/extensions"

            if not os.path.exists(data_dir):
                return
            # List of languages
            for languages in os.listdir(data_dir):
                lang_path = os.path.join(data_dir, languages)

                # Load Code Templates
                for file_name in os.listdir(os.path.join(lang_path, "codetemplates")):
                    if not file_name.endswith(".json"):
                        continue
                    file_path = os.path.join(lang_path,"codetemplates")
                    file_path = os.path.join(file_path, file_name)
                    code_template = CodeTemplateControl.load(file_path)
                    if code_template is not None:
                        code_template.file = file_path
                        self.__code_templates[code_template.type] = code_template

                # Load Ports
                for file_name in os.listdir(os.path.join(lang_path,"ports")):
                    if not file_name.endswith(".json"):
                        continue
                    file_path = os.path.join(lang_path,"ports")
                    file_path = os.path.join(file_path, file_name)
                    port = PortControl.load(file_path)
                    if port is not None:
                        port.file = file_path
                        self.__ports[port.type] = port

                # Load Blocks
                for extension_name in os.listdir(os.path.join(lang_path,"blocks")):
                    extension_path = os.path.join(lang_path, "blocks")
                    extension_path = os.path.join(extension_path, extension_name)
                    for group_name in os.listdir(extension_path):
                        group_path = os.path.join(extension_path, group_name)
                        for file_name in os.listdir(group_path):
                            if not file_name.endswith(".json"):
                                continue
                            file_path = os.path.join(group_path, file_name)
                            block = BlockControl.load(file_path)
                            if block is not None:
                                block.file = file_path
                                self.__blocks[block.type] = block

            for key in self.__blocks:
                try:
                    block = self.__blocks[key]
                    BlockControl.load_ports(block, self.__ports)
                except:
                    print("Error in loading block " + key)

    # ----------------------------------------------------------------------
    def __init__(self):
        if not System.instance:
            System.instance = System.__Singleton()

    # ----------------------------------------------------------------------
    def __new__(cls):  # __new__ always a classmethod
        if System.instance is None:
            System.instance = System.__Singleton()

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
    def get_preferences(cls):
        """
        This method returns System installed blocks.
        """
        return cls.instance.get_preferences()

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
            print("Could not set logger")

    # ----------------------------------------------------------------------
    @classmethod
    def log(cls, msg):
        "This metho show the log."
        try:
            cls.instance.Log.log(msg)
        except:
            print(msg)
            
    # ----------------------------------------------------------------------
    @classmethod
    def get_user_dir(cls):
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, System.APP)

    # ----------------------------------------------------------------------
    @classmethod
    def replace_wildcards(cls, name, diagram):
        """
        This method replace the wildcards.

        Returns:

            * **Types** (:class:`str<str>`)
        """
        result = name.replace("%t", str(time.time()))
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
        name = System.get_preferences().default_directory
        name = System.replace_wildcards(name, diagram)
        if not name.endswith("/"):
            name = name + "/"
        return name

