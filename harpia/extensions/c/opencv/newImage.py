#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the NewImage class.
"""
from harpia.GUI.fieldtypes import *
from harpia.extensions.c.opencv.opencvplugin import OpenCVPlugin


class NewImage(OpenCVPlugin):
    """
    This class contains methods related the NewImage class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.width = "640"
        self.height = "480"

        # Appearance
        self.help = "Cria uma nova imagem."
        self.label = "New Image"
        self.color = "50:100:200:150"
        self.out_types = ["harpia.extensions.c.ports.image"]
        self.group = "Image Source"

        self.properties = [{"name": "Width",
                            "label": "width",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Height",
                            "label": "Height",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.codes[2] = \
            'CvSize size$id$ = cvSize($width$,$height$);\n' + \
            'block$id$_img_o0 = cvCreateImage(size$id$,IPL_DEPTH_8U,3);\n' + \
            'cvSetZero(block$id$_img_o0);\n'

# ------------------------------------------------------------------------------
