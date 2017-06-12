# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the CodeTemplatePersistence class.
"""
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
from os.path import expanduser
from mosaicode.utils.XMLUtils import XMLParser
from mosaicode.utils.PythonUtils import PythonParser
from mosaicode.model.codetemplate import CodeTemplate

class CodeTemplatePersistence():
    """
    This class contains methods related the CodeTemplatePersistence class.
    """

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

        if parser.getTag("MosaicodeCodeTemplate") is None:
            return None

        try:
            code_template = CodeTemplate()
            code_template.name = parser.getTagAttr("MosaicodeCodeTemplate",  "name")
            code_template.type = parser.getTagAttr("MosaicodeCodeTemplate",  "type")
            code_template.description = parser.getTagAttr("MosaicodeCodeTemplate",  "description")
            code_template.language = parser.getTagAttr("MosaicodeCodeTemplate",  "language")
            code_template.extension = parser.getTagAttr("MosaicodeCodeTemplate",  "extension")
            code_template.source = parser.getTagAttr("MosaicodeCodeTemplate",  "source")
            code_template.command = parser.getTag("MosaicodeCodeTemplate").getTag("command").getText()
            code_template.code = parser.getTag("MosaicodeCodeTemplate").getTag("code").getText()
        except:
            return None

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
        from mosaicode.system import System
        code_template.source = "xml"
        parser = XMLParser()
        parser.addTag('MosaicodeCodeTemplate')
        parser.setTagAttr('MosaicodeCodeTemplate','name', code_template.name)
        parser.setTagAttr('MosaicodeCodeTemplate','type', code_template.type)
        parser.setTagAttr('MosaicodeCodeTemplate','description', code_template.description)
        parser.setTagAttr('MosaicodeCodeTemplate','language', code_template.language)
        parser.setTagAttr('MosaicodeCodeTemplate','extension', code_template.extension)
        parser.setTagAttr('MosaicodeCodeTemplate','source', code_template.source)
        parser.appendToTag('MosaicodeCodeTemplate','command').string = str(code_template.command)
        parser.appendToTag('MosaicodeCodeTemplate','code').string = str(code_template.code)

        try:
            data_dir = System.get_user_dir() + "/extensions/"
            data_dir = data_dir + code_template.language + "/"
            if not os.path.isdir(data_dir):
                try:
                    os.makedirs(data_dir)
                except:
                    pass
            file_name = data_dir + code_template.type + ".xml"
            code_template_file = file(os.path.expanduser(file_name), 'w')
            code_template_file.write(parser.prettify())
            code_template_file.close()
        except IOError as e:
            return False
        return True

    # ----------------------------------------------------------------------
    @classmethod
    def save_python(cls, code_template):
        """
        This method save the codetemplate in user space in python extension.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        from mosaicode.system import System
        parser = PythonParser()
        parser.class_name = code_template.name.replace(' ', '')
        parser.dependencies = [{'from':'mosaicode.model.codetemplate', 'import':'CodeTemplate'}]
        parser.inherited_classes = ['CodeTemplate']
        parser.setAttribute('type', code_template.type)
        parser.setAttribute('name', code_template.name)
        parser.setAttribute('description', code_template.description)
        parser.setAttribute('language', code_template.language)
        parser.setAttribute('command', code_template.command)
        parser.setAttribute('extension', code_template.extension)
        parser.setAttribute('code', code_template.code)
        parser.setAttribute('source', 'python')

        try:
            data_dir = System.get_user_dir() + "/extensions/"
            data_dir = data_dir + code_template.language + "/"
            if not os.path.isdir(data_dir):
                try:
                    os.makedirs(data_dir)
                except:
                    pass
            file_name = data_dir + code_template.name.lower().replace(' ', '_') + ".py"
            parser.save(file_name)
        except IOError as e:
            return False
        return True
# ----------------------------------------------------------------------
