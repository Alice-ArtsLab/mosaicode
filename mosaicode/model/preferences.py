# -*- coding: utf-8 -*-
import os


class Preferences(object):
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
    """
    This class contain the default preferences from mosaicode user.
    """

    def __init__(self):
        self.conf_file_path = "configuration"

        self.author = ""
        self.license = "GPL 3.0"
        from mosaicode.system import System as System
        self.version = System.VERSION

        self.recent_files = []
        from mosaicode.system import System
        self.default_directory = os.path.join(System.get_user_dir(), "code-gen")
        self.default_filename = "%n"
        self.grid = 10

        # GUI stuff
        self.width = 900
        self.height = 500
        self.hpaned_work_area = 150
        self.vpaned_bottom = 450
        self.vpaned_left = 300

        self.connection = "Curve"
# ------------------------------------------------------------------------------
