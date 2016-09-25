#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.control.preferencescontrol import *

class Preferences(object):

    def __init__(self):
        self.conf_file_path = "~/.harpiaConf.xml"
        self.control = PreferencesControl(self)
        self.__recent_files = []
        self.__default_directory = "/tmp/"
        self.__default_filename = "harpia%d"
        self.__error_log_file = "ErrorLog"

        # GUI stuff
        self.__width = 900
        self.__height = 500
        self.__hpaned_work_area = 150
        self.__vpaned_bottom = 450
        self.__vpaned_left = 300

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
    def get_default_filename(self):
        return self.__default_filename

    # ----------------------------------------------------------------------
    def set_default_filename(self, default_filename):
        self.__default_filename = default_filename
        self.control.save()

    # ----------------------------------------------------------------------
    def get_error_log_file(self):
        return self.__error_log_file

    # ----------------------------------------------------------------------
    def set_error_log_file(self, error_log_file):
        self.__error_log_file = error_log_file
        self.control.save()

    # ----------------------------------------------------------------------
    def get_width(self):
        return self.__width

    # ----------------------------------------------------------------------
    def set_width(self, width):
        self.__width = width
        self.control.save()

    # ----------------------------------------------------------------------
    def get_height(self):
        return self.__height

    # ----------------------------------------------------------------------
    def set_height(self, height):
        self.__height = height
        self.control.save()

    # ----------------------------------------------------------------------
    def get_hpaned_work_area(self):
        return self.__hpaned_work_area

    # ----------------------------------------------------------------------
    def set_hpaned_work_area(self, hpaned_work_area):
        self.__hpaned_work_area = hpaned_work_area
        self.control.save()

    # ----------------------------------------------------------------------
    def get_vpaned_bottom(self):
        return self.__vpaned_bottom

    # ----------------------------------------------------------------------
    def set_vpaned_bottom(self, vpaned_bottom):
        self.__vpaned_bottom = vpaned_bottom
        self.control.save()

    # ----------------------------------------------------------------------
    def get_vpaned_left(self):
        return self.__vpaned_left

    # ----------------------------------------------------------------------
    def set_vpaned_left(self, vpaned_left):
        self.__vpaned_left = vpaned_left
        self.control.save()

# ------------------------------------------------------------------------------
