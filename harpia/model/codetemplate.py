#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CodeTemplate(object):
    """
    This class contains the base attributes of each code generator.
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        self.name = ""
        self.description = ""
        self.language = ""
        self.command = ""
        self.extension = ""
        self.code = "Invalid Code Template"
        self.source = "python"

# ------------------------------------------------------------------------------
