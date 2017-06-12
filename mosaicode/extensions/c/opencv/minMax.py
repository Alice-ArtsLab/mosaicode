#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the MinMax class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.plugin import Plugin


class MinMax(Plugin):
    """
    This class contains methods related the MinMax class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)
        self.minX = 0
        self.maxX = 500
        self.minY = 0
        self.maxY = 500
        self.minVal = 0
        self.maxVal = 500
        self.minORmax = "min"
        self.criteria = "pos"

        # Appearance
        self.help = "Finds min or max from input image and judges " + \
            "it according to a custom criteria."
        self.label = "Find Min or Max"
        self.color = "50:50:200:150"
        self.in_types = ["mosaicode.extensions.c.ports.image"]
        self.out_types = ["mosaicode.extensions.c.ports.double", "mosaicode.extensions.c.ports.point"]
        self.group = "Feature Detection"

        self.properties = [{"name": "Min X",
                            "label": "minX",
                            "type": MOSAICODE_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Max X",
                            "label": "maxX",
                            "type": MOSAICODE_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Min Y",
                            "label": "minY",
                            "type": MOSAICODE_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Max Y",
                            "label": "maxY",
                            "type": MOSAICODE_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Min Val",
                            "label": "minVal",
                            "type": MOSAICODE_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Max Val",
                            "label": "maxVal",
                            "type": MOSAICODE_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "Min Or Max",
                            "label": "minORmax",
                            "type": MOSAICODE_COMBO,
                            "values": ["min", "max"]
                            },
                           {"name": "Criteria",
                            "label": "criteria",
                            "type": MOSAICODE_COMBO,
                            "values": ["pos", "val"]
                            }
                           ]
        # ------------------------------C/OpenCv code--------------------------

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        value = '\nif(block$id$_img_i0)\n{\n' + \
                '   double minVal,maxVal;\n' + \
                '   CvPoint minP,maxP;\n' + \
                '   block$id$_double_o0 = 0;\n' + \
                '   cvMinMaxLoc(block$id$_img_i0, &minVal, ' + \
                '&maxVal, &minP, &maxP, NULL);\n'
        if self.minORmax == 'max':
            value += '  minP = maxP;\n' + \
                '   minVal = maxVal;\n'

        value += '  block$id$_point_o1 = minP;\n'

        if self.criteria == "pos":
            value += '  if(minP.x >= $minX$ && minP.x <= $maxX$)\n' + \
                '        if(minP.y >= $minY$ && minP.y <= $maxY$)\n' + \
                '           block$id$_double_o0 = 1.0;\n'
        elif self.criteria == "val":
            value += '  if(minVal >= $minVal$ && minVal <= $maxVal$)\n' + \
                '        block$id$_double_o0 = 1.0;\n'
        value += '}\n'

        return value


        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
