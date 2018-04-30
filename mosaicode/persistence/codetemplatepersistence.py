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


class CodeTemplatePersistence():
    """
    This class contains methods related the CodeTemplatePersistence class.
    """

    tag_name = "MosaicodeCodeTemplate"
    properties = ["name", "type", "description",
                  "language", "command", "extension", "code"]

    # ----------------------------------------------------------------------
    @classmethod
    def load_xml(cls, file_name):
        """
        This method loads the code_template from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        # load the code_template
        if os.path.exists(file_name) is False:
            return None
        parser = XMLParser(file_name)

        if parser.getTag(CodeTemplatePersistence.tag_name) is None:
            return None
        ct = parser.getTag(CodeTemplatePersistence.tag_name)

        code_template = CodeTemplate()
        for prop in CodeTemplatePersistence.properties:
            if hasattr(ct, prop) and hasattr(code_template, prop):
                code_template.__dict__[prop] = parser.getTagAttr(
                    CodeTemplatePersistence.tag_name, prop)

        code_parts = parser.getTag(CodeTemplatePersistence.tag_name).getTag(
            "code_parts").getChildTags("code_part")
        for code_part in code_parts:
            code_template.code_parts.append(code_part.getAttr("value"))

        if code_template.name == "":
            return None
        return code_template

    # ----------------------------------------------------------------------
    @classmethod
    def save_xml(cls, code_template, path):
        """
        This method save the code_template in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        code_template.source = "xml"
        parser = XMLParser()
        parser.addTag(CodeTemplatePersistence.tag_name)

        for prop in CodeTemplatePersistence.properties:
            if hasattr(code_template, prop):
                parser.setTagAttr(CodeTemplatePersistence.tag_name,
                                  prop, code_template.__dict__[prop])

        parser.appendToTag(CodeTemplatePersistence.tag_name, 'code_parts')
        for key in code_template.code_parts:
            parser.appendToTag('code_parts', 'code_part', value=key.strip())

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
    def save_python(cls, code_template, path):
        """
        This method save the codetemplate in user space in python extension.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        parser = PythonParser()
        parser.class_name = code_template.name.replace(' ', '')
        parser.dependencies = [
            {'from': 'mosaicode.model.codetemplate', 'import': 'CodeTemplate'}]
        parser.inherited_classes = ['CodeTemplate']
        parser.setAttribute('name', code_template.name)
        parser.setAttribute('description', code_template.description)
        parser.setAttribute('language', code_template.language)
        parser.setAttribute('command', code_template.command)
        parser.setAttribute('extension', code_template.extension)
        parser.setAttribute('code', code_template.code)
        parser.setAttribute('code_parts', code_template.code_parts)

        if not Persistence.create_dir(path):
            return False

        file_name = path + code_template.name.lower().replace(' ', '_') + ".py"
        try:
            parser.save(file_name)
        except IOError as e:
            return False
        return True
# ----------------------------------------------------------------------
