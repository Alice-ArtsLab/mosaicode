# -*- coding: utf-8 -*-

class Preferences(object):

    def __init__(self):
        self.conf_file_path = "configuration.xml"
        self.recent_files = []
        self.default_directory = "/tmp/%l/%n-%t"
        self.default_filename = "%n"
        self.grid = 10
        self.port = 49151

        # GUI stuff
        self.width = 900
        self.height = 500
        self.hpaned_work_area = 150
        self.vpaned_bottom = 450
        self.vpaned_left = 300

# ------------------------------------------------------------------------------
