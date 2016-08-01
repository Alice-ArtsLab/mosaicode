#!/usr/bin/env python
 # -*- coding: utf-8 -*-

class Plugin():

    def __init__(self):
        self.type = -1
        self.id = -1
        self.x = 0
        self.y = 0

    # ----------------------------------------------------------------------
    def get_help(self):
        return ""

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        pass

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {}

    # ----------------------------------------------------------------------
    def set_properties(self, data):
        for key in self.get_properties():
            self.__dict__[key] = data[key]

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

    # ----------------------------------------------------------------------
    def get_xml(self):
        xml = "<properties>\n"
        xml += "<block type='" + str(self.type) + "' id='" + str(self.id) + "'>\n"
        for key in self.get_properties():
            xml += "<property name='" + key + "' value='" + str(self.__dict__[key]) + "' />\n"
        xml += "</block>\n"
        xml += "</properties>\n"
        return xml

# ------------------------------------------------------------------------------
