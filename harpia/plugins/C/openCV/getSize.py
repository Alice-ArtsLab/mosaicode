#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class GetSize(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)

        self.help = "Extracts the input image size."

        self.description = {
            'Label': 'Get Size',
            'Icon': 'images/getSize.xpm',
            'Color': '250:20:30:150',
            'InTypes': {0: 'HRP_IMAGE'},
            'OutTypes': {0: 'HRP_RECT'},
            'TreeGroup': 'Experimental',
            'TimeShifts': False
        }

        self.properties = {}

        # ------------------------------C/OpenCv code--------------------------
        self.vars = ""

        self.function_call = \
            '\nif(block$id$_img_i0)\n{\n' + \
            '  \tblock$id$_rect_o0 = cvRect( 0, 0, ' + \
            'block$id$_img_i0->width, block$id$_img_i0->height);\n' + \
            '}\n'

    # ----------------------------------------------------------------------
    def get_help(self):
        return self.help

    # ----------------------------------------------------------------------
    def get_description(self):
        return self.description

    # ----------------------------------------------------------------------
    def get_properties(self):
        return self.properties

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        return self.function_call

# -----------------------------------------------------------------------------
