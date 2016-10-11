#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class AddBorder(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.border = 50
        self.color = "#0000ffff0000"
        self.border_type = "IPL_BORDER_CONSTANT"
        self.help = "Adiciona bordas na imagem."

        self.description = {
            "Label": "Add Border",
            "Icon": "images/and.png",
            "Color": "0:180:210:150",
            "InTypes": {0: "HRP_IMAGE", 1: "HRP_INT"},
            "OutTypes": {0: "HRP_IMAGE"},
            "TreeGroup": "Experimental"
        }

        self.properties = {
            "color": {
                "name": "Color", "type": HARPIA_COLOR},
            "border_type": {
                "name": "Type", "type": HARPIA_COMBO,
                "values": ["IPL_BORDER_CONSTANT",
                           "IPL_BORDER_REPLICATE",
                           "IPL_BORDER_REFLECT",
                           "IPL_BORDER_WRAP"]},
            "border": {"name": "Border Size", "type": HARPIA_INT}
        }

        # --------------------c/OpneCV code----------------------------
        self.vars = \
            "IplImage * block$id$_img_i0 = NULL;\n" + \
            "int block$id$_int_i1 = $border$;\n" + \
            "IplImage * block$id$_img_o0 = NULL;\n"

        self.function_call = \
            'if(block$id$_img_i0){\n' + \
            '\tCvSize size$id$ = cvSize(block$id$_img_i0->width +' + \
            ' block$id$_int_i1 * 2, block$id$_img_i0->height' + \
            ' + block$id$_int_i1 * 2);\n' + \
            '\tblock$id$_img_o0 = cvCreateImage(size$id$,' + \
            ' block$id$_img_i0->depth,block$id$_img_i0->nChannels);\n' + \
            '\tCvPoint point$id$ = cvPoint' + \
            '(block$id$_int_i1, block$id$_int_i1);\n' + \
            '\tCvScalar color = cvScalar($blue$,$green$,$red$,0);\n' + \
            '\tcvCopyMakeBorder(block$id$_img_i0, block$id$_img_o0,' + \
            ' point$id$, $border_type$, color);\n' + \
            '}\n'

    # ----------------------------------------------------------------------
    def set_properties(self, data):
        OpenCVPlugin.set_properties(self, data)
        self.red = self.color[1:5]
        self.green = self.color[5:9]
        self.blue = self.color[9:13]

        self.red = int(self.red, 16) / 257
        self.green = int(self.green, 16) / 257
        self.blue = int(self.blue, 16) / 257

    # -------------------------------------------------------------------------
    def get_help(self):
        return self.help

    # -------------------------------------------------------------------------
    def get_description(self):
        return self.description

    # -------------------------------------------------------------------------
    def get_properties(self):
        return self.properties

    # -------------------------------------------------------------------------
    def generate_vars(self):
        return self.vars

    # -------------------------------------------------------------------------
    def generate_function_call(self):
        return self.function_call

# -----------------------------------------------------------------------------
