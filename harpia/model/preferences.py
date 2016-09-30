#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import ast

class Preferences(object):

    def __init__(self):
        self.conf_file_path = "~/.harpiaConf.xml"
        self.recent_files = []
        self.default_directory = "/tmp/%l/%n-%t"
        self.default_filename = "%n"
        self.error_log_file = "ErrorLog"

        # GUI stuff
        self.width = 900
        self.height = 500
        self.hpaned_work_area = 150
        self.vpaned_bottom = 450
        self.vpaned_left = 300

    # ----------------------------------------------------------------------
    def get_recent_files(self):
        return map(str, self.recent_files)

    # ----------------------------------------------------------------------
    def get_recent_files_as_array(self):
        try:
            return ast.literal_eval(self.recent_files)
        except:
            return self.recent_files

    # ----------------------------------------------------------------------
    def add_recent_file(self, file_name):
        try:
            self.recent_files = ast.literal_eval(self.recent_files)
        except:
            return
        if file_name in self.recent_files:
            self.recent_files.remove(file_name)
        self.recent_files.insert(0,file_name)
        if len(self.recent_files) > 10:
            self.recent_files.pop()

    # ----------------------------------------------------------------------
    def get_default_directory(self):
        return self.default_directory

    # ----------------------------------------------------------------------
    def set_default_directory(self, default_directory):
        self.default_directory = default_directory

    # ----------------------------------------------------------------------
    def get_default_filename(self):
        return self.default_filename

    # ----------------------------------------------------------------------
    def set_default_filename(self, default_filename):
        self.default_filename = default_filename

    # ----------------------------------------------------------------------
    def get_error_log_file(self):
        return self.error_log_file

    # ----------------------------------------------------------------------
    def set_error_log_file(self, error_log_file):
        self.error_log_file = error_log_file

    # ----------------------------------------------------------------------
    def get_width(self):
        return int(self.width)

    # ----------------------------------------------------------------------
    def set_width(self, width):
        self.width = int(width)

    # ----------------------------------------------------------------------
    def get_height(self):
        return int(self.height)

    # ----------------------------------------------------------------------
    def set_height(self, height):
        self.height = height

    # ----------------------------------------------------------------------
    def get_hpaned_work_area(self):
        return int(self.hpaned_work_area)

    # ----------------------------------------------------------------------
    def set_hpaned_work_area(self, hpaned_work_area):
        self.hpaned_work_area = hpaned_work_area

    # ----------------------------------------------------------------------
    def get_vpaned_bottom(self):
        return int(self.vpaned_bottom)

    # ----------------------------------------------------------------------
    def set_vpaned_bottom(self, vpaned_bottom):
        self.vpaned_bottom = vpaned_bottom

    # ----------------------------------------------------------------------
    def get_vpaned_left(self):
        return int(self.vpaned_left)

    # ----------------------------------------------------------------------
    def set_vpaned_left(self, vpaned_left):
        self.vpaned_left = vpaned_left

# ------------------------------------------------------------------------------
