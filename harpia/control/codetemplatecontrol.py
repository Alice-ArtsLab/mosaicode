# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the CodeTemplateControl class.
"""
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
import harpia.plugins
from os.path import expanduser
from harpia.utils.XMLUtils import XMLParser
from harpia.model.codetemplate import CodeTemplate

class CodeTemplateControl():
    """
    This class contains methods related the CodeTemplateControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self):
        pass

    # ----------------------------------------------------------------------
    @classmethod
    def load_code_templates(cls, system):
        system.code_templates.clear()
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
                    system.code_templates[instance.language] = instance

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
            code_template = CodeTemplateControl.load(home_dir + "/" + file)
            if code_template is None:
                continue
            code_template.source = "xml"
            system.code_templates[code_template.language] = code_template

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        """
        This method loads the code_template from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        # load the code_template
        if os.path.exists(file_name) is False:
            return
        xml_loader = XMLParser(file_name)
        properties = xml_loader.getTag(
                "HarpiaCodeTemplate").getChildTags("property")
        code_template = CodeTemplate()
        for prop in properties:
            try:
                prop.getAttr("key")
            except:
                continue
            if prop.getAttr("key") in code_template.__dict__:
                code_template.__dict__[prop.getAttr("key")] = prop.getAttr("value")
        if code_template.language == "":
            return None
        return code_template

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, code_template):
        """
        This method save the code_template in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        from harpia.system import System
        code_template.source = "xml"
        parser = XMLParser()
        parser.addTag('HarpiaCodeTemplate')
        for key in code_template.__dict__:
            parser.appendToTag('HarpiaCodeTemplate', 'property',
                               key=key, value=code_template.__dict__[key])
        try:
            file_name = System.get_user_dir() + "/" + code_template.name + ".xml"
            code_template_file = file(os.path.expanduser(file_name), 'w')
            code_template_file.write(parser.prettify())
            code_template_file.close()
        except IOError as e:
            return False
        return True

    # ----------------------------------------------------------------------
    @classmethod
    def add_code_template(cls, code_template):
        # first, save it
        CodeTemplateControl.save(code_template)
        # Then add it to system
        from harpia.system import System
        System.code_templates[code_template.language] = code_template

    # ----------------------------------------------------------------------
    @classmethod
    def delete_code_template(cls, code_template_key):
        from harpia.system import System
        code_template = System.code_templates[code_template_key]
        if code_template.source == "xml":
            file_name = System.get_user_dir() + "/" + code_template.name + ".xml"
            os.remove(file_name)
            CodeTemplateControl.load_code_templates(System)
            return True
        else:
            return False
# ----------------------------------------------------------------------
