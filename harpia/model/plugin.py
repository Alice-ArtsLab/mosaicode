#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Plugin(object):
    """
    This class contains the base attributes of each plug-in,
    their position on the screen, id and others applicable properties for each one. 
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        self.type = self.__class__.__module__
        self.language = ""
        self.framework = ""
        self.id = -1
        self.x = 0
        self.y = 0

        # Code generation
        self.properties = []
        self.header = ""
        self.vars = ""
        self.function_call = ""
        self.dealloc = ""
        self.out_dealloc = ""

        # Appearance
        self.help = ""
        self.label = ""
        self.icon = "images/show.png"
        self.color = "200:200:25:150"
        self.in_types = []
        self.out_types = []
        self.group = "Undefined"

    # ----------------------------------------------------------------------
    def get_help(self):
        """
        Get the plugins help text.
        """
        return self.help

    # ----------------------------------------------------------------------
    def get_label(self):
        """
        Get labels of plugins.
        """
        return self.label

    # ----------------------------------------------------------------------
    def get_icon(self):
        """
        Get icon of plugins.
        """

        return self.icon

    # ----------------------------------------------------------------------
    def get_color(self):
        """
        Get color in format RGB and return. 
        """
        color = self.color.split(":")
        color = [int(color[0]), int(color[1]), int(color[2]), int(color[3])]
        color = int(color[0]) * 0x1000000 + \
            int(color[1]) * 0x10000 + \
            int(color[2]) * 0x100 + \
            int(color[3]) * 0x01
        return color

    # ----------------------------------------------------------------------
    def get_in_types(self):
        return self.in_types

    # ----------------------------------------------------------------------
    def get_out_types(self):
        return self.out_types

    # ----------------------------------------------------------------------
    def get_group(self):
        return self.group

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
        return self.header

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return self.vars

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return self.function_call

    # ----------------------------------------------------------------------
    def generate_dealloc(self):
        return self.dealloc

    # ----------------------------------------------------------------------
    def generate_out_dealloc(self):
        return self.out_dealloc

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def set_properties(self, data):
        for prop in self.get_properties():
            key = prop.get("name")
            if key in data:
                prop["value"] = data[key]
            else:
                print "Plugin.set_property ERROR: key ", key, "not present"

    # ----------------------------------------------------------------------
    def get_properties(self):
        return self.properties

    # ----------------------------------------------------------------------
    def get_plugin(self):
        return self

    # ----------------------------------------------------------------------
    def __str__(self):
        return str(self.get_id())

# ------------------------------------------------------------------------------
