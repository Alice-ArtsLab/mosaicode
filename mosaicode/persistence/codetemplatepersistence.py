# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the CodeTemplatePersistence class.
"""
import ast
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
import json
from os.path import join
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.persistence.persistence import Persistence


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
        if os.path and os.path.isdir(file_name):
            return None

        code_template = CodeTemplate()
        data = ""

        try:
            data_file = open(file_name, 'r')
            data = json.load(data_file)
            data_file.close()

            if data["data"] != "CODE_TEMPLATE":
                return None

            code_template.version = data["version"]
            code_template.name = data["name"]
            code_template.type = data["type"]
            code_template.description = data["description"]
            code_template.language = data["language"]
            code_template.command = data["command"]

            props = data["properties"]
            for prop in props:
                code_template.properties.append(prop)

            codes = data["codes"]
            if codes:
                for code in codes:
                    code_template.codes[code["filename"]] = code["code"]

            codes = data["codes"]

            parts = data["code_parts"]
            for part in parts:
                code_template.code_parts.append(part)
        except:
            return None

        if code_template.name == "":
            return None
        return code_template

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, code_template, path):
        """
        This method save the code_template in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """

        x = {
            "source": "JSON",
            "data": "CODE_TEMPLATE",
            "version": code_template.version,
            'name': code_template.name,
            'type': code_template.type,
            'description': code_template.description,
            'language': code_template.language,
            'command': code_template.command,
            "code_parts": code_template.code_parts,
            "properties":[],
            "codes":[]
        }

        for key in code_template.properties:
            x["properties"].append(key)

        for key in code_template.codes:
            x["codes"].append({
                "filename":key,
                "code": code_template.codes[key]
                })

        if not Persistence.create_dir(path):
            from mosaicode.system import System as System
            System.log("Problem creating dir to save Code templates")
            return False

        try:
            file_name = code_template.name
            data_file = open(os.path.join(path, file_name + '.json'), 'w')
            data_file.write(json.dumps(x, indent=4))
            data_file.close()
        except IOError as e:
            from mosaicode.system import System as System
            System.log("Problem saving Code template: " + e)
            return False
        return True

# ----------------------------------------------------------------------
