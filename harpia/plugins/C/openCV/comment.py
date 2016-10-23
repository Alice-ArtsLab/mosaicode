#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Comment(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.comment = ""

        # Appearance
        self.help = "Insert a comment"
        self.label = "Comment"
        self.icon = "images/comment.png"
        self.color = "50:100:200:150"
        self.group = "General"

        self.properties = {
            "comment": {
                "name": "Comment",
                "type": HARPIA_COMMENT
            }
        }

        # ----------------C/OpenCv code--------------------------------
        self.vars = '/* $comment$ */ \n'

# -----------------------------------------------------------------------------
