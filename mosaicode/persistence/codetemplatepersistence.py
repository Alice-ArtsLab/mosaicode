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
from mosaicode.persistence.persistence import Persistence

tag_name = "MosaicodeCodeTemplate"

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
            return None
        parser = XMLParser(file_name)

        if parser.getTag(tag_name) is None:
            return None

        try:
            code_template = CodeTemplate()
            code_template.name = parser.getTagAttr(tag_name,  "name")
            code_template.type = parser.getTagAttr(tag_name,  "type")
            code_template.description = parser.getTagAttr(tag_name,  "description")
            code_template.language = parser.getTagAttr(tag_name,  "language")
            code_template.command = parser.getTag(tag_name).getTag("command").getText()
            code_template.extension = parser.getTagAttr(tag_name,  "extension")
            code_template.code = parser.getTag(tag_name).getTag("code").getText()

            code_parts = parser.getTag(tag_name).getTag("code_parts").getChildTags("code_part")
            for code_part in code_parts:
                code_template.code_parts.append(code_part.getAttr("value"))

        except Exception as e:
            print e
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
        parser.addTag(tag_name)
        parser.setTagAttr(tag_name,'name', code_template.name)
        parser.setTagAttr(tag_name,'type', code_template.type)
        parser.setTagAttr(tag_name,'description', code_template.description)
        parser.setTagAttr(tag_name,'language', code_template.language)
        parser.setTagAttr(tag_name,'extension', code_template.extension)
        parser.appendToTag(tag_name,'command').string = str(code_template.command)
        parser.appendToTag(tag_name,'code').string = str(code_template.code)

        parser.appendToTag(tag_name, 'code_parts')
        for key in code_template.code_parts:
            parser.appendToTag('code_parts', 'code_part', value=key.strip())

        path = System.get_user_dir() + "/extensions/"
        path = path + code_template.language + "/"
        if not Persistence.create_dir(path):
            return False
        try:
            file_name = path + code_template.type + ".xml"
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
        parser.setAttribute('code_parts', code_template.code_parts)

        path = System.get_user_dir() + "/extensions/"
        path = path + code_template.language + "/"
        if not Persistence.create_dir(path):
            return False
        try:
            file_name = path + code_template.name.lower().replace(' ', '_') + ".py"
            parser.save(file_name)
        except IOError as e:
            return False
        return True
# ----------------------------------------------------------------------
