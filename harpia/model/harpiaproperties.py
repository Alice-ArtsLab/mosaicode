#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.control.harpiapropertiescontrol import *

class HarpiaProperties(object):

    def __init__(self):
        self.__recent_files = []
        self.__default_directory = "/tmp/"
        self.__error_log_file = "ErrorLog"
        self.conf_file_path = "~/.harpiaConf.xml"
        self.control = HarpiaPropertiesControl(self)

    # ----------------------------------------------------------------------
    def get_recent_files(self):
        return self.__recent_files

    # ----------------------------------------------------------------------
    def set_recent_files(self, recent_files):
        self.__recent_files = []
        self.__recent_files = recent_files
        self.control.save()


    # ----------------------------------------------------------------------
    def add_recent_file(self, file_name):
        if file_name in self.__recent_files:
            self.__recent_files.remove(file_name)
        self.__recent_files.insert(0,file_name)
        if len(self.__recent_files) > 10:
            self.__recent_files.pop()
        self.control.save()

    # ----------------------------------------------------------------------
    def get_default_directory(self):
        return self.__default_directory

    # ----------------------------------------------------------------------
    def set_default_directory(self, default_directory):
        self.__default_directory = default_directory
        self.control.save()

    # ----------------------------------------------------------------------
    def get_error_log_file(self):
        return self.__error_log_file

    # ----------------------------------------------------------------------
    def set_error_log_file(self, error_log_file):
        self.__error_log_file = error_log_file
        self.control.save()

# ------------------------------------------------------------------------------
