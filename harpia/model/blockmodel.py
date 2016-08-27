#!/usr/bin/env python
 # -*- coding: utf-8 -*-

class BlockModel(object):

    #----------------------------------------------------------------------
    def __init__(self, plugin):
        self.__plugin = plugin

    #----------------------------------------------------------------------
    def get_id(self):
        return self.__plugin.id

    #----------------------------------------------------------------------
    def get_type(self):
        return self.__plugin.get_description()["Type"]

    #----------------------------------------------------------------------
    def get_xml(self):
        return self.__plugin.get_xml()

    #----------------------------------------------------------------------
    def get_help(self):
        return self.__plugin.get_help()

    #----------------------------------------------------------------------
    def get_properties(self):
        return self.__plugin.get_properties()

    #----------------------------------------------------------------------
    def get_plugin(self):
        return self.__plugin

    #----------------------------------------------------------------------
    def get_description(self):
        return self.__plugin.get_description()

