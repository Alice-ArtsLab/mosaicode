#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Save class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Save(OpenCVPlugin):
    """
    This class contains methods related the Save class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.filename = ""

        # Appearance
        self.help = "Salva uma imagem em uma mídia indicada pelo usuário." + \
            "Atualmente a imagem é salva como PNG por padrão."
        self.label = "Save Image"
        self.color = "50:100:200:150"
        self.in_types = ["HRP_IMAGE"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "General"

        self.properties = [{"name": "File Name",
                            "label": "filename",
                            "type": HARPIA_SAVE_FILE
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.function_call = \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'if(block$id$_img_i0)\n' + \
            'cvSaveImage("$filename$" ,block$id$_img_i0);\n'

# -----------------------------------------------------------------------------
