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


class CodeTemplateControl():
    """
    This class contains methods related the CodeTemplateControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self):
        pass

    # ----------------------------------------------------------------------
    @classmethod
    def export(cls):
        from mosaicode.system import System as System
        System()
        code_templates = System.get_code_templates()
        result = True
        for key in code_templates:
            path = System.get_user_dir()
            path = os.path.join(path,
                                'extensions',
                                code_templates[key].language,
                                'codetemplates')
            result = result and CodeTemplatePersistence.save(
                    code_templates[key], path)
        return result

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        return CodeTemplatePersistence.load(file_name)

    # ----------------------------------------------------------------------
    @classmethod
    def add_code_template(cls, code_template):
        # save it
        from mosaicode.system import System as System
        System()
        path = os.path.join(System.get_user_dir(), "extensions")
        path = os.path.join(path, code_template.language)
        path = os.path.join(path, "codetemplates")
        CodeTemplatePersistence.save(code_template, path)

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
