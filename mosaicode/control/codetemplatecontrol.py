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
        CodeTemplatePersistence.load(file_name)

    # ----------------------------------------------------------------------
    @classmethod
    def export_xml(cls):
        from mosaicode.system import System as System
        System()
        for code_template in System.code_templates:
            print "Exporting code template " + code_template
            CodeTemplatePersistence.save(System.code_templates[code_template])

    # ----------------------------------------------------------------------
    @classmethod
    def export_python(cls):
        from mosaicode.system import System as System
        System()
        for code_template in System.code_templates:
            print "Exporting code template " + code_template
            CodeTemplatePersistence.save_python(System.code_templates[code_template])

    # ----------------------------------------------------------------------
    @classmethod
    def add_code_template(cls, code_template):
        # first, save it
        CodeTemplatePersistence.save(code_template)
        # Then add it to system
        from mosaicode.system import System
        System.code_templates[code_template.type] = code_template

    # ----------------------------------------------------------------------
    @classmethod
    def delete_code_template(cls, code_template_key):
        from mosaicode.system import System
        code_template = System.code_templates[code_template_key]
        if code_template.source == "xml":
            data_dir = System.get_user_dir() + "/extensions/"
            file_name = data_dir + code_template.type + ".xml"
            os.remove(file_name)
            System.code_templates.pop(code_template_key, None)
            return True
        else:
            return False
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
        print 'CodeTemplate.code =', code_template.code
        print 'CodeTemplate.source =', code_template.source
# ----------------------------------------------------------------------
