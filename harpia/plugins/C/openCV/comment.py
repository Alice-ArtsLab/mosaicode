#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Comment(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.comment = ""

        self.help = "Insert a comment"

        self.description = {
            "Label": "Comment",
            "Icon": "images/comment.png",
            "Color": "50:100:200:150",
            "InTypes": "",
            "OutTypes": "",
            "TreeGroup": "General"
        }

        self.properties = {
            "comment": {
                "name": "Comment",
                "type": HARPIA_COMMENT
            }
        }

        # ----------------C/OpenCv code--------------------------------
        self.vars = '/* $comment$ */ \n'

    # ----------------------------------------------------------------------
    def get_help(self):
        return self.help

    # ----------------------------------------------------------------------
    def get_description(self):
        return self.description

    # ----------------------------------------------------------------------
    def get_properties(self):
        return self.properties

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return self.vars

# -----------------------------------------------------------------------------
