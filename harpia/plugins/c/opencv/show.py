#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Show class.
"""
from harpia.GUI.fieldtypes import *
from harpia.plugins.c.opencv.opencvplugin import OpenCVPlugin


class Show(OpenCVPlugin):
    """
    This class contains methods related the Show class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        OpenCVPlugin.__init__(self)

        # Appearance
        self.help = "Mostra uma imagem da cadeia de processamento de imagens."
        self.label = "Show Image"
        self.color = "50:100:200:150"
        self.in_ports = [{"type":"HRP_IMAGE",
                          "name":"input_image",
                          "label":"Input Image"}
                         ]
        self.group = "General"

        self.properties = [{"label": "Window Title",
                            "name": "title",
                            "type": HARPIA_STRING,
                            "value":"My Image"
                            },
                           {"label": "Window Type",
                            "name": "window_type",
                            "type": HARPIA_COMBO,
                            "values": ["Window Size",
                                       "Image Size"],
                            "value":"Image Size"
                            }
                           ]

        self.vars = "IplImage * block$id$_img_i0 = NULL;\n" + \
                "if (strcmp(\"Window Size\", \"$window_type$\") == 0)\n" + \
                "cvNamedWindow(\"$title$\",CV_WINDOW_NORMAL);\n" + \
                "else\n" + \
                "cvNamedWindow(\"$title$\",CV_WINDOW_AUTOSIZE);\n"

        self.function_call = "\nif(block$id$_img_i0){\n" + \
            "cvShowImage(\"$title$\",block$id$_img_i0);\n" + \
            "if (strcmp(\"Window Size\", \"$window_type$\") == 0)\n" + \
            "cvSetWindowProperty(\"$title$\", " + \
            "CV_WND_PROP_FULLSCREEN, CV_WINDOW_FULLSCREEN);\n" + \
            "}\n"

        self.dealloc = "cvReleaseImage(&block$id$_img_i0);"

# -----------------------------------------------------------------------------
