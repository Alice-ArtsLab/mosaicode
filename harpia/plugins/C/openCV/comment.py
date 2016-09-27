#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin

class Comment(OpenCVPlugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.comment = ""

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Insert a comment"

    # ----------------------------------------------------------------------
    def generate_vars(self):
        return '/* $comment$ */ \n'

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Label":"Comment",
            "Icon":"images/comment.png",
            "Color":"50:100:200:150",
            "InTypes":"",
            "OutTypes":"",
            "TreeGroup":"General"
         }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {
        "comment":{"name": "Comment",
                    "type": HARPIA_COMMENT,
                    "value": self.comment
                    }
        }
# ------------------------------------------------------------------------------
