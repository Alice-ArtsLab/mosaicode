#!/usr/bin/env python
# -*- coding: utf-8 -*-

from harpia.GUI.fieldtypes import *
from harpia.plugins.C.openCV.opencvplugin import OpenCVPlugin


class Canny(OpenCVPlugin):

    # -------------------------------------------------------------------------
    def __init__(self):
        OpenCVPlugin.__init__(self)
        self.apertureSize = 3
        self.threshold1 = 16
        self.threshold2 = 33

        # Appearance
        self.help = "Operacão de filtragem que implementa o algoritmo " + \
            "Canny para detecção de contornos e bordas." + \
            "\nPropriedades\nLimiar 1 e Limiar 2: os dois valores" + \
            " de limiar são utilizados em conjunto." + \
            "O menor valor é utilizado para a realizar a " + \
            "conexão de cantos e bordas." + \
            "O maior valor é utilizado para encontrar" + \
            " segmentos iniciais das bordas mais significativas."
        self.label = "Canny"
        self.icon = "images/canny.png"
        self.color = "50:180:80:150"
        self.in_types = ["HRP_IMAGE", "HRP_INT", "HRP_INT", "HRP_INT"]
        self.out_types = ["HRP_IMAGE"]
        self.group = "Gradients, Edges and Corners"

        self.properties = {
            "apertureSize": {
                "name": "Aperture Size",
                "type": HARPIA_INT,
                "lower": 1,
                "upper": 10,
                "step": 1
            },
            "threshold1": {
                "name": "Threshold 1",
                "type": HARPIA_INT,
                "lower": 1,
                "upper": 100,
                "step": 1
            },
            "threshold2": {"name": "Threshold 2",
                           "type": HARPIA_INT,
                           "lower": 1,
                           "upper": 100,
                           "step": 1
                           }
        }

        # -------------------------C/OpenCV code----------------------------
        self.vars = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'int block$id$_int_i1 = $threshold2$;\n' + \
            'int block$id$_int_i3 = $apertureSize$;\n' + \
            'int block$id$_int_i2 = $threshold1$;\n'

        self.function_call = \
            "if(block$id$_img_i0){ //Canny Code" + \
            "\tif (block$id$_int_i1 < 1) block$id$_int_i1 = 1;" + \
            "\tif (block$id$_int_i2 < 1) block$id$_int_i2 = 1;" + \
            "\tif (block$id$_int_i3 < 1) block$id$_int_i3 = 1;" + \
            "\tif (block$id$_int_i1 > 10) block$id$_int_i1 = 10;" + \
            "\tif (block$id$_int_i2 > 100) block$id$_int_i2 = 100;" + \
            "\tif (block$id$_int_i3 > 100) block$id$_int_i3 = 100;" + \
            "\tblock$id$_img_o0 = cvCloneImage(block$id$_img_i0);" + \
            "\tIplImage * tmpImg$id$ =" + \
            " cvCreateImage(cvGetSize(block$id$_img_i0),8,1);" + \
            "\tif(block$id$_img_i0->nChannels == 3){" + \
            "    \t\tcvCvtColor(block$id$_img_i0," + \
            " tmpImg$id$ ,CV_RGB2GRAY);" + \
            "\t}else{" + \
            "    \t\ttmpImg$id$ = block$id$_img_i0 = NULL;" + \
            "}" + \
            "cvCanny(tmpImg$id$, tmpImg$id$, block$id$_int_i2," + \
            " block$id$_int_i1, block$id$_int_i3);" + \
            "\tif(block$id$_img_i0->nChannels == 3){" + \
            "    \t\tcvCvtColor(tmpImg$id$, block$id$_img_o0,CV_GRAY2RGB);" + \
            "\t}else{" + \
            "    \t\tcvCopyImage(tmpImg$id$, block$id$_img_o0);" + \
            "\t}" + \
            "\tcvReleaseImage(&tmpImg$id$);" + \
            "} // End Canny Code"

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        self.apertureSize = int(float(self.apertureSize))
        self.threshold1 = int(float(self.threshold1))
        self.threshold2 = int(float(self.threshold2))

        return self.function_call

# ------------------------------------------------------------------------------
