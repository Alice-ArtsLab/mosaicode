#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Port(object):
    """
    This class contains the base attributes of each plugin port.
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        self.type = ""
        self.language = ""
        self.label = ""
        self.color = "#000"
        self.multiple = False
        self.source = "Python"
        self.code = ""
        self.input_codes = ["","","","",""]
        self.output_codes = ["","","","",""]

    # ----------------------------------------------------------------------
    def get_type(self):
        return self.type

    # ----------------------------------------------------------------------
    def get_language(self):
        return self.language

    # ----------------------------------------------------------------------
    def get_label(self):
        return self.label

    # ----------------------------------------------------------------------
    def get_color(self):
        return self.color

    # ----------------------------------------------------------------------
    def get_multiple(self):
        return self.multiple

    # ----------------------------------------------------------------------
    def get_code(self):
        return self.code

    # ----------------------------------------------------------------------
    def get_source(self):
        return self.source

# ------------------------------------------------------------------------------
