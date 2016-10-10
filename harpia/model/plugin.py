#!/usr/bin/env python
 # -*- coding: utf-8 -*-

class Plugin(object):

    # ----------------------------------------------------------------------
    def __init__(self):
        self.type = self.__class__.__module__
        self.id = -1
        self.x = 0
        self.y = 0
        self.help = ""
        self.description = {}
        # Code generation
        self.vars = ""

    # ----------------------------------------------------------------------
    def get_output_port_name(self, number):
        return "block_" + str(self.id) + "o" + str(number)

    # ----------------------------------------------------------------------
    def get_input_port_name(self, number):
        return "block_" + str(self.id) + "i" + str(number)

    # ----------------------------------------------------------------------
    def get_position(self):
        return (self.x, self.y)

    # ----------------------------------------------------------------------
    def get_type(self):
        return self.type

    # ----------------------------------------------------------------------
    def set_id(self, value):
        self.id = value

    # ----------------------------------------------------------------------
    def get_id(self):
        return self.id

    # ----------------------------------------------------------------------
    def get_language(self):
        try:
            return self.language
        except:
            return None

    # ----------------------------------------------------------------------
    def get_help(self):
        return self.help

    # ----------------------------------------------------------------------
    def generate_header(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return self.vars

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return ""

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return self.description

    # ----------------------------------------------------------------------
    def set_properties(self, data):
        for key in self.get_properties():
            if key in self.__dict__ and key in data:
                self.__dict__[key] = data[key]
            else:
                print "Plugin.set_property ERROR: key ", key , "not present" 

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

    # ----------------------------------------------------------------------
    def get_plugin(self):
        return self

    # ----------------------------------------------------------------------
    def get_xml(self):
        xml = ""
        for key in self.get_properties():
            xml += "\t\t<property name='" + key + "' value='" + str(self.__dict__[key]) + "' />\n"
        return xml

    #----------------------------------------------------------------------
    def __str__(self):
        return str(self.get_id())

# ------------------------------------------------------------------------------
