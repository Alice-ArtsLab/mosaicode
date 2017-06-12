#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the MoveRct class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin


class MoveRct(Plugin):
    """
    This class contains methods related the MoveRct class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.offset_x = 0
        self.offset_y = 0

        # Appearance
        self.help = "Move Rectangle`s (0,0) point to input point"
        self.label = "Move Rectangle"
        self.color = "50:50:200:150"
        self.in_types = ["mosaicode.extensions.c.ports.rect", "mosaicode.extensions.c.ports.point"]
        self.out_types = ["mosaicode.extensions.c.ports.rect"]
        self.group = "Experimental"

        self.properties = [{"name": "Offset x",
                            "label": "offset_x",
                            "type": MOSAICODE_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Offset Y",
                            "label": "offset_y",
                            "type": MOSAICODE_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            }
                           ]
        # --------------------C/OpenCv code--------------------------------
        self.codes[1] = \
            'CvRect block$id$_rect_i0;\n' + \
            'CvPoint block$id$_point_i1;\n' + \
            'CvRect block$id$_rect_o0;\n'

        self.codes[2] = \
            'block$id$_rect_o0 = block$id$_rect_i0;\n' + \
            'block$id$_rect_o0.x = block$id$_point_i1.x + $offset_x$;\n' + \
            'block$id$_rect_o0.y = block$id$_point_i1.y + $offset_y$;\n'
        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
