#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Smooth class.
"""
from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin


class Smooth(Plugin):
    """
    This class contains methods related the Smooth class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.smooth_type = "CV_GAUSSIAN"
        self.param1 = 7
        self.param2 = 9

        # Appearance
        self.help = "Aplicação de um filtro de suavização. " + \
            "Suaviza os contornos de objetos na imagem, borrando-os levemente."
        self.label = "Smooth"
        self.color = "50:125:50:150"
        self.in_types = ["harpia.extensions.c.ports.image", "harpia.extensions.c.ports.int"]
        self.out_types = ["harpia.extensions.c.ports.image", "harpia.extensions.c.ports.int", "harpia.extensions.c.ports.int"]
        self.group = "Filters and Color Conversion"

        self.properties = [{"name": "Type",
                            "label": "smooth_type",
                            "type": HARPIA_COMBO,
                            "values": ["CV_GAUSSIAN", "CV_BLUR", "CV_MEDIAN"]
                            },
                           {"name": "Parameter 1",
                            "label": "param1",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 99,
                            "step": 1
                            },
                           {"name": "Parameter 2",
                            "label": "param2",
                            "type": HARPIA_INT,
                            "lower": 0,
                            "upper": 99,
                            "step": 1
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.codes[1] = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'int block$id$_int_i1 = $param1$;\n' + \
            'int block$id$_int_i2 = $param2$;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n'

        self.codes[2] = \
            '\nif(block$id$_img_i0){\n' + \
            'block$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n' + \
            'block$id$_int_i1 = (block$id$_int_i1 %2 == 0)? ' + \
            'block$id$_int_i1 + 1 : block$id$_int_i1;\n' + \
            'block$id$_int_i2 = (block$id$_int_i2 %2 == 0)? ' + \
            'block$id$_int_i2 + 1 : block$id$_int_i2;\n' + \
            'cvSmooth(block$id$_img_i0, block$id$_img_o0, ' + \
            '$smooth_type$,block$id$_int_i1,block$id$_int_i2,0,0);\n' + \
            '}\n'


        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
