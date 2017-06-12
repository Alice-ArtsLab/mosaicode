#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Fill class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin


class Fill(Plugin):
    """
    This class contains methods related the Fill class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.rect_color = "#0000ffff0000"

        # Appearance
        self.help = "Preenche toda a imagem de uma cor."
        self.label = "Fill image"
        self.color = "50:100:200:150"
        self.in_types = ["mosaicode.extensions.c.ports.image"]
        self.out_types = ["mosaicode.extensions.c.ports.image"]
        self.group = "General"

        self.properties = [{"name": "rect_Color",
                            "label": "rect_color",
                            "type": MOSAICODE_COLOR
                            }
                           ]

        # ------------------------------C/OpenCv code--------------------------

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        # --------define RGB-------------
        red = self.rect_color[1:5]
        green = self.rect_color[5:9]
        blue = self.rect_color[9:13]

        red = int(red, 16) / 257
        green = int(green, 16) / 257
        blue = int(blue, 16) / 257

        return \
            'if(block$id$_img_i0){\n' + \
            '\tblock$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            '\tCvScalar color = cvScalar' + \
            '(' + str(blue) + ',' + str(green) + ',' + str(red) + ',0);\n' + \
            '\tcvSet(block$id$_img_o0, color, NULL);\n' + \
            '}\n'


        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
