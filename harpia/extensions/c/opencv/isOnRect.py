#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the IsOnRect class.
"""
from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin


class IsOnRect(Plugin):
    """
    This class contains methods related the IsOnRect class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        Plugin.__init__(self)

        # Appearance
        self.help = "Checks Wheather the given " + \
            "point is inside the given rectangle."
        self.label = "Check Point"
        self.color = "50:50:200:150"
        self.in_types = ["harpia.extensions.c.ports.point", "harpia.extensions.c.ports.rect"]
        self.out_types = ["harpia.extensions.c.ports.double"]
        self.group = "Experimental"

        # ------------------------------C/OpenCv code--------------------------
        self.codes[2] = \
            '\n block$id$_double_o0 = 0.0;\n' + \
            'if(block$id$_point_i0.x >= block$id$_rect_i1.x)\n' + \
            '   if(block$id$_point_i0.y >= block$id$_rect_i1.y)\n' + \
            '       if(block$id$_point_i0.x < block$id$_rect_i1.x + ' + \
            'block$id$_rect_i1.width)\n' + \
            '           if(block$id$_point_i0.y < block$id$_rect_i1.y + ' + \
            'block$id$_rect_i1.height)\n' + \
            '               block$id$_double_o0 = 1.0;\n'


        self.language = "c"
        self.framework = "opencv"
# -----------------------------------------------------------------------------
