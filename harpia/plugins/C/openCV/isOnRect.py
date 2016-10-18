#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class IsOnRect(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)

        self.help = "Checks Wheather the given " + \
            "point is inside the given rectangle."

        self.description = {
            'Label': 'Check Point',
            'Icon': 'images/isOnRect.png',
            'Color': '50:50:200:150',
            'InTypes': {0: 'HRP_POINT', 1: 'HRP_RECT'},
            'OutTypes': {0: 'HRP_DOUBLE'},
            'TreeGroup': 'Experimental'
        }

        # ------------------------------C/OpenCv code--------------------------
        self.function_call = \
            '\n block$id$_double_o0 = 0.0;\n' + \
            'if(block$id$_point_i0.x >= block$id$_rect_i1.x)\n' + \
            '   if(block$id$_point_i0.y >= block$id$_rect_i1.y)\n' + \
            '       if(block$id$_point_i0.x < block$id$_rect_i1.x + ' + \
            'block$id$_rect_i1.width)\n' + \
            '           if(block$id$_point_i0.y < block$id$_rect_i1.y + ' + \
            'block$id$_rect_i1.height)\n' + \
            '               block$id$_double_o0 = 1.0;\n'

# -----------------------------------------------------------------------------
