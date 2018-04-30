#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CodeTemplate(object):
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes

    """
    This class contains the base attributes of each code generator.
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        self.type = self.__class__.__module__
        self.name = ""
        self.file = None
        self.description = ""
        self.language = ""
        self.command = ""
        self.extension = ""
        self.code = "Invalid Code Template"
        self.code_parts = []

    def equals(self, code_template):
        for key in self.__dict__:
            if not hasattr(code_template, key):
                return False
            if code_template.__dict__[key] != self.__dict__[key]:
                return False
        return True
# ------------------------------------------------------------------------------
