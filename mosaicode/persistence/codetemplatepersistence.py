# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the CodeTemplatePersistence class.
"""
import ast
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
from os.path import join
from mosaicode.utils.XMLUtils import XMLParser
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.persistence.persistence import Persistence

tag_name = "MosaicodeCodeTemplate"

class CodeTemplatePersistence():
    """
    This class contains methods related the CodeTemplatePersistence class.
    """

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
        if os.path and os.path.isdir(file_name):
            return None
        parser = XMLParser(file_name)

        if parser.getTag(tag_name) is None:
            return None
        ct = parser.getTag(tag_name)

        code_template = CodeTemplate()
        code_template.name = parser.getTagAttr(tag_name, "name")
        code_template.type = parser.getTagAttr(tag_name, "type")
        code_template.description = parser.getTagAttr(tag_name, "description")
        code_template.language = parser.getTagAttr(tag_name, "language")
        code_template.command = parser.getTagAttr(tag_name, "command")

        parts = parser.getTag(tag_name)
        parts = parts.getTag("code_parts")
        if parts:
            parts = parts.getChildTags("code_part")
            for part in parts:
                code_template.code_parts.append(part.getAttr("value"))

        parts = parser.getTag(tag_name)
        parts = parts.getTag("files")
        if parts:
            parts = parts.getChildTags("file")
            for part in parts:
                code_template.files[part.getAttr("name_")] = part.getAttr("value")

        parts = parser.getTag(tag_name)
        parts = parts.getTag("properties")
        if parts:
            parts = parts.getChildTags("property")
            for part in parts:
                code_template.properties.append(ast.literal_eval(part.getAttr("value")))

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
        parser.addTag(tag_name)

        parser.setTagAttr(tag_name, 'name', code_template.name)
        parser.setTagAttr(tag_name, 'type', code_template.type)
        parser.setTagAttr(tag_name, 'description', code_template.description)
        parser.setTagAttr(tag_name, 'language', code_template.language)
        parser.setTagAttr(tag_name, 'command', code_template.command)

        parser.appendToTag(tag_name, 'code_parts')
        for key in code_template.code_parts:
            parser.appendToTag('code_parts', 'code_part', value=key.strip())

        parser.appendToTag(tag_name, 'files')
        for key in code_template.files:
            parser.appendToTag(
                    'files',
                    'file',
                    name_=key,
                    value=code_template.files[key]
                    )

        parser.appendToTag(tag_name, 'properties')
        for key in code_template.properties:
            parser.appendToTag('properties', 'property', value=key) 

        if not Persistence.create_dir(path):
            return False
        try:
            file_name = code_template.name
            code_template_file = file(os.path.join(path, file_name + '.xml'), 'w')
            code_template_file.write(parser.prettify())
            code_template_file.close()
        except IOError as e:
            return False
        return True

# ----------------------------------------------------------------------
