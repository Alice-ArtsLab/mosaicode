#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Show class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin


class Show(Plugin):
    """
    This class contains methods related the Show class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)

        # Appearance
        self.help = "Mostra uma imagem da cadeia de processamento de imagens."
        self.label = "Show Image"
        self.color = "50:100:200:150"
        self.in_ports = [{"type":"mosaicode.extensions.c.ports.image",
                          "name":"input_image",
                          "label":"Input Image"}
                         ]
        self.group = "General"

        self.properties = [{"label": "Window Title",
                            "name": "title",
                            "type": MOSAICODE_STRING,
                            "value":"My Image"
                            },
                           {"label": "Window Type",
                            "name": "window_type",
                            "type": MOSAICODE_COMBO,
                            "values": ["Window Size",
                                       "Image Size"],
                            "value":"Image Size"
                            }
                           ]

        self.codes[1] = "IplImage * block$id$_img_i0 = NULL;\n" + \
                "if (strcmp(\"Window Size\", \"$prop[window_type]$\") == 0)\n" + \
                "cvNamedWindow(\"$prop[title]$\",CV_WINDOW_NORMAL);\n" + \
                "else\n" + \
                "cvNamedWindow(\"$prop[title]$\",CV_WINDOW_AUTOSIZE);\n"

        self.codes[2] = "\nif(block$id$_img_i0){\n" + \
            "cvShowImage(\"$prop[title]$\",block$id$_img_i0);\n" + \
            "if (strcmp(\"Window Size\", \"$prop[window_type]$\") == 0)\n" + \
            "cvSetWindowProperty(\"$prop[title]$\", " + \
            "CV_WND_PROP_FULLSCREEN, CV_WINDOW_FULLSCREEN);\n" + \
            "}\n"

        self.codes[3] = "cvReleaseImage(&block$id$_img_i0);"


        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
