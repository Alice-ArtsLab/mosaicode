#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Pow class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin


class Pow(Plugin):
    """
    This class contains methods related the Pow class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        # Appearance
        self.help = "Eleva cada ponto de uma " + \
            "imagem a um valor fixo de potência."
        self.label = "Pow"
        self.color = "230:230:60:150"
        self.in_ports = [{"type":"mosaicode.extensions.c.ports.image",
                          "name":"input_image",
                          "label":"Input Image"}
                         ]
        self.out_ports = [{"type":"mosaicode.extensions.c.ports.image",
                           "name":"output_image",
                           "label":"Output Image"}]
        self.group = "Math Functions"

        self.properties = [{"label": "Exponent",
                            "name": "exponent",
                            "value":1,
                            "type": MOSAICODE_INT,
                            "lower": 1,
                            "upper": 10,
                            "step": 1
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.codes[2] = \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'cvPow(block$id$_img_i0, block$id$_img_o0, $exponent$);\n' + \
            '}\n'


        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
