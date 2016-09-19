#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class Speaker(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = self.__class__.__module__

    # ----------------------------------------------------------------------
    def get_help(self):#Função que chama a help
        return "Sound output"

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO = ''
        blockTemplate.functionCall = ''
        blockTemplate.dealloc = ''

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
            "Label": _("Speaker"),
            "Icon": "images/show.png",
            "Color": "50:150:250:150",
            "InTypes": {0: "HRP_WEBAUDIO_SOUND"},
            "OutTypes": {},
            "Description": _("Sound Output"),
            "TreeGroup": _("Sound")
            }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {}

# ------------------------------------------------------------------------------
