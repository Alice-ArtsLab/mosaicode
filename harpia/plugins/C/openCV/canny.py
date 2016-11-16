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

        self.properties = [{"name": "Aperture Size",
                            "label": "apertureSize",
                            "type": HARPIA_INT,
                            "lower": 1,
                            "upper": 10,
                            "step": 1
                            },
                           {"name": "Threshold 1",
                            "label": "threshold1",
                            "type": HARPIA_INT,
                            "lower": 1,
                            "upper": 100,
                            "step": 1
                            },
                           {"name": "Threshold 2",
                            "label": "threshold2",
                            "type": HARPIA_INT,
                            "lower": 1,
                            "upper": 100,
                            "step": 1
                            }
                           ]

        # -------------------------C/OpenCV code----------------------------
        self.vars = \
            'IplImage * block$id$_img_i0 = NULL;\n' + \
            'IplImage * block$id$_img_o0 = NULL;\n' + \
            'int block$id$_int_i1 = $threshold2$;\n' + \
            'int block$id$_int_i3 = $apertureSize$;\n' + \
            'int block$id$_int_i2 = $threshold1$;\n'

        self.function_call = \
            "if(block$id$_img_i0){ //Canny Code\n" + \
            "\tif (block$id$_int_i1 < 1) block$id$_int_i1 = 1;\n" + \
            "\tif (block$id$_int_i2 < 1) block$id$_int_i2 = 1;\n" + \
            "\tif (block$id$_int_i3 < 1) block$id$_int_i3 = 1;\n" + \
            "\tif (block$id$_int_i1 > 10) block$id$_int_i1 = 10;\n" + \
            "\tif (block$id$_int_i2 > 100) block$id$_int_i2 = 100;\n" + \
            "\tif (block$id$_int_i3 > 100) block$id$_int_i3 = 100;\n" + \
            "\tblock$id$_img_o0 = cvCloneImage(block$id$_img_i0);\n" + \
            "\tIplImage * tmpImg$id$ =" + \
            " cvCreateImage(cvGetSize(block$id$_img_i0),8,1);\n" + \
            "\tif(block$id$_img_i0->nChannels == 3){\n" + \
            "    \t\tcvCvtColor(block$id$_img_i0," + \
            " tmpImg$id$ ,CV_RGB2GRAY);\n" + \
            "\t}else{\n" + \
            "    \t\ttmpImg$id$ = block$id$_img_i0 = NULL;\n" + \
            "}\n" + \
            "cvCanny(tmpImg$id$, tmpImg$id$, block$id$_int_i2," + \
            " block$id$_int_i1, block$id$_int_i3);\n" + \
            "\tif(block$id$_img_i0->nChannels == 3){\n" + \
            "    \t\tcvCvtColor(tmpImg$id$, " + \
            "block$id$_img_o0,CV_GRAY2RGB);\n" + \
            "\t}else{\n" + \
            "    \t\tcvCopyImage(tmpImg$id$, block$id$_img_o0);\n" + \
            "\t}\n" + \
            "\tcvReleaseImage(&tmpImg$id$);\n" + \
            "} // End Canny Code\n"

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        self.apertureSize = int(float(self.apertureSize))
        self.threshold1 = int(float(self.threshold1))
        self.threshold2 = int(float(self.threshold2))

        return self.function_call

# ------------------------------------------------------------------------------
