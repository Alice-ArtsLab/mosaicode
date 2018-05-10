# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the CodeTemplateControl class.
"""
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
from os.path import expanduser
from mosaicode.utils.XMLUtils import XMLParser
from mosaicode.utils.PythonUtils import PythonParser
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.persistence.codetemplatepersistence import CodeTemplatePersistence


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
        return CodeTemplatePersistence.load_xml(file_name)

    # ----------------------------------------------------------------------
    @classmethod
    def export_xml(cls):
        from mosaicode.system import System as System
        System()
        code_templates = System.get_code_templates()
        for code_template in code_templates:
            path = System.get_user_dir() + "/extensions/"
            path = path + code_template.language + "/"
            CodeTemplatePersistence.save_xml(code_templates[code_template])

    # ----------------------------------------------------------------------
    @classmethod
    def export_python(cls):
        from mosaicode.system import System as System
        System()
        code_templates = System.get_code_templates()
        for code_template in code_templates:
            path = System.get_user_dir() + "/extensions/"
            path = path + code_template.language + "/"
            CodeTemplatePersistence.save_python(
                code_templates[code_template], path)

    # ----------------------------------------------------------------------
    @classmethod
    def add_code_template(cls, code_template):
        # save it
        from mosaicode.system import System as System
        System()
        path = System.get_user_dir() + "/extensions/"
        path = path + code_template.language + "/"
        CodeTemplatePersistence.save_xml(code_template, path)

    # ----------------------------------------------------------------------
    @classmethod
    def delete_code_template(cls, code_template_key):
        from mosaicode.system import System
        code_templates = System.get_code_templates()
        code_template = code_templates[code_template_key]
        if code_template.file is not None:
            os.remove(code_template.file)
        return code_template.file

    # ----------------------------------------------------------------------
    @classmethod
    def print_template(cls, code_template):
        """
        This method prints the CodeTemplate properties.
        """
        print 'CodeTemplate.type =', code_template.type
        print 'CodeTemplate.name =', code_template.name
        print 'CodeTemplate.description =', code_template.description
        print 'CodeTemplate.language =', code_template.language
        print 'CodeTemplate.command =', code_template.command
        print 'CodeTemplate.extension =', code_template.extension
        print 'CodeTemplate.file =', code_template.file
# ----------------------------------------------------------------------
