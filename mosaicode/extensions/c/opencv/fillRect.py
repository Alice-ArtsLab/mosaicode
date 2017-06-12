#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the FillRect class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin


class FillRect(Plugin):
    """
    This class contains methods related the FillRect class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.rect_color = "#0000ffff0000"

        # Appearance
        self.help = "Preenche o retângulo de uma cor."
        self.label = "Fill Rectangle"
        self.color = "50:100:200:150"
        self.in_ports = [{"type":"mosaicode.extensions.c.ports.image",
                          "name":"input_image",
                          "label":"Input Image"},
                         {"type":"mosaicode.extensions.c.ports.rect",
                          "name":"rect",
                          "label":"Rectangle"}
                         ]
        self.out_ports = [{"type":"mosaicode.extensions.c.ports.image",
                           "name":"output_image",
                           "label":"Output Image"}]
        self.group = "Basic Shapes"

        self.properties = [{"name": "color",
                            "label": "Color",
                            "type": MOSAICODE_COLOR
                            }
                           ]

        self.codes[0] = \
            "CvScalar get_scalar_color(const char * rgbColor){\n" + \
            "   if (strlen(rgbColor) < 13 || rgbColor[0] != '#')\n" + \
            "       return cvScalar(0,0,0,0);\n" + \
            "   char r[4], g[4], b[4];\n" + \
            "   strncpy(r, rgbColor+1, 4);\n" + \
            "   strncpy(g, rgbColor+5, 4);\n" + \
            "   strncpy(b, rgbColor+9, 4);\n" + \
            "\n" + \
            "   int ri, gi, bi = 0;\n" + \
            "   ri = (int)strtol(r, NULL, 16);\n" + \
            "   gi = (int)strtol(g, NULL, 16);\n" + \
            "   bi = (int)strtol(b, NULL, 16);\n" + \
            "\n" + \
            "   ri /= 257;\n" + \
            "   gi /= 257;\n" + \
            "   bi /= 257;\n" + \
            "   \n" + \
            "   return cvScalar(bi, gi, ri, 0);\n" + \
            "}\n"

        self.codes[1] = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'CvRect block$id$_rect_i1;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n'

        # ----------------------------------------------------------------------
        self.codes[2] = \
            '\nif(block$id$_img_i0)\n{\n' + \
            '\tblock$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            '\tcvSetImageROI(block$id$_img_o0 , block$id$_rect_i1);\n' + \
            '\tCvScalar color = get_scalar_color("$prop[color]$");\n' + \
            '\tcvSet(block$id$_img_o0,color,NULL);\n' + \
            '\tcvResetImageROI(block$id$_img_o0);\n' + \
            '}\n'


        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
