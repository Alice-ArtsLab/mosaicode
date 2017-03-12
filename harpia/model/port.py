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
        self.code = ""
        self.source = "Python"
        self.input_vars = ""
        self.output_vars = ""
        self.input_dealloc = ""
        self.output_dealloc = ""

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

    # ----------------------------------------------------------------------
    def get_input_vars(self):
        return self.input_vars

    # ----------------------------------------------------------------------
    def get_output_vars(self):
        return self.output_vars

   # ----------------------------------------------------------------------
    def get_input_dealloc(self):
        return self.input_dealloc

    # ----------------------------------------------------------------------
    def get_output_dealloc(self):
        return self.output_dealloc
# ------------------------------------------------------------------------------
