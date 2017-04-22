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
    def load(cls, file_name):
        """
        This method loads the code_template from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        # load the code_template
        if os.path.exists(file_name) is False:
            return
        parser = XMLParser(file_name)

        if parser.getTag("HarpiaCodeTemplate") is None:
            return None

        code_template = CodeTemplate()
        code_template.name = parser.getTagAttr("HarpiaCodeTemplate",  "name")
        code_template.description = parser.getTagAttr("HarpiaCodeTemplate",  "description")
        code_template.language = parser.getTagAttr("HarpiaCodeTemplate",  "language")
        code_template.extension = parser.getTagAttr("HarpiaCodeTemplate",  "extension")
        code_template.source = parser.getTagAttr("HarpiaCodeTemplate",  "source")
        code_template.command = parser.getTag("HarpiaCodeTemplate").getTag("command").getText()
        code_template.code = parser.getTag("HarpiaCodeTemplate").getTag("code").getText()

        if code_template.name == "":
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
        parser.setTagAttr('HarpiaCodeTemplate','name', code_template.name)
        parser.setTagAttr('HarpiaCodeTemplate','description', code_template.description)
        parser.setTagAttr('HarpiaCodeTemplate','language', code_template.language)
        parser.setTagAttr('HarpiaCodeTemplate','extension', code_template.extension)
        parser.setTagAttr('HarpiaCodeTemplate','source', code_template.source)
        parser.appendToTag('HarpiaCodeTemplate','command').string = str(code_template.command)
        parser.appendToTag('HarpiaCodeTemplate','code').string = str(code_template.code)

        try:
            data_dir = System.get_user_dir() + "/extensions/"
            file_name = data_dir + code_template.name + ".xml"
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
        System.code_templates[code_template.name] = code_template

    # ----------------------------------------------------------------------
    @classmethod
    def delete_code_template(cls, code_template_key):
        from harpia.system import System
        code_template = System.code_templates[code_template_key]
        if code_template.source == "xml":
            data_dir = System.get_user_dir() + "/extensions/"
            file_name = data_dir + code_template.name + ".xml"
            os.remove(file_name)
            System.code_templates.pop(code_template_key, None)
            return True
        else:
            return False
# ----------------------------------------------------------------------
