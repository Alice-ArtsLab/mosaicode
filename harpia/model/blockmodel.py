#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BlockModel(object):

    # ----------------------------------------------------------------------

    def __init__(self, plugin):
        self.__plugin = plugin
        self.x = plugin.x
        self.y = plugin.y

    # ----------------------------------------------------------------------
    def get_output_port_name(self, number):
        return self.__plugin.get_output_port_name(number)

    # ----------------------------------------------------------------------
    def get_input_port_name(self, number):
        return self.__plugin.get_input_port_name(number)

    # ----------------------------------------------------------------------
    def get_id(self):
        return self.__plugin.id

    # ----------------------------------------------------------------------
    def set_id(self, block_id):
        self.__plugin.id = block_id

    # ----------------------------------------------------------------------
    def get_type(self):
        return self.__plugin.type

    # ----------------------------------------------------------------------
    def get_help(self):
        return self.__plugin.get_help()

    # ----------------------------------------------------------------------
    def get_properties(self):
        return self.__plugin.get_properties()

    # ----------------------------------------------------------------------
    def set_properties(self, data):
        self.get_plugin().set_properties(data)

    # ----------------------------------------------------------------------
    def get_language(self):
        return self.__plugin.language

    # ----------------------------------------------------------------------
    def get_plugin(self):
        return self.__plugin

    # ----------------------------------------------------------------------
    def __str__(self):
        return str(self.get_id())

    # ----------------------------------------------------------------------
    def get_help(self):
        return self.__plugin.get_help()

    # ----------------------------------------------------------------------
    def get_label(self):
        return self.__plugin.get_label()

    # ----------------------------------------------------------------------
    def get_icon(self):
        return self.__plugin.get_icon()

    # ----------------------------------------------------------------------
    def get_color(self):
        return self.__plugin.get_color()

    # ----------------------------------------------------------------------
    def get_in_types(self):
        return self.__plugin.get_in_types()

    # ----------------------------------------------------------------------
    def get_out_types(self):
        return self.__plugin.get_out_types()

    # ----------------------------------------------------------------------
    def get_group(self):
        return self.__plugin.get_group()

