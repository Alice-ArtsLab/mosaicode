# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the CodeTemplateControl class.
"""
import inspect  # For module inspect
import os
import pkgutil  # For dynamic package load
from os.path import expanduser

from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.persistence.codetemplatepersistence import \
    CodeTemplatePersistence
from mosaicode.utils.XMLUtils import XMLParser


class CodeTemplateControl():
    """
    This class contains methods related the CodeTemplateControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self):
        pass

    # ----------------------------------------------------------------------
    @classmethod
    def export_xml(cls):
        from mosaicode.system import System as System
        System()
        code_templates = System.get_code_templates()
        for key in code_templates:
            path = System.get_user_dir()
            path = os.path.join(path,
                                'extensions',
                                code_templates[key].language,
                                'codetemplates')
            CodeTemplatePersistence.save_xml(code_templates[key], path)

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        return CodeTemplatePersistence.load_xml(file_name)

    # ----------------------------------------------------------------------
    @classmethod
    def add_code_template(cls, code_template):
        # save it
        from mosaicode.system import System as System
        System()
        path = System.get_user_dir() + "/extensions/"
        path = path + code_template.language + "/codetemplates/"
        CodeTemplatePersistence.save_xml(code_template, path)

    # ----------------------------------------------------------------------
    @classmethod
    def delete_code_template(cls, code_template_key):
        from mosaicode.system import System
        code_templates = System.get_code_templates()
        if code_template_key not in code_templates:
            System.log("Error: This code template does not exist")
            return False
        code_template = code_templates[code_template_key]
        if code_template.file is not None:
            os.remove(code_template.file)
        else:
            System.log("Error: This code template does not have a file.")            
        return code_template.file

    # ----------------------------------------------------------------------
    @classmethod
    def print_template(cls, code_template):
        """
        This method prints the CodeTemplate properties.
        """
        separator = '-------------------------------------------------'

        print(separator)
        print('CodeTemplate.type: ', code_template.type)

        print(separator)
        print('CodeTemplate.name: ', code_template.name)

        print(separator)
        print('CodeTemplate.file: ', code_template.file)

        print(separator)
        print('CodeTemplate.description: ', code_template.description)

        print(separator)
        print('CodeTemplate.language: ', code_template.language)

        print(separator)
        print('CodeTemplate.command: ', code_template.command)

        print(separator)
        print('CodeTemplate.files:\n')
        for file in code_template.files:
            print('\n', file)

        print(separator)
        print('CodeTemplate.code_parts:\n')
        for code_part in code_template.code_parts:
            print('\n', code_part)

        print(separator)
        print('CodeTemplate.properties:\n')
        for property in code_template.properties:
            print('\n', property)
# ----------------------------------------------------------------------
