#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Comment(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = "10"
        self.comment = ""

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Insert a comment"

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.functionCall = '/*'+self.comment+'*/ \n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label":_("Comment"),
            "Icon":"images/comment.png",
            "Color":"50:100:200:150",
            "InTypes":"",
            "OutTypes":"",
            "Description":_("Insert a comment."),
            "TreeGroup":_("General")
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
