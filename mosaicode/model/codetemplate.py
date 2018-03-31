#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CodeTemplate(object):
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

# ------------------------------------------------------------------------------
